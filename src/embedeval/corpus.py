"""Generation corpus — persistent store for LLM-generated code cells.

Layout on disk:
    results/corpus/<model_slug>/<case_id>/<attempt>.json

Each file is a CorpusCell.  The cache key is
    (prompt_hash, model, temperature, generation_params, attempt)
and is stored inside the file so a key mismatch is detected on load
(e.g. the prompt was edited but the file from the old prompt is still
present under the same path).

Usage in runner.py:
    cell = corpus_lookup(corpus_dir, case_id, model, attempt, key)
    if cell is not None:
        use cell.generated_code          # cache hit
    else:
        generated_code = call_model(...)
        corpus_store(corpus_dir, case_id, model, attempt, key, ...)
"""

import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

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
    """Return the file path for a corpus cell."""
    model_slug = model.replace("/", "_").replace(":", "_")
    return corpus_dir / model_slug / case_id / f"{attempt}.json"


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
