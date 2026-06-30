"""Data loading for the TUI: case discovery and leaderboard aggregation."""
from __future__ import annotations

import json
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


def _load_runs_summary() -> list[dict]:
    """Return one dict per run dir, built from summary.json + detail stats."""
    runs: list[dict] = []
    runs_root = config.RESULTS_DIR / "runs"
    if not runs_root.is_dir():
        return runs
    for run_dir in sorted(runs_root.iterdir(), reverse=True):
        summary_file = run_dir / "summary.json"
        if not summary_file.is_file():
            continue
        try:
            summary = json.loads(summary_file.read_text(encoding="utf-8"))
        except Exception:
            continue

        # Derive total, passed, score from detail files — the ground truth.
        # summary.json totals can be stale if the run was partially overwritten.
        details_dir = run_dir / "details"
        scores: list[float] = []
        passed = 0
        sdks: set[str] = set()
        if details_dir.is_dir():
            for f in details_dir.glob("*.json"):
                try:
                    d = json.loads(f.read_text(encoding="utf-8"))
                    s = d.get("total_score")
                    if s is not None:
                        scores.append(float(s))
                    if d.get("passed"):
                        passed += 1
                    sdk = d.get("sdk", "")
                    if sdk:
                        sdks.add(sdk)
                except Exception:
                    pass

        avg_score = sum(scores) / len(scores) if scores else 0.0
        total = len(scores)
        model = summary.get("model", "")
        if model == "mock":
            continue
        run_date = summary.get("run_timestamp", run_dir.name[:10])
        run_time = summary.get("run_time", "")
        timestamp = f"{run_date} {run_time}".strip() if run_time else run_date

        # Derive attempts and think from the run dir name or summary fields.
        gen_params = summary.get("generation_params", {})
        no_think = gen_params.get("no_think", False)
        temperature = summary.get("temperature", 0.0)
        # n_samples_per_case is the configured attempts count.
        attempts = summary.get("n_samples_per_case", 1)

        runs.append({
            "run_id": run_dir.name,
            "timestamp": timestamp,
            "model": model,
            "total": total,
            "passed": passed,
            "avg_score": avg_score,
            "attempts": attempts,
            "temperature": temperature,
            "no_think": no_think,
            "sdks": sorted(sdks),
        })
    return runs


def _load_leaderboard(cases: list[dict]) -> tuple[list[str], list[dict]]:
    """Aggregate run results into a per-config leaderboard.

    A leaderboard row is identified by the tuple (model, temperature,
    no_think, attempts) — the same model run with different parameters is a
    distinct row. Multiple runs sharing that config are merged: for each case
    the most recent run wins.

    Coverage per SDK = distinct cases tested / total cases of that SDK present
    on disk (cases/). The total score is the global pass-rate (passed cases /
    tested cases) across all SDKs.

    @param cases  Discovered case metadata dicts (provides the SDK denominators).
    @return (sdk_list, rows) where sdk_list is every SDK discovered on disk and
            rows is the leaderboard sorted by pass-rate descending.
    """
    # --- denominator: total cases per SDK from discovery ---
    total_by_sdk: dict[str, int] = {}
    for c in cases:
        sdk = c.get("sdk", "")
        if sdk:
            total_by_sdk[sdk] = total_by_sdk.get(sdk, 0) + 1
    sdk_list = sorted(total_by_sdk)

    runs_root = config.RESULTS_DIR / "runs"
    if not runs_root.is_dir():
        return sdk_list, []

    # config_key -> {meta, cases: {case_id: {passed, sdk}}}
    groups: dict[tuple, dict] = {}

    # Iterate ascending so later runs overwrite earlier ones per case.
    for run_dir in sorted(runs_root.iterdir()):
        summary_file = run_dir / "summary.json"
        if not summary_file.is_file():
            continue
        try:
            summary = json.loads(summary_file.read_text(encoding="utf-8"))
        except Exception:
            continue

        model = summary.get("model", "")
        if model == "mock" or not model:
            continue

        gen_params = summary.get("generation_params", {})
        no_think = bool(gen_params.get("no_think", False))
        temperature = float(summary.get("temperature", 0.0))
        attempts = int(summary.get("n_samples_per_case", 1))
        key = (model, temperature, no_think, attempts)

        group = groups.setdefault(key, {
            "model": model,
            "temperature": temperature,
            "no_think": no_think,
            "attempts": attempts,
            "cases": {},
        })

        details_dir = run_dir / "details"
        if not details_dir.is_dir():
            continue
        for f in details_dir.glob("*.json"):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            case_id = d.get("case_id") or f.stem
            group["cases"][case_id] = {
                "passed": bool(d.get("passed")),
                "sdk": d.get("sdk", ""),
            }

    rows: list[dict] = []
    for group in groups.values():
        tested_by_sdk: dict[str, int] = {}
        tested_total = 0
        passed_total = 0
        for info in group["cases"].values():
            tested_total += 1
            if info["passed"]:
                passed_total += 1
            sdk = info["sdk"]
            if sdk:
                tested_by_sdk[sdk] = tested_by_sdk.get(sdk, 0) + 1

        coverage: dict[str, tuple[int, int]] = {}
        for sdk in sdk_list:
            coverage[sdk] = (tested_by_sdk.get(sdk, 0), total_by_sdk[sdk])

        pass_rate = passed_total / tested_total if tested_total else 0.0
        rows.append({
            "model": group["model"],
            "temperature": group["temperature"],
            "no_think": group["no_think"],
            "attempts": group["attempts"],
            "coverage": coverage,
            "tested_total": tested_total,
            "passed_total": passed_total,
            "pass_rate": pass_rate,
        })

    rows.sort(key=lambda r: r["pass_rate"], reverse=True)
    return sdk_list, rows





def _score_bar(score: float, width: int = 8) -> str:
    """Return a simple ASCII progress bar for a [0,1] score."""
    filled = round(score * width)
    return "█" * filled + "░" * (width - filled)
