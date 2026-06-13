"""EmbedEval results dashboard.

Lightweight FastAPI web app that reads results/ and cases/ directly —
no database, no build step. Start with:
    uv run embedeval dashboard
Then open http://localhost:7860.
"""

import difflib
import json
from pathlib import Path
from urllib.parse import quote

import yaml
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI(title="EmbedEval Dashboard")

# Resolved at startup by the CLI command.
RESULTS_DIR: Path = Path("results")
CASES_DIR: Path = Path("cases")

# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------

def _load_runs() -> list[dict]:
    """Return all runs sorted newest-first, each with their detail files."""
    runs_root = RESULTS_DIR / "runs"
    if not runs_root.is_dir():
        return []
    runs = []
    for run_dir in sorted(runs_root.iterdir(), reverse=True):
        if not run_dir.is_dir():
            continue
        details_dir = run_dir / "details"
        cases = []
        if details_dir.is_dir():
            for detail_file in sorted(details_dir.glob("*.json")):
                try:
                    cases.append(json.loads(detail_file.read_text()))
                except Exception:
                    pass
        runs.append({"run_id": run_dir.name, "cases": cases})
    return runs


def _all_results() -> list[dict]:
    """Flatten all detail JSONs from all runs into a single list."""
    results = []
    for run in _load_runs():
        results.extend(run["cases"])
    return results


def _find_reference(case_id: str) -> str | None:
    """Find the reference main.c for a given case_id."""
    for sdk_dir in CASES_DIR.iterdir():
        if not sdk_dir.is_dir():
            continue
        ref = sdk_dir / case_id / "reference" / "main.c"
        if ref.is_file():
            return ref.read_text()
    return None


def _find_metadata(case_id: str) -> dict:
    """Load metadata.yaml for a case, return empty dict if missing."""
    for sdk_dir in CASES_DIR.iterdir():
        if not sdk_dir.is_dir():
            continue
        meta = sdk_dir / case_id / "metadata.yaml"
        if meta.is_file():
            try:
                return yaml.safe_load(meta.read_text()) or {}
            except Exception:
                return {}
    return {}


def _find_prompt(case_id: str) -> str | None:
    """Load prompt.md for a case."""
    for sdk_dir in CASES_DIR.iterdir():
        if not sdk_dir.is_dir():
            continue
        prompt = sdk_dir / case_id / "prompt.md"
        if prompt.is_file():
            return prompt.read_text()
    return None


def _find_case_dir(case_id: str) -> Path | None:
    """Return the case directory Path, or None if not found."""
    for sdk_dir in CASES_DIR.iterdir():
        if not sdk_dir.is_dir():
            continue
        candidate = sdk_dir / case_id
        if candidate.is_dir():
            return candidate
    return None


def _all_cases() -> list[dict]:
    """Return all cases sorted by sdk then case_id, with their metadata."""
    cases = []
    if not CASES_DIR.is_dir():
        return cases
    for sdk_dir in sorted(CASES_DIR.iterdir()):
        if not sdk_dir.is_dir():
            continue
        for case_dir in sorted(sdk_dir.iterdir()):
            if not case_dir.is_dir():
                continue
            meta_file = case_dir / "metadata.yaml"
            if not meta_file.is_file():
                continue
            try:
                meta = yaml.safe_load(meta_file.read_text()) or {}
            except Exception:
                meta = {}
            meta["_case_id"] = case_dir.name
            cases.append(meta)
    return cases


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

_BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
       background: #0f1117; color: #e2e8f0; font-size: 14px; }
