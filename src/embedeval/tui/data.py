"""Data loading for the TUI: case discovery and leaderboard aggregation."""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from embedeval.tui import config


def _discover_cases(cases_dir: Path) -> list[dict]:
    """Return minimal case metadata dicts from all metadata.yaml files."""
    cases: list[dict] = []
    for meta_file in sorted(cases_dir.rglob("metadata.yaml")):
        try:
            data = yaml.safe_load(meta_file.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "id" in data:
                cases.append(data)
        except Exception:
            pass
    return cases


def _load_subsets(cases_dir: Path) -> dict[str, list[str]]:
    """Return named case subsets from cases/subsets.yaml.

    Maps subset name -> list of case IDs. Returns {} if the file is missing
    or malformed; the TUI simply shows no subset options in that case.
    """
    subsets_file = cases_dir / "subsets.yaml"
    if not subsets_file.is_file():
        return {}
    try:
        data = yaml.safe_load(subsets_file.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    # Keep only well-formed entries: a name mapping to a list of string IDs.
    return {
        name: [str(cid) for cid in ids]
        for name, ids in data.items()
        if isinstance(ids, list)
    }


def _timestamp_from_dir_name(name: str) -> str:
    """'2026-06-25_2008_openrouter_...' -> '2026-06-25 20:08' (best effort)."""
    m = re.match(r"^(\d{4}-\d{2}-\d{2})_(\d{2})(\d{2})", name)
    if not m:
        return name[:16]
    return f"{m.group(1)} {m.group(2)}:{m.group(3)}"


def _generation_run_row(run_dir: Path, summary_file: Path) -> dict | None:
    """History row for a single-shot generation run (summary.json + details)."""
    try:
        summary = json.loads(summary_file.read_text(encoding="utf-8"))
    except Exception:
        return None
    model = summary.get("model", "")
    if not model or model == "mock":
        return None

    # Derive total/passed from detail files — the ground truth.
    # summary.json totals can be stale if the run was partially overwritten.
    # Details are one file per (case, attempt): dedup to distinct cases,
    # counting a case as passed when any attempt passed (pass@attempts).
    details_dir = run_dir / "details"
    passed_by_case: dict[str, bool] = {}
    sdks: set[str] = set()
    if details_dir.is_dir():
        for f in details_dir.glob("*.json"):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            case_id = d.get("case_id") or f.stem
            passed_by_case[case_id] = (
                passed_by_case.get(case_id, False) or bool(d.get("passed"))
            )
            sdk = d.get("sdk", "")
            if sdk:
                sdks.add(sdk)
    total = len(passed_by_case)
    passed = sum(passed_by_case.values())

    gen_params = summary.get("generation_params", {})
    return {
        "run_id": run_dir.name,
        "timestamp": _timestamp_from_dir_name(run_dir.name),
        "mode": "gen",
        "model": model,
        "temperature": summary.get("temperature", 0.0),
        "no_think": bool(gen_params.get("no_think", False)),
        # n_samples_per_case is the configured attempts count.
        "attempts": summary.get("n_samples_per_case", 1),
        "max_turns": None,
        "context_pack": None,
        "total": total,
        "passed": passed,
        "tokens": None,
        "sdks": sorted(sdks),
    }


def _agent_run_row(run_dir: Path, agent_file: Path) -> dict | None:
    """History row for a multi-turn agent run (agent_run.json archive)."""
    try:
        data = json.loads(agent_file.read_text(encoding="utf-8"))
    except Exception:
        return None
    model = data.get("model", "")
    if not model or model == "mock":
        return None
    cases = data.get("cases", [])
    summary = data.get("summary", {})
    return {
        "run_id": run_dir.name,
        "timestamp": _timestamp_from_dir_name(run_dir.name),
        "mode": "agent",
        "model": model,
        "temperature": data.get("temperature", 0.0),
        "no_think": None,
        "attempts": None,
        "max_turns": data.get("max_turns", 0),
        "context_pack": data.get("context_pack"),
        "total": len(cases),
        "passed": sum(1 for c in cases if c.get("passed")),
        "tokens": summary.get("total_tokens"),
        "sdks": [],  # agent archives carry no per-case sdk field
    }


def _load_runs_summary() -> list[dict]:
    """Return one history row per run dir, newest first.

    Covers both run kinds: agent archives (agent_run.json) and single-shot
    generation runs (summary.json + details/). Mock runs are skipped.
    """
    runs: list[dict] = []
    runs_root = config.RESULTS_DIR / "runs"
    if not runs_root.is_dir():
        return runs
    for run_dir in sorted(runs_root.iterdir(), reverse=True):
        agent_file = run_dir / "agent_run.json"
        summary_file = run_dir / "summary.json"
        if agent_file.is_file():
            row = _agent_run_row(run_dir, agent_file)
        elif summary_file.is_file():
            row = _generation_run_row(run_dir, summary_file)
        else:
            row = None
        if row is not None:
            runs.append(row)
    return runs



def _score_bar(score: float, width: int = 8) -> str:
    """Return a simple ASCII progress bar for a [0,1] score."""
    filled = round(score * width)
    return "█" * filled + "░" * (width - filled)
