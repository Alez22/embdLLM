"""Persistence for multi-turn agent runs.

An agent run is identified by ``(model, max_turns)`` so that, e.g.,
``qwen@t1`` and ``qwen@t3`` are two comparable entries. The full per-turn
history is stored so a later run can --resume from turn N+1 of this one.

This format is intentionally separate from the single-shot ``run`` archive
(report.md / per_check_metrics.json): agent runs are not yet wired into the
leaderboard. See docs/CONTEXT-QUALITY-MODE.md for the agent mode rationale.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from embedeval.agent import AgentResult
from embedeval.models import EvalResult

AGENT_RUN_FILENAME = "agent_run.json"


@dataclass
class AgentRunArchive:
    """In-memory view of an agent run, mirroring agent_run.json on disk."""

    model: str
    max_turns: int
    temperature: float
    timestamp: str
    resumed_from: str | None
    results: list[AgentResult]


def _model_slug(model: str) -> str:
    """Filesystem-safe model slug, matching the convention used by `run`."""
    return model.replace("/", "_").replace(":", "_")


def build_run_dir(output_dir: Path, model: str, max_turns: int) -> Path:
    """@brief Build the run directory path for an agent run.

    Layout: ``<output_dir>/runs/<ts>_<model_slug>_t<N>/`` so that runs with
    different turn budgets never collide and sort next to each other.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    slug = _model_slug(model)
    run_dir = output_dir / "runs" / f"{timestamp}_{slug}_t{max_turns}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _case_total_cost(result: AgentResult) -> float:
    """Sum cost across ALL turns — the price of the multi-turn loop."""
    return sum(r.cost_usd for r in result.history)


def _case_total_tokens(result: AgentResult) -> int:
    """Sum token usage across all turns."""
    return sum(
        r.token_usage.input_tokens + r.token_usage.output_tokens
        for r in result.history
    )


def _passed_at_turn(result: AgentResult) -> int | None:
    """Turn number on which the case passed, or None if it never passed."""
    return result.turns_used if result.passed else None


def _build_summary(results: list[AgentResult]) -> dict:
    """@brief Aggregate comparable metrics for a whole agent run.

    - pass_rate: final pass rate (comparable across turn budgets).
    - recovery_rate: of the cases that failed on turn 1, the fraction that
      eventually passed within max_turns. None when no case failed turn 1.
    - passed_at_turn_hist: how many cases passed on each turn.
    """
    total = len(results)
    passed = [r for r in results if r.passed]

    failed_turn_1 = [r for r in results if not (r.passed and r.turns_used == 1)]
    recovered = [
        r for r in failed_turn_1 if r.passed and r.turns_used > 1
    ]
    recovery_rate = (
        len(recovered) / len(failed_turn_1) if failed_turn_1 else None
    )

    hist: dict[str, int] = {}
    for r in passed:
        key = str(r.turns_used)
        hist[key] = hist.get(key, 0) + 1

    return {
        "pass_rate": len(passed) / total if total else 0.0,
        "recovery_rate": recovery_rate,
        "passed_at_turn_hist": hist,
        "total_cost_usd": sum(_case_total_cost(r) for r in results),
        "total_tokens": sum(_case_total_tokens(r) for r in results),
    }


def _serialize_case(result: AgentResult) -> dict:
    """Serialize one case's agent result, including full per-turn history."""
    return {
        "case_id": result.case_id,
        "passed": result.passed,
        "turns_used": result.turns_used,
        "passed_at_turn": _passed_at_turn(result),
        "total_cost_usd": _case_total_cost(result),
        "total_tokens": _case_total_tokens(result),
        "history": [r.model_dump(mode="json") for r in result.history],
    }


def write_agent_run(
    run_dir: Path,
    model: str,
    max_turns: int,
    temperature: float,
    results: list[AgentResult],
    resumed_from: str | None = None,
    context_pack_name: str | None = None,
    context_pack_hash: str | None = None,
) -> Path:
    """@brief Write agent_run.json into the run directory.

    @param run_dir Target run directory (already created).
    @param resumed_from Path of the run this one continued, or None for a
        fresh run. Marks runs that share their initial turns.
    @param context_pack_name Identity of the run-wide context pack (file name
        or keyword), or None if no pack was used. Lets the dashboard treat
        with-pack vs without-pack as distinct experimental conditions.
    @param context_pack_hash Short hash of the pack text, distinguishing two
        different versions of the same file. None when no pack was used.
    @return Path to the written agent_run.json.
    """
    payload = {
        "model": model,
        "max_turns": max_turns,
        "temperature": temperature,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "resumed_from": resumed_from,
        "context_pack": context_pack_name,
        "context_pack_hash": context_pack_hash,
        "cases": [_serialize_case(r) for r in results],
        "summary": _build_summary(results),
    }
    out_path = run_dir / AGENT_RUN_FILENAME
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out_path


def load_agent_run(run_dir: Path) -> AgentRunArchive:
    """@brief Load a previous agent_run.json for --resume.

    Reconstructs AgentResult objects (with full EvalResult history) so the
    resume path can decide, per case, whether more turns are needed.
    """
    raw = json.loads((run_dir / AGENT_RUN_FILENAME).read_text(encoding="utf-8"))
    results: list[AgentResult] = []
    for case in raw["cases"]:
        history = [EvalResult.model_validate(h) for h in case["history"]]
        results.append(
            AgentResult(
                case_id=case["case_id"],
                passed=case["passed"],
                turns_used=case["turns_used"],
                max_turns=raw["max_turns"],
                history=history,
            )
        )
    return AgentRunArchive(
        model=raw["model"],
        max_turns=raw["max_turns"],
        temperature=raw.get("temperature", 0.0),
        timestamp=raw["timestamp"],
        resumed_from=raw.get("resumed_from"),
        results=results,
    )
