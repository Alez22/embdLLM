"""Generation corpus and grading cache.

Generation cache layout:
    results/corpus/generations/<model_slug>/<case_id>/<attempt>.json  (CorpusCell)

Grading cache layout:
    results/corpus/grades/<generated_code_hash>/<checks_hash>.json  (GradeCell)

Generation cache key:  (prompt_hash, model, temperature, generation_params, attempt)
Grading cache key:     (generated_code_hash, checks_hash)

The two caches are independent:
  - Editing a prompt → generation miss → regenerate → grading miss → re-grade.
  - Editing only a check → generation hit → grading miss → re-grade from cached code.
  - Neither changed → both hit → zero work.
"""

import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from embedeval.models import LayerResult

if TYPE_CHECKING:
    from embedeval.models import EvalResult

logger = logging.getLogger(__name__)

CORPUS_DIRNAME = "corpus"


class GenerationParams(BaseModel):
    """Parameters that affect LLM output (besides model and temperature)."""

    no_think: bool = False
    feedback_rounds: int = 0

    def as_sorted_dict(self) -> dict:
        """Return a stable dict representation for hashing."""
        return {"feedback_rounds": self.feedback_rounds, "no_think": self.no_think}


class CorpusCell(BaseModel):
    """One cached generation — a single (case, model, attempt) cell."""

    # Cache key fields — stored so we can detect key mismatches on load.
    prompt_hash: str
    model: str
    temperature: float = Field(ge=0.0)
    generation_params: dict  # serialized GenerationParams.as_sorted_dict()
    attempt: int = Field(ge=1)

    # Payload
    generated_code: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = Field(default=0.0, ge=0.0)
    generated_at: str  # ISO timestamp


def hash_prompt(prompt: str) -> str:
    """Return a 16-char SHA256 prefix of the full prompt text."""
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]


def _cell_path(corpus_dir: Path, case_id: str, model: str, attempt: int) -> Path:
    """Return the file path for a generation corpus cell."""
    model_slug = model.replace("/", "_").replace(":", "_")
    return corpus_dir / "generations" / model_slug / case_id / f"{attempt}.json"


def corpus_lookup(
    corpus_dir: Path,
    case_id: str,
    model: str,
    attempt: int,
    prompt_hash: str,
    temperature: float,
    generation_params: dict,
) -> CorpusCell | None:
    """Return the cached cell if it exists and the key matches, else None.

    A key mismatch (e.g. prompt was edited) is treated as a cache miss so
    the caller regenerates and overwrites the stale cell.
    """
    path = _cell_path(corpus_dir, case_id, model, attempt)
    if not path.is_file():
        return None

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        cell = CorpusCell.model_validate(data)
    except Exception as exc:
        logger.warning("Corpus: failed to load %s: %s", path, exc)
        return None

    if (
        cell.prompt_hash != prompt_hash
        or cell.model != model
        or cell.temperature != temperature
        or cell.generation_params != generation_params
    ):
        logger.debug(
            "Corpus: key mismatch for %s attempt %d — treating as miss",
            case_id,
            attempt,
        )
        return None

    return cell


def corpus_store(
    corpus_dir: Path,
    case_id: str,
    model: str,
    attempt: int,
    prompt_hash: str,
    temperature: float,
    generation_params: dict,
    generated_code: str,
    input_tokens: int,
    output_tokens: int,
    cost_usd: float,
) -> None:
    """Write a cell to the corpus store, overwriting any existing file."""
    path = _cell_path(corpus_dir, case_id, model, attempt)
    path.parent.mkdir(parents=True, exist_ok=True)

    cell = CorpusCell(
        prompt_hash=prompt_hash,
        model=model,
        temperature=temperature,
        generation_params=generation_params,
        attempt=attempt,
        generated_code=generated_code,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost_usd=cost_usd,
        generated_at=datetime.now(tz=timezone.utc).isoformat(),
    )
    path.write_text(
        cell.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )
    logger.debug("Corpus: stored %s attempt %d at %s", case_id, attempt, path)


# ---------------------------------------------------------------------------
# Grading cache
# ---------------------------------------------------------------------------

def hash_code(generated_code: str) -> str:
    """Return a 16-char SHA256 prefix of the generated code."""
    return hashlib.sha256(generated_code.encode("utf-8")).hexdigest()[:16]


def hash_checks(case_dir: Path) -> str:
    """Return a 16-char content hash of all check files in case_dir/checks/.

    Covers static.py, behavior.py, and negatives.py (if present).
    A change to any of these produces a different hash → grading cache miss.
    """
    checks_dir = case_dir / "checks"
    if not checks_dir.is_dir():
        return "no_checks"

    parts: list[str] = []
    for name in ("static.py", "behavior.py", "negatives.py"):
        f = checks_dir / name
        if f.is_file():
            fhash = hashlib.sha256(f.read_bytes()).hexdigest()[:8]
            parts.append(f"{name}:{fhash}")

    if not parts:
        return "no_checks"

    return hashlib.sha256("\n".join(parts).encode()).hexdigest()[:16]


class GradeCell(BaseModel):
    """Cached output of the check pipeline.

    Stores ONLY fields that are a pure function of (generated_code, checks).
    Excludes runtime/per-call fields (model, attempt, token_usage, cost_usd,
    duration_seconds, ...) which would poison cross-model and cross-attempt
    lookups if shared via the cache.
    """

    layers: list[LayerResult]
    failed_at_layer: int | None = Field(default=None, ge=0, le=4)
    passed: bool
    total_score: float = Field(default=1.0, ge=0.0, le=1.0)


def _grade_path(corpus_dir: Path, code_hash: str, checks_hash: str) -> Path:
    """Return the file path for a grade cache entry.

    Two-level layout: first dir is the code hash (16 chars), file name is
    the checks hash.  This keeps the directory tree shallow even with many
    models and cases.
    """
    return corpus_dir / "grades" / code_hash / f"{checks_hash}.json"


def grade_lookup(
    corpus_dir: Path,
    generated_code: str,
    case_dir: Path,
) -> GradeCell | None:
    """Return a cached GradeCell if (code_hash, checks_hash) matches, else None.

    The caller is responsible for combining the GradeCell with the current
    call's runtime metadata to build an EvalResult.
    """
    code_hash = hash_code(generated_code)
    checks_hash = hash_checks(case_dir)
    path = _grade_path(corpus_dir, code_hash, checks_hash)

    if not path.is_file():
        return None

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return GradeCell.model_validate(data)
    except Exception as exc:
        logger.warning("Grade cache: failed to load %s: %s", path, exc)
        return None


def grade_store(
    corpus_dir: Path,
    generated_code: str,
    case_dir: Path,
    result: "EvalResult",
) -> None:
    """Persist the check-pipeline output as a GradeCell."""
    code_hash = hash_code(generated_code)
    checks_hash = hash_checks(case_dir)
    path = _grade_path(corpus_dir, code_hash, checks_hash)
    path.parent.mkdir(parents=True, exist_ok=True)

    cell = GradeCell(
        layers=result.layers,
        failed_at_layer=result.failed_at_layer,
        passed=result.passed,
        total_score=result.total_score,
    )
    path.write_text(
        cell.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )
    logger.debug(
        "Grade cache: stored %s/%s at %s", code_hash, checks_hash, path
    )
