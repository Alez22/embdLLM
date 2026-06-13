"""JSONL checkpoint persistence for resumable runs."""

import json
import logging
from pathlib import Path

from embedeval.models import EvalResult

logger = logging.getLogger(__name__)


def _load_checkpoint(path: Path) -> dict[str, EvalResult]:
    """Load previously completed results from a JSONL checkpoint file.

    Returns a mapping of case_id -> EvalResult for cases that were
    already evaluated in a prior (interrupted) invocation.
    """
    if not path.is_file():
        return {}
    completed: dict[str, EvalResult] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            result = EvalResult.model_validate(data)
            completed[result.case_id] = result
        except Exception as exc:  # noqa: BLE001
            logger.warning("Ignoring bad checkpoint line: %s", exc)
    logger.info(
        "Loaded %d completed case(s) from checkpoint %s",
        len(completed),
        path,
    )
    return completed


def _append_checkpoint(path: Path, result: EvalResult) -> None:
    """Append one EvalResult as a single JSONL line to the checkpoint."""
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(result.model_dump(mode="json"), ensure_ascii=False))
        f.write("\n")