a { color: #63b3ed; text-decoration: none; }
a:hover { text-decoration: underline; }
h1 { font-size: 1.4rem; font-weight: 600; }
h2 { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.75rem; }
h3 { font-size: 0.95rem; font-weight: 600; margin-bottom: 0.5rem; color: #a0aec0; }
.desc { color: #a0aec0; font-size: 0.85rem; line-height: 1.5;
        margin-bottom: 1rem; max-width: 80ch; }
.desc strong { color: #e2e8f0; }
.nav { background: #1a1d2e; padding: 0.75rem 1.5rem;
       display: flex; align-items: center; gap: 2rem;
       border-bottom: 1px solid #2d3748; }
.nav a { color: #a0aec0; font-size: 0.9rem; }
.nav a:hover { color: #e2e8f0; text-decoration: none; }
.container { padding: 1.5rem; max-width: 1600px; margin: 0 auto; }
.card { background: #1a1d2e; border: 1px solid #2d3748;
        border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 4px;
         font-size: 0.75rem; font-weight: 600; }
.badge-pass { background: #22543d; color: #68d391; }
.badge-fail { background: #742a2a; color: #fc8181; }
.badge-skip { background: #2d3748; color: #718096; }
.badge-medium { background: #744210; color: #f6ad55; }
.badge-hard { background: #742a2a; color: #fc8181; }
.badge-easy { background: #1a365d; color: #63b3ed; }
.badge-error { background: #2d2a1a; color: #e9c46a; }
table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
th { background: #2d3748; padding: 0.6rem 0.75rem; text-align: left;
     font-weight: 600; color: #a0aec0; white-space: nowrap; }
td { padding: 0.5rem 0.75rem; border-bottom: 1px solid #2d3748; }
tr:hover td { background: #252840; }
.cell-pass { background: #1a3a2a; color: #68d391; text-align: center;
             font-weight: 600; font-size: 0.8rem; }
.cell-fail { background: #3a1a1a; color: #fc8181; text-align: center;
             font-weight: 600; font-size: 0.8rem; }
.cell-none { background: #1a1d2e; color: #4a5568; text-align: center;
             font-size: 0.8rem; }
pre { background: #0d1117; border: 1px solid #2d3748; border-radius: 6px;
      padding: 1rem; overflow-x: auto; font-size: 0.8rem;
      line-height: 1.5; white-space: pre; }
pre.hljs-wrap { background: transparent; border: none; padding: 0; }
pre.hljs-wrap code.hljs { border-radius: 6px; font-size: 0.8rem;
                           line-height: 1.5; display: block; }
.diff-add { background: #1a3a2a; color: #68d391; display: block; }
.diff-del { background: #3a1a1a; color: #fc8181; display: block; }
.diff-ctx { display: block; color: #718096; }
.diff-hdr { display: block; color: #63b3ed; background: #1a2744; }
.split { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.check-row { display: flex; align-items: flex-start; gap: 0.75rem;
             padding: 0.5rem 0; border-bottom: 1px solid #2d3748; }
.check-row:last-child { border-bottom: none; }
.check-name { font-family: monospace; font-size: 0.8rem; flex: 1; }
.check-detail { font-size: 0.75rem; color: #718096; margin-top: 2px; }
.check-detail span { color: #fc8181; }
.tag { display: inline-block; background: #2d3748; color: #a0aec0;
       padding: 1px 6px; border-radius: 3px; font-size: 0.7rem;
       margin: 1px; }
.score-bar { display: inline-block; height: 14px; border-radius: 4px;
             background: #3a3f55; width: 90px; vertical-align: middle;
             overflow: hidden; position: relative; }
.score-fill { display: block; height: 100%; position: absolute; top: 0; left: 0; }
"""

_NAV = """
<nav class="nav">
  <h1>EmbedEval</h1>
  <a href="/">Leaderboard</a>
  <a href="/analysis">Analysis</a>
  <a href="/report">Report</a>
  <a href="/cases">Cases</a>
  <a href="/history">Run History</a>
  <a href="/docs/layers">Docs</a>
  <a href="/docs/models">Models</a>
</nav>
"""


_HLJS_HEAD = """
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github-dark.min.css">
  <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js"></script>
  <script>document.addEventListener('DOMContentLoaded', () => hljs.highlightAll());</script>"""


def _page(title: str, body: str, highlight: bool = False) -> str:
    hljs = _HLJS_HEAD if highlight else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — EmbedEval</title>
  <style>{_BASE_CSS}</style>
{hljs}
</head>
<body>
{_NAV}
<div class="container">
{body}
</div>
</body>
</html>"""


def _recompute_total_score(result: dict, applicable: set[int]) -> float:
    """Recompute total_score using the fixed-denominator method.

    Denominator = applicable layer set (computed across all attempts for the case).
    Skipped layers that are in the applicable set contribute 0 to the numerator.
    Corrects stale values in old JSON files computed with a different formula.
    """
    if not applicable:
        return result.get("total_score", 0.0)
    layers = result.get("layers") or []
    score_by_layer: dict[int, float] = {}
    for ly in layers:
        ln = ly.get("layer")
        if ln not in applicable:
            continue
        error = ly.get("error") or ""
        if error.startswith("Skipped:"):
            score_by_layer[ln] = 0.0
        else:
            score_by_layer[ln] = ly.get("score", 0.0)
    # Layers not present in the JSON at all default to 0.
    total = sum(score_by_layer.get(ln, 0.0) for ln in applicable)
    return total / len(applicable)


def _consistency_score(scores: list[float]) -> float | None:
    """Compute consistency as 1 - CV (coefficient of variation).

    Returns None when fewer than 5 attempts are available (not enough data).
    Returns 1.0 when mean == 0 (model consistently scores zero — perfectly
    consistent in its failure).
    Returns max(0.0, 1 - std/mean) otherwise, clamped to [0, 1].
    """
    if len(scores) < 5:
        return None
    mean = sum(scores) / len(scores)
    if mean == 0.0:
        return 1.0
    variance = sum((s - mean) ** 2 for s in scores) / len(scores)
    std = variance ** 0.5
    return max(0.0, 1.0 - std / mean)


def _result_status(r: dict) -> str:
    """Derive 'pass' | 'fail' | 'error' from a result dict without touching saved JSON.

    - pass:  passed == True
    - error: generated_code is empty AND output_tokens == 0 (infra failure, not model's fault)
    - fail:  everything else (model produced prose, bad code, failed checks)
    """
    if r.get("passed"):
        return "pass"
    if not r.get("generated_code", "").strip():
        output_tokens = r.get("token_usage", {}).get("output_tokens", 0)
        if output_tokens == 0:
            return "error"
    return "fail"


def _status_badge(r: dict) -> str:
    status = _result_status(r)
    if status == "pass":
        return '<span class="badge badge-pass">PASS</span>'
    if status == "error":
        return '<span class="badge badge-error">ERROR</span>'
    return '<span class="badge badge-fail">FAIL</span>'


def _pass_badge(passed: bool) -> str:
    cls = "badge-pass" if passed else "badge-fail"
    label = "PASS" if passed else "FAIL"
    return f'<span class="badge {cls}">{label}</span>'


def _score_bar(score: float) -> str:
    """Render a coloured progress bar. Does NOT include the percentage text."""
    pct = int(score * 100)
    color = "#68d391" if score >= 0.8 else "#f6ad55" if score >= 0.5 else "#fc8181"
    return (
        f'<span class="score-bar">'
        f'<span class="score-fill" style="width:{pct}%;background:{color}"></span>'
        f'</span>'
    )


def _bar_cell(score: float) -> str:
    """Bar + percentage label, suitable for a table cell."""
    pct = int(score * 100)
    return f'{_score_bar(score)} <span style="font-size:0.8rem">{pct}%</span>'


_DASH = '<span style="color:#4a5568;font-size:0.8rem">—</span>'


def _applicable_layers(all_attempts: list[dict]) -> set[int]:
    """Return the set of layer numbers that have real checks for this case.

    A layer is applicable if any attempt actually executed it (not skipped due
    to earlier failure) and produced at least one non-environment-skip check.
    Scanning all attempts finds layers that only some attempts reached.
    """
    applicable: set[int] = set()
    for attempt in all_attempts:
        for ly in (attempt.get("layers") or []):
            layer_num = ly.get("layer")
            if layer_num == 4:
                continue
            error = ly.get("error") or ""
            if error.startswith("Skipped:"):
                continue
            details = ly.get("details") or []
            real = [
                d for d in details
                if not (d.get("check_type") == "environment" and "skipped" in str(d.get("actual", "")))
            ]
            if real:
                applicable.add(layer_num)
    return applicable


def _layer_score_cell(case: dict, layer_num: int, applicable: set[int]) -> str:
    """Return a table cell with the score for a specific layer.

    Shows '—' when the layer is not applicable for this case (no check files).
    Shows 0% when the layer exists but was skipped due to earlier failure.
    Shows a bar when the layer was executed.
    """
    if layer_num not in applicable:
        return _DASH

    for ly in (case.get("layers") or []):
        if ly.get("layer") != layer_num:
            continue
        error = ly.get("error") or ""
        # Layer exists but was skipped → 0%. Ignore stored score value
        # (old runs had 1.0 as default for skipped layers).
        if error.startswith("Skipped:"):
            return _bar_cell(0.0)
        return _bar_cell(ly.get("score", 0.0))
    return _DASH


def _diff_html(a: str, b: str, fromfile: str = "reference", tofile: str = "generated") -> str:
    """Return unified diff as HTML with syntax coloring."""
    # Normalize line endings and trailing whitespace so \r\n vs \n or a
    # missing final newline don't produce spurious diff lines.
    a_lines = [ln + "\n" for ln in a.strip().splitlines()]
    b_lines = [ln + "\n" for ln in b.strip().splitlines()]
    diff = difflib.unified_diff(a_lines, b_lines, fromfile=fromfile, tofile=tofile, lineterm="")
    parts = []
    for line in diff:
        esc = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if line.startswith("+++") or line.startswith("---"):
            parts.append(f'<span class="diff-hdr">{esc}</span>')
        elif line.startswith("@@"):
            parts.append(f'<span class="diff-hdr">{esc}</span>')
        elif line.startswith("+"):
            parts.append(f'<span class="diff-add">{esc}</span>')
        elif line.startswith("-"):
            parts.append(f'<span class="diff-del">{esc}</span>')
        else:
            parts.append(f'<span class="diff-ctx">{esc}</span>')
    if not parts:
        return '<span style="color:#68d391">No differences — generated matches reference exactly.</span>'
    return "".join(parts)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

_DIFFICULTIES = ["easy", "medium", "hard"]


def _latest_attempt_lookup(results: list[dict]) -> dict[tuple[str, str], dict]:
    """Build (case_id, model) → latest-attempt result from a flat result list."""
    lookup: dict[tuple[str, str], dict] = {}
    for r in results:
        key = (r.get("case_id", ""), r.get("model", ""))
        if key not in lookup or r.get("attempt", 0) > lookup[key].get("attempt", 0):
            lookup[key] = r
    return lookup


def _model_leaderboard_stats(
    lookup: dict[tuple[str, str], dict],
) -> tuple[list[str], dict[str, dict], dict[str, str]]:
    """Compute per-model leaderboard stats from a latest-attempt lookup.

    Returns (sorted_models, model_stats, case_difficulty). Shared by the global
    leaderboard and the Analysis page so the scoring logic lives in one place.
    ERROR results (infra failures, output_tokens==0) are excluded from pass-rate
    and coverage so they don't penalise the model unfairly.
    """
    models: list[str] = []
    seen_models: set[str] = set()
    for (_, m) in lookup:
        if m and m not in seen_models:
            models.append(m)
            seen_models.add(m)

    case_difficulty: dict[str, str] = {}
    for (case_id, _) in lookup:
        if case_id not in case_difficulty:
            case_difficulty[case_id] = _find_metadata(case_id).get("difficulty", "unknown")

    def _bucket_stats(model: str, difficulty: str) -> dict:
        bucket = [
            r for (cid, m), r in lookup.items()
            if m == model and case_difficulty.get(cid) == difficulty
        ]
        scorable = [r for r in bucket if _result_status(r) != "error"]
        errors = len(bucket) - len(scorable)
        total = len(scorable)
        passed = sum(1 for r in scorable if r.get("passed"))
        pct = int(passed / total * 100) if total else 0
        return {"passed": passed, "total": total, "errors": errors, "pct": pct}

    model_stats: dict[str, dict] = {}
    for model in models:
        all_for_model = [r for (_, m), r in lookup.items() if m == model]
        scorable = [r for r in all_for_model if _result_status(r) != "error"]
        errors = len(all_for_model) - len(scorable)
        total = len(scorable)
        passed = sum(1 for r in scorable if r.get("passed"))
        pct = int(passed / total * 100) if total else 0
        coverage = (
            sum(r.get("total_score", 0.0) for r in scorable) / total if total else 0.0
        )
        avg_duration = (
            sum(r.get("duration_seconds", 0.0) for r in scorable) / total if total else 0.0
        )
        model_stats[model] = {
            "passed": passed, "total": total, "errors": errors, "pct": pct,
            "coverage": coverage,
            "avg_duration": avg_duration,
            "buckets": {d: _bucket_stats(model, d) for d in _DIFFICULTIES},
        }

    models = sorted(
        models,
        key=lambda m: (model_stats[m]["pct"], model_stats[m]["coverage"]),
        reverse=True,
    )
    return models, model_stats, case_difficulty


def _leaderboard_table(
    models: list[str],
    model_stats: dict[str, dict],
    review_sdk: str = "",
    consistency_by_model: dict[str, float | None] | None = None,
    link_filters: dict[str, str] | None = None,
) -> str:
    """Render the shared models×difficulty leaderboard table HTML.

    review_sdk, when set, is forwarded into the per-model review links so the
    review view opens pre-filtered to the same SDK bucket.

    consistency_by_model, when provided, replaces the infra-only "Errors" column
    with a per-model "Consistency" column (1-CV averaged over cases with ≥5
    attempts; None → n/a). Used by the Analysis page.

    link_filters, when provided (Analysis page only), turns the pass@1 cell and
    each difficulty bucket cell into drill-down links to /review, carrying the
    active filters so the user lands on that model's matching cases. The keys
    are query params (category/sdk/difficulty); the difficulty bucket cells
    additionally pin difficulty to their own column.
    """
    show_consistency = consistency_by_model is not None
    drill = link_filters is not None

    def _review_link(model: str, extra: dict[str, str]) -> str:
        params = {"model": model}
        if link_filters:
            params.update({k: v for k, v in link_filters.items() if v})
        params.update(extra)
        return "/review?" + "&".join(
            f"{k}={quote(v, safe='')}" for k, v in params.items() if v
        )

    fifth_header = "Consistency" if show_consistency else "Errors"
    diff_headers = "".join(
        f'<th style="text-align:center"><span class="badge badge-{d}">{d.capitalize()}</span></th>'
        for d in _DIFFICULTIES
    )
    header_cells = (
        f"<th>Model</th><th>pass@1</th><th>check coverage</th><th>avg time</th>"
        f"<th>Passed</th><th>{fifth_header}</th>{diff_headers}"
    )

    rows = ""
    for model in models:
        s = model_stats[model]
        short = model.split("/")[-1]
        dur = s["avg_duration"]
        dur_str = f"{dur:.1f}s" if dur < 60 else f"{dur/60:.1f}m"
        dur_color = "#68d391" if dur < 10 else "#f6ad55" if dur < 30 else "#fc8181"
        review_url = f"/review?model={quote(model, safe='')}"
        if review_sdk:
            review_url += f"&sdk={quote(review_sdk, safe='')}"
        if show_consistency:
            cons = consistency_by_model.get(model)
            if cons is None:
                fifth_cell = '<td style="text-align:center;color:#4a5568;font-size:0.8rem">n/a</td>'
            else:
                fifth_cell = f'<td>{_bar_cell(cons)}</td>'
        else:
            errors = s["errors"]
            errors_cell = (
                f'<span class="badge badge-error">{errors}</span>'
                if errors > 0
                else '<span style="color:#4a5568">—</span>'
            )
            fifth_cell = f"<td style='text-align:center'>{errors_cell}</td>"
        # pass@1 cell: drill into all matching cases for this model when filtered.
        passrate_bar = _bar_cell(s['passed'] / s['total'] if s['total'] else 0)
        if drill and s['total']:
            passrate_cell = f"<td><a href='{_review_link(model, {})}'>{passrate_bar}</a></td>"
        else:
            passrate_cell = f"<td>{passrate_bar}</td>"
        row = (
            f"<td title='{model}' style='font-family:monospace;font-size:0.8rem'>"
            f"<a href='{review_url}'>{short}</a></td>"
            f"{passrate_cell}"
            f"<td>{_bar_cell(s['coverage'])}</td>"
            f"<td style='color:{dur_color};font-variant-numeric:tabular-nums'>{dur_str}</td>"
            f"<td style='color:#a0aec0'>{s['passed']}/{s['total']}</td>"
            f"{fifth_cell}"
        )
        for diff in _DIFFICULTIES:
            b = s["buckets"][diff]
            if b["total"] == 0:
                row += "<td class='cell-none' style='text-align:center'>—</td>"
            else:
                color_cls = "cell-pass" if b["pct"] >= 60 else "cell-fail"
                cell_inner = (
                    f"{b['pct']}% <span style='font-weight:normal;font-size:0.75rem'>"
                    f"({b['passed']}/{b['total']})</span>"
                )
                # Drill into this model's cases for this specific difficulty.
                if drill:
                    href = _review_link(model, {"difficulty": diff})
                    cell_inner = f"<a href='{href}'>{cell_inner}</a>"
                row += f"<td class='{color_cls}'>{cell_inner}</td>"
        rows += f"<tr>{row}</tr>"

    return f"""
<div class="card" style="padding:0;overflow:auto;margin-top:1rem">
  <table>
    <thead><tr>{header_cells}</tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>"""


def _consistency_by_model(results: list[dict]) -> dict[str, float | None]:
    """Per-model consistency averaged over its cases with ≥5 attempts.

    Groups the raw (all-attempt) results by model then case_id, computes 1-CV
    per case via _consistency_score, and averages the non-None values.
    Returns None for a model when no case reached 5 attempts.
    """
    by_model: dict[str, dict[str, list[dict]]] = {}
    for r in results:
        model = r.get("model", "")
        cid = r.get("case_id", "")
        by_model.setdefault(model, {}).setdefault(cid, []).append(r)

    out: dict[str, float | None] = {}
    for model, cases_by_id in by_model.items():
        applicable = {
            cid: _applicable_layers(attempts) for cid, attempts in cases_by_id.items()
        }
        vals = [
            v for v in (
                _consistency_score([
                    _recompute_total_score(c, applicable.get(cid, set()))
                    for c in attempts
                ])
                for cid, attempts in cases_by_id.items()
            )
            if v is not None
        ]
        out[model] = sum(vals) / len(vals) if vals else None
    return out


def _filter_select(values: set[str], current: str, param: str) -> str:
    """Render a submit-on-change <select> for a single filter param."""
    opts = '<option value="">All</option>'
    for v in sorted(values):
        sel = ' selected' if v == current else ''
        opts += f'<option value="{v}"{sel}>{v}</option>'
    return (
        f'<select name="{param}" onchange="this.form.submit()" '
        f'style="background:#2d3748;color:#e2e8f0;border:1px solid #4a5568;'
        f'border-radius:4px;padding:3px 8px;font-size:0.8rem">{opts}</select>'
    )


@app.get("/report", response_class=HTMLResponse)
def report() -> str:
    """Visual benchmark report: aggregated per-model charts (Plotly)."""
    from embedeval.report import generate_report_body

    # include_plotly_js=True: the dashboard pages do not otherwise load plotly.
    body = generate_report_body(RESULTS_DIR, include_plotly_js=True,
                                cases_dir=CASES_DIR)
    return _page("Report", body)


@app.get("/", response_class=HTMLResponse)
def leaderboard(request: Request) -> str:
    """Leaderboard: rows=models, columns=difficulty buckets (easy/medium/hard).

    Optional query params:
      ?sdk=zephyr        — filter by SDK bucket
      ?difficulty=medium — filter by difficulty
    Both can be combined: ?sdk=zephyr&difficulty=medium
    """
    filter_sdk = request.query_params.get("sdk", "")
    filter_diff = request.query_params.get("difficulty", "")

    all_results = _all_results()

    if not all_results:
        return _page("Leaderboard", "<div class='card'><p>No results found in results/. Run a benchmark first.</p></div>")

    # Collect available sdk and difficulty values across all results (for filter UI)
    all_sdks: set[str] = set()
    all_diffs: set[str] = set()
    for r in all_results:
        meta = _find_metadata(r.get("case_id", ""))
        sdk = meta.get("sdk", "")
        if sdk:
            all_sdks.add(sdk)
        d = meta.get("difficulty", "")
        if d:
            all_diffs.add(d)

    # Apply filters
    results = all_results
    if filter_sdk:
        results = [r for r in results if _find_metadata(r.get("case_id", "")).get("sdk") == filter_sdk]
    if filter_diff:
        results = [r for r in results if _find_metadata(r.get("case_id", "")).get("difficulty") == filter_diff]

    # Build lookup, then compute shared per-model stats.
    lookup = _latest_attempt_lookup(results)
    models, model_stats, case_difficulty = _model_leaderboard_stats(lookup)

    filter_form = f"""
<form method="get" style="display:flex;align-items:center;gap:1rem;font-size:0.85rem;color:#a0aec0">
  <span>SDK: {_filter_select(all_sdks, filter_sdk, "sdk")}</span>
  <span>Difficulty: {_filter_select(all_diffs, filter_diff, "difficulty")}</span>
</form>"""

    table_html = _leaderboard_table(models, model_stats, review_sdk=filter_sdk)

    # Case count per difficulty for the subtitle
    diff_counts = {d: sum(1 for v in case_difficulty.values() if v == d) for d in _DIFFICULTIES}
    subtitle_parts = [f"{diff_counts[d]} {d}" for d in _DIFFICULTIES if diff_counts[d] > 0]

    no_results_msg = ""
    if not models:
        no_results_msg = "<p style='color:#718096;padding:1rem'>No results match the selected filters.</p>"

    body = f"""
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;flex-wrap:wrap;gap:0.75rem">
  <h1>Leaderboard</h1>
  <span style="color:#718096;font-size:0.85rem">{len(models)} models · {sum(diff_counts.values())} cases ({", ".join(subtitle_parts) or "none"})</span>
</div>
{filter_form}
{table_html if models else "<div class='card' style='margin-top:1rem'>" + no_results_msg + "</div>"}
"""
    return _page("Leaderboard", body)


@app.get("/analysis", response_class=HTMLResponse)
def analysis(request: Request) -> str:
    """Analysis page: build a leaderboard scoped to a filtered subset of cases.

    Starts with category filtering (e.g. zephyr kconfig) plus SDK and difficulty,
    all combinable. More analysis types will be added here over time.

    Optional query params:
      ?category=kconfig   — filter by case category
      ?sdk=zephyr         — filter by SDK bucket
      ?difficulty=medium  — filter by difficulty
    """
    filter_category = request.query_params.get("category", "")
    filter_sdk = request.query_params.get("sdk", "")
    filter_diff = request.query_params.get("difficulty", "")

    all_results = _all_results()
    if not all_results:
        return _page(
            "Analysis",
            "<div class='card'><p>No results found in results/. Run a benchmark first.</p></div>",
        )

    # Collect available filter values across all results (for the filter UI).
    all_categories: set[str] = set()
    all_sdks: set[str] = set()
    all_diffs: set[str] = set()
    for r in all_results:
        meta = _find_metadata(r.get("case_id", ""))
        if meta.get("category"):
            all_categories.add(meta["category"])
        if meta.get("sdk"):
            all_sdks.add(meta["sdk"])
        if meta.get("difficulty"):
            all_diffs.add(meta["difficulty"])

    # Apply filters. Each narrows the result set by the matching metadata field.
    results = all_results
    if filter_category:
        results = [r for r in results if _find_metadata(r.get("case_id", "")).get("category") == filter_category]
    if filter_sdk:
        results = [r for r in results if _find_metadata(r.get("case_id", "")).get("sdk") == filter_sdk]
    if filter_diff:
        results = [r for r in results if _find_metadata(r.get("case_id", "")).get("difficulty") == filter_diff]

    lookup = _latest_attempt_lookup(results)
    models, model_stats, _ = _model_leaderboard_stats(lookup)
    n_cases = len({cid for (cid, _) in lookup})

    filter_form = f"""
<form method="get" style="display:flex;align-items:center;gap:1rem;font-size:0.85rem;color:#a0aec0;flex-wrap:wrap">
  <span>Category: {_filter_select(all_categories, filter_category, "category")}</span>
  <span>SDK: {_filter_select(all_sdks, filter_sdk, "sdk")}</span>
  <span>Difficulty: {_filter_select(all_diffs, filter_diff, "difficulty")}</span>
</form>"""

    active = [
        f"category={filter_category}" if filter_category else "",
        f"sdk={filter_sdk}" if filter_sdk else "",
        f"difficulty={filter_diff}" if filter_diff else "",
    ]
    active_str = " · ".join(p for p in active if p) or "no filters (all cases)"

    if models:
        # Consistency needs all attempts, so compute it from the raw filtered
        # results rather than the latest-attempt lookup.
        consistency_by_model = _consistency_by_model(results)
        content = _leaderboard_table(
            models, model_stats, review_sdk=filter_sdk,
            consistency_by_model=consistency_by_model,
            link_filters={
                "category": filter_category,
                "sdk": filter_sdk,
                "difficulty": filter_diff,
            },
        )
    else:
        content = "<div class='card' style='margin-top:1rem'><p style='color:#718096;padding:1rem'>No results match the selected filters.</p></div>"

    body = f"""
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;flex-wrap:wrap;gap:0.75rem">
  <h1>Analysis</h1>
  <span style="color:#718096;font-size:0.85rem">{len(models)} models · {n_cases} cases · {active_str}</span>
</div>
<p class="desc">
  Slice the benchmark by metadata and rank models on just that subset.
  Example: pick category <strong>kconfig</strong> and SDK <strong>zephyr</strong> to
  compare models on Zephyr Kconfig cases only. More analysis types coming.
</p>
{filter_form}
{content}
"""
    return _page("Analysis", body)


@app.get("/case/{case_id}", response_class=HTMLResponse)
def case_overview(case_id: str) -> str:
    """All model results for a single case."""
    results = [r for r in _all_results() if r.get("case_id") == case_id]
    if not results:
        raise HTTPException(status_code=404, detail=f"No results for case {case_id}")

    meta = _find_metadata(case_id)
    prompt = _find_prompt(case_id)

    tags = " ".join(f'<span class="tag">{t}</span>' for t in meta.get("tags", []))
    diff = meta.get("difficulty", "")
    diff_badge = f'<span class="badge badge-{diff}">{diff}</span>' if diff else ""

    rows = ""
    seen: dict[str, dict] = {}
    for r in results:
        m = r.get("model", "")
        if m not in seen or r.get("attempt", 0) > seen[m].get("attempt", 0):
            seen[m] = r

    for model, r in seen.items():
        short = model.split("/")[-1]
        passed = _pass_badge(r.get("passed", False))
        score = _bar_cell(r.get("total_score", 0))
        layer = r.get("failed_at_layer")
        layer_str = f"L{layer}" if layer is not None else "—"
        rows += f"""<tr>
          <td><a href="/case/{case_id}/{model}">{short}</a></td>
          <td>{passed}</td>
          <td>{score}</td>
          <td style="color:#718096">{layer_str}</td>
          <td style="color:#718096">{r.get('attempt',1)}</td>
        </tr>"""

    prompt_html = ""
    if prompt:
        esc = prompt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        prompt_html = f'<div class="card"><h2>Prompt</h2><pre style="background:transparent;border:none;padding:0">{esc}</pre></div>'

    body = f"""
<div style="margin-bottom:1rem">
  <a href="/" style="color:#718096;font-size:0.85rem">← Leaderboard</a>
</div>
<div class="card">
  <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.75rem">
    <h1>{case_id}</h1>
    {diff_badge}
    <span style="color:#718096;font-size:0.85rem">{meta.get('category','')}</span>
  </div>
  <p style="color:#a0aec0;margin-bottom:0.75rem">{meta.get('description','')}</p>
  <div>{tags}</div>
</div>
{prompt_html}
<div class="card" style="padding:0;overflow:auto">
  <table>
    <thead><tr><th>Model</th><th>Result</th><th>Score</th><th>Failed at</th><th>Attempt</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>
"""
    return _page(case_id, body)


@app.get("/case/{case_id}/{model:path}", response_class=HTMLResponse)
def case_detail(case_id: str, model: str) -> str:
    """Detailed view: checks + diff for a specific case+model."""
    all_results = [
        r for r in _all_results()
        if r.get("case_id") == case_id and r.get("model") == model
    ]
    if not all_results:
        raise HTTPException(status_code=404, detail=f"No results for {case_id} / {model}")

    # Use the latest attempt
    result = max(all_results, key=lambda r: r.get("attempt", 1))
    reference = _find_reference(case_id)
    generated = result.get("generated_code", "")
    meta = _find_metadata(case_id)

    # --- checks table ---
    checks_html = ""
    for layer in result.get("layers", []):
        layer_name = layer.get("name", "")
        layer_passed = layer.get("passed", False)
        layer_error = layer.get("error")
        details = layer.get("details", [])
        layer_score = layer.get("score")

        badge = _pass_badge(layer_passed)
        score_pct = f'<span style="font-size:0.8rem;color:#718096;margin-left:0.5rem">{int(layer_score * 100)}%</span>' if layer_score is not None and details else ""
        checks_html += f'<div style="margin-bottom:1rem"><h3>L{layer["layer"]} — {layer_name} {badge}{score_pct}</h3>'

        if layer_error and not details:
            checks_html += f'<p style="color:#718096;font-size:0.8rem;padding:0.5rem 0">{layer_error}</p>'
        else:
            for chk in details:
                icon = "✓" if chk["passed"] else "✗"
                color = "#68d391" if chk["passed"] else "#fc8181"
                name = chk.get("check_name", "")
                actual = chk.get("actual", "")
                expected = chk.get("expected", "")
                detail_html = ""
                if not chk["passed"]:
                    act_esc = str(actual).replace("<", "&lt;")
                    exp_esc = str(expected).replace("<", "&lt;")
                    detail_html = f'<div class="check-detail">expected: {exp_esc}<br>actual: <span>{act_esc}</span></div>'
                checks_html += f"""
<div class="check-row">
  <span style="color:{color};font-weight:bold;font-size:1rem;min-width:1.2rem">{icon}</span>
  <div class="check-name">{name}{detail_html}</div>
</div>"""
        checks_html += "</div>"

    # --- diff ---
    if reference:
        diff_content = _diff_html(reference, generated, fromfile="reference/main.c", tofile="generated")
        diff_section = f'<pre>{diff_content}</pre>'
    else:
        ref_esc = ""
        diff_section = "<p style='color:#718096'>No reference found for this case.</p>"

    # --- raw code panels ---
    ref_esc = (reference or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    gen_esc = generated.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    model_short = model.split("/")[-1]
    diff = meta.get("difficulty", "")
    diff_badge = f'<span class="badge badge-{diff}">{diff}</span>' if diff else ""
    overall = _pass_badge(result.get("passed", False))

    body = f"""
<div style="margin-bottom:1rem">
  <a href="/case/{case_id}" style="color:#718096;font-size:0.85rem">← {case_id}</a>
</div>
<div class="card">
  <div style="display:flex;align-items:center;gap:1rem">
    <h1>{case_id}</h1>
    {diff_badge}
    {overall}
    <span style="color:#a0aec0">· {model_short}</span>
    <span style="color:#718096;font-size:0.8rem">attempt {result.get('attempt',1)}</span>
  </div>
</div>

<div class="split">

  <div>
    <div class="card">
      <h2>Checks</h2>
      {checks_html}
    </div>
  </div>

  <div>
    <div class="card">
      <h2>Diff (reference → generated)</h2>
      {diff_section}
    </div>
    <div class="card" style="margin-top:1rem">
      <h2>Code side-by-side</h2>
      <div class="split" style="gap:0.5rem">
        <div>
          <h3>Reference</h3>
          <pre class="hljs-wrap"><code class="language-c">{ref_esc}</code></pre>
        </div>
        <div>
          <h3>Generated</h3>
          <pre class="hljs-wrap"><code class="language-c">{gen_esc}</code></pre>
        </div>
      </div>
    </div>
  </div>

</div>
"""
    return _page(f"{case_id} / {model_short}", body, highlight=True)


@app.get("/review", response_class=HTMLResponse)
def review(request: Request) -> str:
    """Human review view: all cases for a given model + optional filters.

    Query params:
      ?model=groq/llama-3.3-70b-versatile  — required
      ?sdk=mcuxpresso-sdk                   — optional, narrows by SDK bucket
      ?category=dma                         — optional, narrows by category
      ?difficulty=medium                    — optional, narrows by difficulty

    The category/difficulty filters let the Analysis page drill down from a
    pass-rate cell straight into the matching cases for that model.
    """
    filter_model = request.query_params.get("model", "")
    filter_sdk = request.query_params.get("sdk", "")
    filter_category = request.query_params.get("category", "")
    filter_diff = request.query_params.get("difficulty", "")

    if not filter_model:
        return _page("Review", "<div class='card'><p>No model selected. Go back to <a href='/'>Leaderboard</a> and click a model name.</p></div>")

    all_results = _all_results()

    # Collect all SDKs available for this model
    model_results = [r for r in all_results if r.get("model") == filter_model]
    if not model_results:
        return _page("Review", f"<div class='card'><p>No results found for model <code>{filter_model}</code>.</p></div>")

    available_sdks: set[str] = set()
    for r in model_results:
        sdk = _find_metadata(r.get("case_id", "")).get("sdk", "")
        if sdk:
            available_sdks.add(sdk)

    # Apply filters (all combinable, matching the Analysis page semantics).
    visible = model_results
    if filter_sdk:
        visible = [r for r in visible if _find_metadata(r.get("case_id", "")).get("sdk") == filter_sdk]
    if filter_category:
        visible = [r for r in visible if _find_metadata(r.get("case_id", "")).get("category") == filter_category]
    if filter_diff:
        visible = [r for r in visible if _find_metadata(r.get("case_id", "")).get("difficulty") == filter_diff]

    # Group all attempts per case (for attempt count + consistency), and keep
    # the latest attempt per case for the summary row.
    attempts_by_case: dict[str, list[dict]] = {}
    for r in visible:
        attempts_by_case.setdefault(r.get("case_id", ""), []).append(r)

    latest: dict[str, dict] = {}
    for r in visible:
        cid = r.get("case_id", "")
        if cid not in latest or r.get("attempt", 0) > latest[cid].get("attempt", 0):
            latest[cid] = r

    # Per-case consistency: 1-CV over recomputed total_scores across attempts.
    # None when fewer than 5 attempts are available (same rule as Run History).
    applicable_by_case = {
        cid: _applicable_layers(atts) for cid, atts in attempts_by_case.items()
    }
    consistency_by_case = {
        cid: _consistency_score([
            _recompute_total_score(c, applicable_by_case.get(cid, set()))
            for c in atts
        ])
        for cid, atts in attempts_by_case.items()
    }

    # Sort by difficulty order then case_id
    _diff_order = {"easy": 0, "medium": 1, "hard": 2, "unknown": 3}
    sorted_cases = sorted(
        latest.values(),
        key=lambda r: (
            _diff_order.get(_find_metadata(r.get("case_id", "")).get("difficulty", "unknown"), 3),
            r.get("case_id", ""),
        ),
    )

    # SDK dropdown
    def _sdk_options() -> str:
        opts = '<option value="">All SDKs</option>'
        for sdk in sorted(available_sdks):
            sel = ' selected' if sdk == filter_sdk else ''
            opts += f'<option value="{sdk}"{sel}>{sdk}</option>'
        return (
            f'<select name="sdk" onchange="this.form.submit()" '
            f'style="background:#2d3748;color:#e2e8f0;border:1px solid #4a5568;'
            f'border-radius:4px;padding:3px 8px;font-size:0.8rem">{opts}</select>'
        )

    # Preserve category/difficulty across the SDK dropdown submit.
    extra_hidden = ""
    if filter_category:
        extra_hidden += f'<input type="hidden" name="category" value="{filter_category}">'
    if filter_diff:
        extra_hidden += f'<input type="hidden" name="difficulty" value="{filter_diff}">'

    filter_form = f"""
<form method="get" style="display:flex;align-items:center;gap:1rem;font-size:0.85rem;color:#a0aec0">
  <input type="hidden" name="model" value="{filter_model}">
  {extra_hidden}
  <span>SDK: {_sdk_options()}</span>
</form>"""

    # Table rows
    rows = ""
    for r in sorted_cases:
        cid = r.get("case_id", "")
        meta = _find_metadata(cid)
        diff = meta.get("difficulty", "—")
        diff_badge = f'<span class="badge badge-{diff}">{diff}</span>' if diff in ("easy", "medium", "hard") else diff
        sdk_label = meta.get("sdk", "—")
        category = meta.get("category", "—")
        title = meta.get("title", "")
        passed_badge = _status_badge(r)
        score = _bar_cell(r.get("total_score", 0)) if _result_status(r) != "error" else '<span style="color:#4a5568;font-size:0.8rem">n/a</span>'
        layer = r.get("failed_at_layer")
        layer_str = f"L{layer}" if layer is not None else "—"
        detail_url = f"/case/{cid}/{filter_model}"

        n_attempts = len(attempts_by_case.get(cid, []))
        consistency = consistency_by_case.get(cid)
        if consistency is None:
            cons_cell = (
                f'<span style="color:#4a5568;font-size:0.8rem" '
                f'title="Needs ≥5 attempts (got {n_attempts})">n/a</span>'
            )
        else:
            cons_cell = f'{_score_bar(consistency)} <span style="font-size:0.8rem">{int(consistency * 100)}%</span>'

        rows += f"""<tr>
          <td><a href="{detail_url}">{cid}</a></td>
          <td style="color:#718096;font-size:0.8rem">{sdk_label}</td>
          <td>{diff_badge}</td>
          <td style="color:#718096;font-size:0.8rem">{category}</td>
          <td style="color:#a0aec0;font-size:0.8rem">{title}</td>
          <td>{passed_badge}</td>
          <td>{score}</td>
          <td style="color:#718096;font-size:0.8rem">{layer_str}</td>
          <td style="color:#718096;font-size:0.8rem;text-align:center">{n_attempts}</td>
          <td>{cons_cell}</td>
        </tr>"""

    scorable = [r for r in sorted_cases if _result_status(r) != "error"]
    errors = len(sorted_cases) - len(scorable)
    total = len(scorable)
    passed = sum(1 for r in scorable if r.get("passed"))
    model_short = filter_model.split("/")[-1]
    errors_summary = (
        f' · <span class="badge badge-error">{errors} error{"s" if errors != 1 else ""}</span>'
        if errors > 0 else ""
    )

    # Show the active drill-down filters and badge each one.
    active_filters = ""
    for label, val in (("category", filter_category), ("sdk", filter_sdk), ("difficulty", filter_diff)):
        if val:
            active_filters += f'<span class="tag">{label}: {val}</span>'

    # Back link points to Analysis when a category/difficulty drill-down is active.
    if filter_category or filter_diff:
        back_href, back_label = "/analysis", "← Analysis"
    else:
        back_href, back_label = "/", "← Leaderboard"

    body = f"""
<div style="margin-bottom:1rem">
  <a href="{back_href}" style="color:#718096;font-size:0.85rem">{back_label}</a>
</div>
<div class="card" style="margin-bottom:1rem">
  <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap">
    <h1 style="font-family:monospace">{model_short}</h1>
    <span style="color:#718096;font-size:0.85rem" title="{filter_model}">{filter_model}</span>
    <span style="color:#718096;font-size:0.85rem">{passed}/{total} passed</span>
    {_bar_cell(passed / total if total else 0)}
    {errors_summary}
    {active_filters}
  </div>
</div>
{filter_form}
<div class="card" style="padding:0;overflow:auto;margin-top:1rem">
  <table>
    <thead><tr>
      <th>Case</th><th>SDK</th><th>Difficulty</th><th>Category</th>
      <th>Title</th><th>Result</th><th>Score</th><th>Failed at</th>
      <th style="text-align:center">Attempts</th><th>Consistency</th>
    </tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>
"""
    return _page(f"Review — {model_short}", body)


@app.get("/history", response_class=HTMLResponse)
def history() -> str:
    """List of all runs with summary stats."""
    runs = _load_runs()
    if not runs:
        return _page("History", "<div class='card'><p>No runs found.</p></div>")

    rows = ""
    for run in runs:
        cases = run["cases"]
        total = len(cases)
        passed = sum(1 for c in cases if c.get("passed"))
        models = list({c.get("model", "") for c in cases if c.get("model")})
        model_tags = " ".join(
            f'<span class="tag">{m.split("/")[-1]}</span>' for m in models
        )
        cases_by_id_hist: dict[str, list[dict]] = {}
        for c in cases:
            cases_by_id_hist.setdefault(c.get("case_id", ""), []).append(c)
        applicable_hist = {
            cid: _applicable_layers(atts) for cid, atts in cases_by_id_hist.items()
        }
        avg_score = sum(
            _recompute_total_score(c, applicable_hist.get(c.get("case_id", ""), set()))
            for c in cases
        ) / total if total else 0.0
        score_bar = _bar_cell(avg_score)
        passed_str = f'<span style="color:#718096;font-size:0.8rem">{passed}/{total}</span>'

        # Total output tokens for the run
        output_tokens = sum(
            c.get("token_usage", {}).get("output_tokens", 0) for c in cases
        )
        tokens_str = f"{output_tokens:,}"

        # A run is complete if every case produced generated_code (non-empty).
        incomplete = sum(1 for c in cases if not c.get("generated_code", "").strip())
        if incomplete == 0:
            status_html = '<span class="badge badge-pass">complete</span>'
        else:
            status_html = f'<span class="badge badge-fail">partial ({total - incomplete}/{total})</span>'

        temperatures = {c.get("temperature", 0.0) for c in cases}
        temp_str = ", ".join(f"{t:.1f}" for t in sorted(temperatures))
        attempts = {c.get("attempt", 1) for c in cases}
        max_attempt = max(attempts) if attempts else 1
        sdks = {c.get("sdk", "") for c in cases if c.get("sdk")}
        sdk_tags = " ".join(f'<span class="tag">{s}</span>' for s in sorted(sdks))

        # Consistency aggregated over cases with ≥5 attempts.
        hist_cases_by_id: dict[str, list[dict]] = {}
        for c in cases:
            hist_cases_by_id.setdefault(c.get("case_id", ""), []).append(c)
        hist_applicable = {
            cid: _applicable_layers(atts) for cid, atts in hist_cases_by_id.items()
        }
        cons_vals = [
            v for v in (
                _consistency_score([
                    _recompute_total_score(c, hist_applicable.get(cid, set()))
                    for c in atts
                ])
                for cid, atts in hist_cases_by_id.items()
            )
            if v is not None
        ]
        if cons_vals:
            cons_avg = sum(cons_vals) / len(cons_vals)
            consistency_cell = f'{_bar_cell(cons_avg)} <span style="font-size:0.75rem;color:#718096">({len(cons_vals)})</span>'
        else:
            consistency_cell = '<span style="color:#4a5568;font-size:0.8rem">n/a</span>'

        rows += f"""<tr>
          <td style="font-family:monospace;font-size:0.8rem">
            <a href="/history/{run['run_id']}">{run['run_id']}</a>
          </td>
          <td>{model_tags}</td>
          <td>{sdk_tags}</td>
          <td style="color:#a0aec0;font-variant-numeric:tabular-nums;text-align:center">{temp_str}</td>
          <td style="color:#a0aec0;text-align:center">{max_attempt}</td>
          <td>{status_html}</td>
          <td style="color:#a0aec0;text-align:right;font-variant-numeric:tabular-nums">{tokens_str}</td>
          <td>{score_bar}</td>
          <td>{passed_str}</td>
          <td>{consistency_cell}</td>
        </tr>"""

    body = f"""
<h1 style="margin-bottom:1rem">Run History</h1>
<div class="card" style="padding:0;overflow:auto">
  <table>
    <thead><tr>
      <th>Run</th><th>Model</th><th>SDKs</th>
      <th style="text-align:center">Temp</th><th style="text-align:center">Att.</th>
      <th>Status</th><th style="text-align:right">Tokens out</th>
      <th>Score</th><th>Passed</th><th>Consistency</th>
    </tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>
"""
    return _page("History", body)


@app.get("/history/{run_id:path}", response_class=HTMLResponse)
def history_detail(run_id: str) -> str:
    """Detail view for a single run: checks + diff for every case."""
    run_dir = RESULTS_DIR / "runs" / run_id
    if not run_dir.is_dir():
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")

    cases = []
    details_dir = run_dir / "details"
    if details_dir.is_dir():
        for f in sorted(details_dir.glob("*.json")):
            try:
                cases.append(json.loads(f.read_text()))
            except Exception:
                pass

    if not cases:
        return _page(run_id, f"<div class='card'><p>No cases found in run {run_id}.</p></div>")

    model = cases[0].get("model", "")
    total = len(cases)
    passed = sum(1 for c in cases if c.get("passed"))

    # Run parameters from the cases themselves
    temperature = cases[0].get("temperature", 0.0)
    max_attempt = max(c.get("attempt", 1) for c in cases)
    gen_params = cases[0].get("generation_params", {})
    no_think_str = "yes" if gen_params.get("no_think") else "—"
    sdks = sorted({c.get("sdk", "") for c in cases if c.get("sdk")})
    sdk_tags = " ".join(f'<span class="tag">{s}</span>' for s in sdks)
    output_tokens = sum(c.get("token_usage", {}).get("output_tokens", 0) for c in cases)

    # Pre-compute which layers are applicable per case_id across all attempts.
    # A layer is applicable if any attempt actually executed it with real checks.
    cases_by_id: dict[str, list[dict]] = {}
    for c in cases:
        cases_by_id.setdefault(c.get("case_id", ""), []).append(c)
    applicable_by_case: dict[str, set[int]] = {
        cid: _applicable_layers(attempts)
        for cid, attempts in cases_by_id.items()
    }

    # Consistency per case_id: 1-CV over recomputed total_scores across attempts.
    # None when fewer than 5 attempts are available.
    consistency_by_case: dict[str, float | None] = {
        cid: _consistency_score([
            _recompute_total_score(c, applicable_by_case.get(cid, set()))
            for c in attempts
        ])
        for cid, attempts in cases_by_id.items()
    }

    # Summary table of all cases in this run
    sorted_cases = sorted(cases, key=lambda x: (x.get("case_id", ""), x.get("attempt", 1)))
    # Track first-row of each case_id to emit the consistency cell with rowspan.
    first_attempt_seen: set[str] = set()
    summary_rows = ""
    for c in sorted_cases:
        cid = c.get("case_id", "")
        applicable = applicable_by_case.get(cid, set())
        status_badge = _status_badge(c)
        recomputed = _recompute_total_score(c, applicable)
        total_cell = _bar_cell(recomputed) if _result_status(c) != "error" else '<span style="color:#4a5568;font-size:0.8rem">n/a</span>'
        diff = _find_metadata(cid).get("difficulty", "—")
        diff_badge = f'<span class="badge badge-{diff}">{diff}</span>' if diff in ("easy", "medium", "hard") else diff
        l0 = _layer_score_cell(c, 0, applicable)
        l1 = _layer_score_cell(c, 1, applicable)
        l2 = _layer_score_cell(c, 2, applicable)
        l3 = _layer_score_cell(c, 3, applicable)

        # Consistency cell: emitted once per case_id using rowspan.
        if cid not in first_attempt_seen:
            first_attempt_seen.add(cid)
            n_attempts = len(cases_by_id.get(cid, []))
            consistency = consistency_by_case.get(cid)
            if consistency is None:
                cons_content = f'<span style="color:#4a5568;font-size:0.8rem" title="Needs ≥5 attempts (got {n_attempts})">n/a</span>'
            else:
                cons_pct = int(consistency * 100)
                cons_content = f'{_score_bar(consistency)} <span style="font-size:0.8rem">{cons_pct}%</span>'
            consistency_cell = f'<td rowspan="{n_attempts}" style="vertical-align:middle;border-left:1px solid #2d3748">{cons_content}</td>'
        else:
            consistency_cell = ""

        summary_rows += f"""<tr>
          <td><a href="#case-{cid}-att{c.get('attempt',1)}">{cid}</a></td>
          <td style="color:#718096;font-size:0.8rem">{c.get('sdk','—')}</td>
          <td>{diff_badge}</td>
          <td>{status_badge}</td>
          <td>{l0}</td>
          <td>{l1}</td>
          <td>{l2}</td>
          <td>{l3}</td>
          <td>{total_cell}</td>
          <td style="color:#718096;font-size:0.8rem">{c.get('attempt',1)}</td>
          {consistency_cell}
        </tr>"""

    sections = ""
    for result in cases:
        case_id = result.get("case_id", "")
        reference = _find_reference(case_id) or ""
        generated = result.get("generated_code", "")
        overall = _pass_badge(result.get("passed", False))
        score = _bar_cell(result.get("total_score", 0))

        # Checks
        applicable = applicable_by_case.get(case_id, set())
        checks_html = ""
        for layer in result.get("layers", []):
            layer_num = layer.get("layer")
            layer_name = layer.get("name", "")
            layer_passed = layer.get("passed", False)
            layer_error = layer.get("error")
            details = layer.get("details") or []

            # Skip layers not applicable for this case (env-skip sentinels only).
            if layer_num not in applicable and layer_num != 4:
                continue
            # Also skip L4 skipped-due-to-earlier-failure silently.
            if (layer_error or "").startswith("Skipped:") and layer_num not in applicable:
                continue

            layer_score = layer.get("score")
            badge = _pass_badge(layer_passed)
            score_pct = f'<span style="font-size:0.8rem;color:#718096;margin-left:0.5rem">{int(layer_score * 100)}%</span>' if layer_score is not None and details else ""
            checks_html += f'<div style="margin-bottom:0.75rem"><h3>L{layer["layer"]} — {layer_name} {badge}{score_pct}</h3>'
            if layer_error and not details:
                checks_html += f'<p style="color:#718096;font-size:0.8rem;padding:0.25rem 0">{layer_error}</p>'
            else:
                for chk in details:
                    icon = "✓" if chk["passed"] else "✗"
                    color = "#68d391" if chk["passed"] else "#fc8181"
                    name = chk.get("check_name", "")
                    actual = chk.get("actual", "")
                    expected = chk.get("expected", "")
                    detail_html = ""
                    if not chk["passed"]:
                        act_esc = str(actual).replace("<", "&lt;")
                        exp_esc = str(expected).replace("<", "&lt;")
                        detail_html = f'<div class="check-detail">expected: {exp_esc}<br>actual: <span>{act_esc}</span></div>'
                    checks_html += f"""
<div class="check-row">
  <span style="color:{color};font-weight:bold;min-width:1.2rem">{icon}</span>
  <div class="check-name">{name}{detail_html}</div>
</div>"""
            checks_html += "</div>"

        # Diff + side-by-side
        if reference and generated:
            diff_content = _diff_html(reference, generated, fromfile="reference/main.c", tofile="generated")
            diff_section = f'<pre style="max-height:320px;overflow-y:auto">{diff_content}</pre>'
        else:
            diff_section = "<p style='color:#718096;font-size:0.8rem'>No reference or no generated code.</p>"

        ref_esc = reference.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        gen_esc = generated.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        attempt = result.get("attempt", 1)
        prose_retry_badge = (
            '<span title="First response was prose; retried with code-only hint" '
            'style="font-size:0.75rem;background:#744210;color:#fefcbf;padding:2px 6px;'
            'border-radius:4px;margin-left:0.25rem">prose-retry</span>'
            if result.get("prose_retry") else ""
        )
        sections += f"""
<div id="case-{case_id}-att{attempt}" class="card" style="margin-bottom:1.5rem">
  <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem">
    <h2 style="margin:0"><a href="/case/{case_id}">{case_id}</a> <span style="color:#718096;font-size:0.9rem;font-weight:normal">attempt {attempt}</span>{prose_retry_badge}</h2>
    {overall} {score}
  </div>
  <div class="split">
    <div>
      <h3>Checks</h3>
      {checks_html}
    </div>
    <div>
      <h3>Diff (reference → generated)</h3>
      {diff_section}
      <div class="split" style="gap:0.5rem;margin-top:0.75rem">
        <div>
          <h3>Reference</h3>
          <pre class="hljs-wrap" style="max-height:320px;overflow-y:auto"><code class="language-c">{ref_esc}</code></pre>
        </div>
        <div>
          <h3>Generated</h3>
          <pre class="hljs-wrap" style="max-height:320px;overflow-y:auto"><code class="language-c">{gen_esc}</code></pre>
        </div>
      </div>
    </div>
  </div>
</div>"""

    body = f"""
<div style="margin-bottom:1rem">
  <a href="/history" style="color:#718096;font-size:0.85rem">← Run History</a>
</div>
<div class="card" style="margin-bottom:1rem">
  <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;margin-bottom:0.75rem">
    <h1 style="font-size:1rem;font-family:monospace">{run_id}</h1>
    <span style="color:#a0aec0" title="{model}">{model.split('/')[-1]}</span>
    <span style="color:#718096;font-size:0.8rem">Avg score:</span>
    {_bar_cell(sum(_recompute_total_score(c, applicable_by_case.get(c.get("case_id",""), set())) for c in cases) / total if total else 0)}
    <span style="color:#718096;font-size:0.8rem;margin-left:0.5rem">Passed:</span>
    <span style="color:#e2e8f0;font-size:0.85rem">{passed}/{total}</span>
    <span style="color:#718096;font-size:0.8rem;margin-left:0.5rem">Consistency:</span>
    {(lambda vals: _bar_cell(sum(vals)/len(vals)) + f' <span style="font-size:0.75rem;color:#718096">({len(vals)} cases)</span>' if vals else '<span style="color:#4a5568;font-size:0.8rem">n/a — needs ≥5 attempts per case</span>')([v for v in consistency_by_case.values() if v is not None])}
  </div>
  <div style="display:flex;gap:2rem;font-size:0.8rem;color:#718096;flex-wrap:wrap">
    <span>Temperature: <b style="color:#e2e8f0">{temperature:.1f}</b></span>
    <span>Attempts: <b style="color:#e2e8f0">{max_attempt}</b></span>
    <span>No-think: <b style="color:#e2e8f0">{no_think_str}</b></span>
    <span>Output tokens: <b style="color:#e2e8f0">{output_tokens:,}</b></span>
    <span>SDKs: {sdk_tags}</span>
  </div>
</div>
<div class="card" style="padding:0;overflow:auto;margin-bottom:1.5rem">
  <table>
    <thead><tr>
      <th>Case</th><th>SDK</th><th>Difficulty</th>
      <th>Result</th><th>L0</th><th>L1</th><th>L2</th><th>L3</th><th>Total</th><th>Att.</th>
      <th style="border-left:1px solid #2d3748">Consistency</th>
    </tr></thead>
    <tbody>{summary_rows}</tbody>
  </table>
</div>
{sections}
"""
    return _page(run_id, body, highlight=True)


@app.get("/cases", response_class=HTMLResponse)
def cases_list() -> str:
    """List of all benchmark cases with metadata."""
    cases = _all_cases()
    if not cases:
        return _page("Cases", "<div class='card'><p>No cases found.</p></div>")

    rows = ""
    for meta in cases:
        case_id = meta.get("_case_id", "")
        sdk = meta.get("sdk", "—")
        diff = meta.get("difficulty", "—")
        diff_badge = f'<span class="badge badge-{diff}">{diff}</span>' if diff in ("easy", "medium", "hard") else diff
        tier = meta.get("tier", "—")
        category = meta.get("category", "—")
        title = meta.get("title", "")
        tags = " ".join(f'<span class="tag">{t}</span>' for t in meta.get("tags", []))
        rows += f"""<tr>
          <td><a href="/cases/{case_id}">{case_id}</a></td>
          <td style="color:#718096;font-size:0.8rem">{sdk}</td>
          <td>{diff_badge}</td>
          <td style="color:#718096">{category}</td>
          <td style="color:#718096">{tier}</td>
          <td style="color:#a0aec0;font-size:0.8rem">{title}</td>
          <td>{tags}</td>
        </tr>"""

    body = f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem">
  <h1>Cases</h1>
  <span style="color:#718096;font-size:0.85rem">{len(cases)} cases</span>
</div>
<div class="card" style="padding:0;overflow:auto">
  <table>
    <thead><tr>
      <th>Case ID</th><th>SDK</th><th>Difficulty</th>
      <th>Category</th><th>Tier</th><th>Title</th><th>Tags</th>
    </tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>
"""
    return _page("Cases", body)


def _editor_panel(
    label: str,
    subtitle: str,
    editor_id: str,
    content_esc: str,
    save_fn: str,
    msg_id: str,
) -> str:
    """Reusable editable panel with Save button."""
    return f"""
<div class="card">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.75rem">
    <h2 style="margin:0">{label} <span style="font-weight:normal;color:#718096;font-size:0.8rem">{subtitle}</span></h2>
    <div style="display:flex;align-items:center;gap:1rem">
      <span id="{msg_id}" style="font-size:0.8rem"></span>
      <button onclick="{save_fn}()"
        style="background:#2d3748;border:1px solid #4a5568;color:#e2e8f0;
               padding:4px 14px;border-radius:4px;cursor:pointer;font-size:0.85rem">
        Save
      </button>
    </div>
  </div>
  <textarea id="{editor_id}"
    style="width:100%;height:480px;background:#0d1117;color:#e2e8f0;
           border:1px solid #2d3748;border-radius:6px;padding:0.75rem;
           font-family:monospace;font-size:0.8rem;line-height:1.5;resize:vertical"
    spellcheck="false">{content_esc}</textarea>
</div>"""


def _check_panel(case_dir: Path) -> str:
    """Read-only panel showing checks/static.py and checks/behavior.py."""
    checks_dir = case_dir / "checks"
    if not checks_dir.is_dir():
        return "<div class='card'><h2>Checks</h2><p style='color:#718096'>No checks directory found.</p></div>"

    html = "<div class='card'><h2>Checks</h2>"
    for fname in ("static.py", "behavior.py"):
        fpath = checks_dir / fname
        if not fpath.is_file():
            continue
        code = fpath.read_text(encoding="utf-8")
        code_esc = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        html += (
            f'<h3 style="margin-top:1rem">{fname}</h3>'
            f'<pre class="hljs-wrap" style="max-height:480px;overflow-y:auto">'
            f'<code class="language-python">{code_esc}</code></pre>'
        )
    html += "</div>"
    return html


@app.get("/cases/{case_id}", response_class=HTMLResponse)
def case_editor(case_id: str) -> str:
    """Case detail: prompt editor, reference editor, checks (read-only)."""
    case_dir = _find_case_dir(case_id)
    if case_dir is None:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")

    meta = _find_metadata(case_id)
    prompt = _find_prompt(case_id) or ""
    reference = _find_reference(case_id) or ""

    diff = meta.get("difficulty", "")
    diff_badge = f'<span class="badge badge-{diff}">{diff}</span>' if diff else ""
    tags = " ".join(f'<span class="tag">{t}</span>' for t in meta.get("tags", []))

    prompt_esc = prompt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    ref_esc = reference.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    save_js = f"""
function _save(url, content, msgId, confirmMsg) {{
  if (!confirm(confirmMsg)) return;
  fetch(url, {{
    method: 'POST',
    headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{content: content}})
  }})
  .then(r => r.json())
  .then(data => {{
    const msg = document.getElementById(msgId);
    msg.textContent = data.ok ? 'Saved.' : ('Error: ' + data.error);
    msg.style.color = data.ok ? '#68d391' : '#fc8181';
    setTimeout(() => {{ msg.textContent = ''; }}, 3000);
  }});
}}
function savePrompt() {{
  _save('/cases/{case_id}/prompt',
        document.getElementById('prompt-editor').value,
        'prompt-msg', 'Overwrite prompt.md for {case_id}?');
}}
function saveReference() {{
  _save('/cases/{case_id}/reference',
        document.getElementById('ref-editor').value,
        'ref-msg', 'Overwrite reference/main.c for {case_id}?');
}}
"""

    prompt_panel = _editor_panel("Prompt", "prompt.md", "prompt-editor", prompt_esc, "savePrompt", "prompt-msg")
    ref_panel = _editor_panel("Reference", "reference/main.c", "ref-editor", ref_esc, "saveReference", "ref-msg")

    body = f"""
<div style="margin-bottom:1rem;display:flex;align-items:center;gap:1.5rem">
  <a href="/cases" style="color:#718096;font-size:0.85rem">← Cases</a>
  <a href="/cases/{case_id}/checks" style="color:#718096;font-size:0.85rem">View checks →</a>
</div>
<div class="card">
  <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem">
    <h1>{case_id}</h1>
    {diff_badge}
    <span style="color:#718096;font-size:0.85rem">{meta.get('sdk','')}</span>
    <span style="color:#718096;font-size:0.85rem">{meta.get('category','')}</span>
  </div>
  <p style="color:#a0aec0;margin-bottom:0.5rem">{meta.get('title','')}</p>
  <div>{tags}</div>
</div>

<div class="split">
  {prompt_panel}
  {ref_panel}
</div>
<script>{save_js}</script>
"""
    return _page(case_id, body)


class _FilePayload(BaseModel):
    content: str


@app.get("/cases/{case_id}/checks", response_class=HTMLResponse)
def case_checks(case_id: str) -> str:
    """Read-only view of checks/static.py and checks/behavior.py."""
    case_dir = _find_case_dir(case_id)
    if case_dir is None:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")

    checks_html = _check_panel(case_dir)

    body = f"""
<div style="margin-bottom:1rem">
  <a href="/cases/{case_id}" style="color:#718096;font-size:0.85rem">← {case_id}</a>
</div>
{checks_html}
"""
    return _page(f"{case_id} / checks", body, highlight=True)


@app.post("/cases/{case_id}/prompt")
def save_prompt(case_id: str, payload: _FilePayload) -> JSONResponse:
    """Overwrite prompt.md for a case."""
    case_dir = _find_case_dir(case_id)
    if case_dir is None:
        return JSONResponse({"ok": False, "error": f"Case {case_id} not found"}, status_code=404)
    try:
        (case_dir / "prompt.md").write_text(payload.content, encoding="utf-8")
    except Exception as exc:
        return JSONResponse({"ok": False, "error": str(exc)}, status_code=500)
    return JSONResponse({"ok": True})


@app.post("/cases/{case_id}/reference")
def save_reference(case_id: str, payload: _FilePayload) -> JSONResponse:
    """Overwrite reference/main.c for a case."""
    case_dir = _find_case_dir(case_id)
    if case_dir is None:
        return JSONResponse({"ok": False, "error": f"Case {case_id} not found"}, status_code=404)
    ref_file = case_dir / "reference" / "main.c"
    try:
        ref_file.parent.mkdir(parents=True, exist_ok=True)
        ref_file.write_text(payload.content, encoding="utf-8")
    except Exception as exc:
        return JSONResponse({"ok": False, "error": str(exc)}, status_code=500)
    return JSONResponse({"ok": True})


@app.get("/docs/layers", response_class=HTMLResponse)
def docs_layers() -> str:
    """Documentation page describing the 5-layer evaluation pipeline."""
    body = """
<h1 style="margin-bottom:1.5rem">Evaluation Layers</h1>

<p style="color:#a0aec0;margin-bottom:2rem">
  Each case is evaluated through up to 5 layers in order. A failure at any layer
  (L0–L3) stops evaluation for that attempt — subsequent layers are skipped.
  L4 is a benchmark quality audit and never affects the case pass/fail result.
</p>

<div class="card" style="margin-bottom:1.5rem">
  <h2 style="margin-bottom:0.5rem">L0 — Static Analysis</h2>
  <p style="color:#718096;font-size:0.85rem;margin-bottom:0.75rem">
    Pattern-matching on the raw generated source text. No compilation needed.
  </p>
  <ul style="color:#a0aec0;font-size:0.85rem;line-height:1.8">
    <li>Checks defined in <code>checks/static.py</code> for each case.</li>
    <li>Verifies required includes, API names, function signatures, constants.</li>
    <li>Anti-hallucination: rejects STM32/Zephyr/Arduino APIs on NXP cases.</li>
    <li>Present on every case. If absent, the layer passes automatically.</li>
  </ul>
  <p style="margin-top:0.75rem;font-size:0.8rem;color:#718096">
    <b>Score:</b> weighted fraction of checks passed (each check has a weight, default 1.0).
  </p>
</div>

<div class="card" style="margin-bottom:1.5rem">
  <h2 style="margin-bottom:0.5rem">L1 — Compile Gate</h2>
  <p style="color:#718096;font-size:0.85rem;margin-bottom:0.75rem">
    Attempts to compile the generated code against the real SDK.
  </p>
  <ul style="color:#a0aec0;font-size:0.85rem;line-height:1.8">
    <li>Only runs when a <code>CMakeLists.txt</code> is present in the case directory.</li>
    <li>Dispatches to the appropriate toolchain: Zephyr (west), ESP-IDF (idf.py), STM32 (arm-none-eabi-gcc).</li>
    <li>Docker mode: compiles in an isolated container with the full SDK image.</li>
    <li>Local mode: compiles on the host (requires SDK + toolchain installed).</li>
    <li>Cases without <code>CMakeLists.txt</code> (e.g. defconfig, scripts) show <b>—</b> for this layer.</li>
  </ul>
  <p style="margin-top:0.75rem;font-size:0.8rem;color:#718096">
    <b>Score:</b> binary — 100% if compilation succeeds, 0% otherwise.
  </p>
</div>

<div class="card" style="margin-bottom:1.5rem">
  <h2 style="margin-bottom:0.5rem">L2 — Runtime Execution</h2>
  <p style="color:#718096;font-size:0.85rem;margin-bottom:0.75rem">
    Runs the compiled binary on a simulator and captures output.
  </p>
  <ul style="color:#a0aec0;font-size:0.85rem;line-height:1.8">
    <li>Uses the build artifacts from L1 (shared build directory).</li>
    <li>Zephyr: <code>west build -t run</code> on <code>native_sim</code> board target only.</li>
    <li>Hardware targets (nrf52840dk, etc.) are skipped — no physical hardware available.</li>
    <li>Checks that expected output appears in stdout within a timeout window.</li>
    <li>Cases without <code>CMakeLists.txt</code> show <b>—</b> for this layer.</li>
  </ul>
  <p style="margin-top:0.75rem;font-size:0.8rem;color:#718096">
    <b>Score:</b> fraction of runtime output checks passed.
  </p>
</div>

<div class="card" style="margin-bottom:1.5rem">
  <h2 style="margin-bottom:0.5rem">L3 — Static Heuristic (Behavioral)</h2>
  <p style="color:#718096;font-size:0.85rem;margin-bottom:0.75rem">
    Domain-knowledge checks that verify implicit correctness — things the model
    must know without being told in the prompt.
  </p>
  <ul style="color:#a0aec0;font-size:0.85rem;line-height:1.8">
    <li>Checks defined in <code>checks/behavior.py</code> for each case.</li>
    <li>Examples: clock enable before peripheral init, volatile on ISR-shared variables,
        error return values checked, correct I2C address bit-shifting.</li>
    <li>These checks are never mentioned in the prompt — the model must apply
        domain knowledge autonomously.</li>
    <li>Present only when a <code>checks/behavior.py</code> file exists.</li>
  </ul>
  <p style="margin-top:0.75rem;font-size:0.8rem;color:#718096">
    <b>Score:</b> weighted fraction of behavioral checks passed.
  </p>
</div>

<div class="card" style="margin-bottom:1.5rem;border-left:3px solid #4a5568">
  <h2 style="margin-bottom:0.5rem;color:#a0aec0">L4 — Test Quality Proof <span style="font-size:0.75rem;font-weight:normal;color:#718096">(benchmark audit, not model score)</span></h2>
  <p style="color:#718096;font-size:0.85rem;margin-bottom:0.75rem">
    Mutation testing: verifies that the case checks are rigorous enough to detect seeded bugs.
  </p>
  <ul style="color:#a0aec0;font-size:0.85rem;line-height:1.8">
    <li>Loads deliberately broken code variants from <code>checks/negatives.py</code>.</li>
    <li>Applies each mutation to the generated code and runs L0+L3 checks on it.</li>
    <li>If the checks <em>pass</em> on a broken variant, L4 fails — the checks are too lenient.</li>
    <li>L4 failure <b>does not affect</b> the case pass/fail or total score — it only signals
        that the benchmark itself needs improvement.</li>
    <li>Optional: cases without <code>checks/negatives.py</code> skip L4 automatically (PASS).</li>
  </ul>
  <p style="margin-top:0.75rem;font-size:0.8rem;color:#718096">
    <b>Score:</b> fraction of mutations correctly rejected by checks.
  </p>
</div>

<div class="card">
  <h2 style="margin-bottom:1rem">Scoring Summary</h2>
  <table>
    <thead><tr>
      <th>Layer</th><th>Name</th><th>Affects pass/fail</th><th>Shown when</th><th>Score</th>
    </tr></thead>
    <tbody>
      <tr><td>L0</td><td>static_analysis</td><td>Yes</td><td>checks/static.py present</td><td>Weighted check fraction</td></tr>
      <tr><td>L1</td><td>compile_gate</td><td>Yes</td><td>CMakeLists.txt present</td><td>Binary (compile success)</td></tr>
      <tr><td>L2</td><td>runtime_execution</td><td>Yes</td><td>CMakeLists.txt + native_sim</td><td>Output check fraction</td></tr>
      <tr><td>L3</td><td>static_heuristic</td><td>Yes</td><td>checks/behavior.py present</td><td>Weighted check fraction</td></tr>
      <tr style="color:#718096"><td>L4</td><td>test_quality_proof</td><td><b>No</b></td><td>checks/negatives.py present</td><td>Mutation rejection rate</td></tr>
    </tbody>
  </table>
  <p style="margin-top:1rem;font-size:0.8rem;color:#718096">
    <b>Total score</b> = mean of applicable layer scores (L0–L3 only, L4 excluded).
    Layers skipped due to earlier failure contribute 0 to the numerator.
    Layers not defined for a case are excluded from the denominator.
    <br><br>
    <b>Consistency</b> = 1 − CV = 1 − (std / mean) across ≥5 attempts.
    Measures how predictable the model is across repeated calls.
    1.0 = perfectly consistent, 0.0 = highly variable.
  </p>
</div>
"""
    return _page("Layers", body)


@app.get("/docs/models", response_class=HTMLResponse)
def docs_models() -> str:
    """Reference page with technical specs for all preset benchmark models."""
    body = """
<h1>Model Reference</h1>
<p>Technical specifications for all preset models available in the benchmark runner.
Specs sourced from official model cards and provider documentation (verified 2026-06-07).</p>

<style>
.models-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.models-table th { background: #1e293b; color: #94a3b8; font-weight: 600;
  text-align: left; padding: 8px 12px; border-bottom: 2px solid #334155; }
.models-table td { padding: 7px 12px; border-bottom: 1px solid #1e293b; vertical-align: middle; }
.models-table tr:hover td { background: #0f172a; }
.models-table .section-header td { background: #0f172a; color: #64748b;
  font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.08em; padding: 6px 12px; }
.tag { display: inline-block; padding: 1px 7px; border-radius: 4px;
  font-size: 0.78rem; font-weight: 600; }
.tag-moe  { background: #1e3a5f; color: #60a5fa; }
.tag-dense { background: #1e3b2e; color: #4ade80; }
.think-yes { color: #4ade80; font-weight: 700; }
.think-no  { color: #475569; }
.model-id  { font-family: monospace; font-size: 0.82rem; color: #e2e8f0; }
.provider  { color: #94a3b8; font-size: 0.82rem; }
</style>

<table class="models-table">
  <thead>
    <tr>
      <th>Model</th>
      <th>Params total</th>
      <th>Params active</th>
      <th>Architecture</th>
      <th>Think</th>
      <th>Context</th>
    </tr>
  </thead>
  <tbody>
    <tr class="section-header"><td colspan="6">Groq</td></tr>
    <tr>
      <td class="model-id">llama-3.3-70b-versatile</td>
      <td>70 B</td><td>70 B</td>
      <td><span class="tag tag-dense">Dense</span></td>
      <td class="think-no">—</td><td>128 K</td>
    </tr>
    <tr>
      <td class="model-id">llama-4-scout-17b-16e-instruct</td>
      <td>109 B</td><td>17 B</td>
      <td><span class="tag tag-moe">MoE</span> 16 experts</td>
      <td class="think-no">—</td><td>10 M</td>
    </tr>
    <tr>
      <td class="model-id">qwen3-32b</td>
      <td>32.8 B</td><td>32.8 B</td>
      <td><span class="tag tag-dense">Dense</span></td>
      <td class="think-yes">✓ hybrid</td><td>128 K</td>
    </tr>
    <tr>
      <td class="model-id">gpt-oss-20b</td>
      <td>21 B</td><td>3.6 B</td>
      <td><span class="tag tag-moe">MoE</span> 32 exp, top-4</td>
      <td class="think-no">—</td><td>128 K</td>
    </tr>
    <tr>
      <td class="model-id">gpt-oss-120b</td>
      <td>120 B</td><td>5.1 B</td>
      <td><span class="tag tag-moe">MoE</span> 128 exp, top-4</td>
      <td class="think-no">—</td><td>128 K</td>
    </tr>
    <tr class="section-header"><td colspan="6">OpenRouter</td></tr>
    <tr>
      <td class="model-id">deepseek-r1-0528</td>
      <td>685 B</td><td>37 B</td>
      <td><span class="tag tag-moe">MoE</span></td>
      <td class="think-yes">✓ CoT</td><td>128 K</td>
    </tr>
    <tr>
      <td class="model-id">deepseek-chat-v3-0324</td>
      <td>671 B</td><td>37 B</td>
      <td><span class="tag tag-moe">MoE</span></td>
      <td class="think-no">—</td><td>128 K</td>
    </tr>
    <tr>
      <td class="model-id">deepseek-v4-flash</td>
      <td>284 B</td><td>13 B</td>
      <td><span class="tag tag-moe">MoE</span> hybrid attn</td>
      <td class="think-yes">✓ 3 modes</td><td>1 M</td>
    </tr>
    <tr>
      <td class="model-id">llama-4-maverick</td>
      <td>~400 B</td><td>17 B</td>
      <td><span class="tag tag-moe">MoE</span> 128 experts</td>
      <td class="think-no">—</td><td>1 M</td>
    </tr>
    <tr>
      <td class="model-id">llama-3.3-70b-instruct</td>
      <td>70 B</td><td>70 B</td>
      <td><span class="tag tag-dense">Dense</span></td>
      <td class="think-no">—</td><td>128 K</td>
    </tr>
    <tr>
      <td class="model-id">qwen3-235b-a22b</td>
      <td>235 B</td><td>22 B</td>
      <td><span class="tag tag-moe">MoE</span> 128 exp, top-8</td>
      <td class="think-yes">✓ hybrid</td><td>128 K</td>
    </tr>
    <tr>
      <td class="model-id">qwen3-30b-a3b</td>
      <td>30 B</td><td>3 B</td>
      <td><span class="tag tag-moe">MoE</span> 128 exp, top-8</td>
      <td class="think-yes">✓ hybrid</td><td>128 K</td>
    </tr>
    <tr>
      <td class="model-id">gemini-2.5-flash</td>
      <td>proprietary</td><td>proprietary</td>
      <td><span class="tag tag-moe">MoE</span> proprietary</td>
      <td class="think-yes">✓</td><td>1 M</td>
    </tr>
    <tr>
      <td class="model-id">gemini-2.5-pro</td>
      <td>proprietary</td><td>proprietary</td>
      <td><span class="tag tag-moe">MoE</span> proprietary</td>
      <td class="think-yes">✓</td><td>1 M</td>
    </tr>
    <tr>
      <td class="model-id">mistral-small-3.2-24b-instruct</td>
      <td>23.6 B</td><td>23.6 B</td>
      <td><span class="tag tag-dense">Dense</span></td>
      <td class="think-no">—</td><td>128 K</td>
    </tr>
  </tbody>
</table>
"""
    return _page("Docs — Models", body)
    return _page("Docs — Evaluation Layers", body)
