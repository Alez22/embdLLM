"""Pure aggregation of agent_run.json archives for static reporting.

Kept separate from dashboard.py so the CLI report command does not pull in
the FastAPI web stack. The discovery/filtering rules here mirror the
dashboard ones (container-only runs, latest-per-key) on purpose — see
dashboard._load_agent_runs / _latest_agent_run_per_key.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from embedeval.agent_report import AGENT_RUN_FILENAME

# Models that cannot be deployed on local infrastructure (Powersoft privacy
# requirement). Used only to flag the "open-weight" column in the report —
# matched as a substring of the model identifier.
_CLOUD_ONLY_VENDORS = ("anthropic",)


@dataclass
class ModelSummary:
    """One row of the agent leaderboard: the latest container run for a model."""

    model: str
    max_turns: int
    context_pack: str | None
    passed: int
    total: int
    recovery_rate: float | None
    total_cost_usd: float
    total_tokens: int
    run_id: str
    # case_id -> turn it passed on (1-based), or None if it never passed.
    passed_at_turn: dict[str, int | None] = field(default_factory=dict)

    @property
    def is_open_weight(self) -> bool:
        """True unless the model is from a cloud-only vendor (cannot deploy local)."""
        return not any(v in self.model for v in _CLOUD_ONLY_VENDORS)

    @property
    def provider(self) -> str:
        """Provider prefix of the model id (e.g. 'openrouter', 'groq')."""
        return self.model.split("/", 1)[0] if "/" in self.model else "?"


def _run_used_build(run: dict) -> bool:
    """@brief True if the run used the real L1 compile gate (container).

    Mirrors dashboard._agent_run_used_build: host soft-skip names its L1
    check ``nxp_available`` and must be excluded — those runs report a
    spurious L1 pass.
    """
    for case in run.get("cases", []):
        for turn in case.get("history", []):
            for layer in turn.get("layers", []):
                if layer.get("layer") != 1:
                    continue
                for det in layer.get("details", []):
                    if det.get("check_name") == "nxp_available":
                        return False
    return True


def load_agent_runs(results_dir: Path) -> list[dict]:
    """@brief Load every agent_run.json under <results>/runs/, newest-first.

    The mock model is excluded, matching the dashboard.
    """
    runs_root = results_dir / "runs"
    if not runs_root.is_dir():
        return []
    runs: list[dict] = []
    for run_dir in sorted(runs_root.iterdir(), reverse=True):
        archive = run_dir / AGENT_RUN_FILENAME
        if not archive.is_file():
            continue
        try:
            data = json.loads(archive.read_text(encoding="utf-8"))
        except Exception:
            continue
        if data.get("model") == "mock":
            continue
        data["run_id"] = run_dir.name
        runs.append(data)
    return runs


def latest_container_runs(runs: list[dict]) -> list[dict]:
    """@brief Keep the most recent container run per (model, turns, pack).

    Host-mode runs are dropped. Runs come in newest-first, so first-seen wins.
    Mirrors dashboard._latest_agent_run_per_key.
    """
    seen: set[tuple[str, int, str | None]] = set()
    kept: list[dict] = []
    for run in runs:
        if not _run_used_build(run):
            continue
        key = (run.get("model", ""), run.get("max_turns", 0), run.get("context_pack"))
        if key in seen:
            continue
        seen.add(key)
        kept.append(run)
    return kept


def summarize_run(run: dict) -> ModelSummary:
    """@brief Reduce one agent_run.json into a leaderboard row."""
    cases = run.get("cases", [])
    summary = run.get("summary", {})
    passed_at_turn = {
        c["case_id"]: c.get("passed_at_turn") for c in cases
    }
    return ModelSummary(
        model=run.get("model", "?"),
        max_turns=run.get("max_turns", 0),
        context_pack=run.get("context_pack"),
        passed=sum(1 for c in cases if c.get("passed")),
        total=len(cases),
        recovery_rate=summary.get("recovery_rate"),
        total_cost_usd=summary.get("total_cost_usd", 0.0),
        total_tokens=summary.get("total_tokens", 0),
        run_id=run.get("run_id", "?"),
        passed_at_turn=passed_at_turn,
    )


def build_leaderboard(results_dir: Path) -> list[ModelSummary]:
    """@brief Build the agent leaderboard, best models first.

    Sorted by pass count desc, then cheaper wins ties. Cost is the primary
    tie-break but is 0 for providers that do not report it (see the cost-column
    note in agent_leaderboard.py), so total tokens acts as the working proxy.
    """
    runs = latest_container_runs(load_agent_runs(results_dir))
    rows = [summarize_run(r) for r in runs]
    rows.sort(key=lambda r: (-r.passed, r.total_cost_usd, r.total_tokens))
    return rows
