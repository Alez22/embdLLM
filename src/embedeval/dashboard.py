"""EmbedEval results dashboard.

Lightweight FastAPI web app that reads results/ and cases/ directly —
no database, no build step. Start with:
    uv run embedeval dashboard
Then open http://localhost:7860.
"""

import json
import difflib
import webbrowser
from pathlib import Path
from threading import Timer
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
  <a href="/cases">Cases</a>
  <a href="/history">Run History</a>
  <a href="/review">Review</a>
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


def _diff_html(a: str, b: str, fromfile: str = "reference", tofile: str = "generated") -> str:
    """Return unified diff as HTML with syntax coloring."""
    a_lines = a.splitlines(keepends=True)
    b_lines = b.splitlines(keepends=True)
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

    # Collect unique models from filtered results
    models: list[str] = []
    seen_models: set[str] = set()
    for r in results:
        m = r.get("model", "")
        if m and m not in seen_models:
            models.append(m)
            seen_models.add(m)

    # Build lookup: (case_id, model) → result (keep latest attempt)
    lookup: dict[tuple[str, str], dict] = {}
    for r in results:
        key = (r.get("case_id", ""), r.get("model", ""))
        if key not in lookup or r.get("attempt", 0) > lookup[key].get("attempt", 0):
            lookup[key] = r

    # Map case_id → difficulty from metadata
    case_difficulty: dict[str, str] = {}
    for (case_id, _) in lookup:
        if case_id not in case_difficulty:
            meta = _find_metadata(case_id)
            case_difficulty[case_id] = meta.get("difficulty", "unknown")

    # Per-model stats: overall + per difficulty bucket
    def _bucket_stats(model: str, difficulty: str) -> dict:
        bucket = [
            r for (cid, m), r in lookup.items()
            if m == model and case_difficulty.get(cid) == difficulty
        ]
        total = len(bucket)
        passed = sum(1 for r in bucket if r.get("passed"))
        pct = int(passed / total * 100) if total else 0
        return {"passed": passed, "total": total, "pct": pct}

    model_stats: dict[str, dict] = {}
    for model in models:
        all_results_for_model = [r for (_, m), r in lookup.items() if m == model]
        total = len(all_results_for_model)
        passed = sum(1 for r in all_results_for_model if r.get("passed"))
        pct = int(passed / total * 100) if total else 0
        coverage = (
            sum(r.get("total_score", 0.0) for r in all_results_for_model) / total
            if total else 0.0
        )
        avg_duration = (
            sum(r.get("duration_seconds", 0.0) for r in all_results_for_model) / total
            if total else 0.0
        )
        model_stats[model] = {
            "passed": passed, "total": total, "pct": pct,
            "coverage": coverage,
            "avg_duration": avg_duration,
            "buckets": {d: _bucket_stats(model, d) for d in _DIFFICULTIES},
        }

    # Sort by pass rate descending, then check coverage as tiebreaker
    models = sorted(models, key=lambda m: (model_stats[m]["pct"], model_stats[m]["coverage"]), reverse=True)

    # Filter form
    def _options(values: set[str], current: str, param: str) -> str:
        opts = f'<option value="">All</option>'
        for v in sorted(values):
            sel = ' selected' if v == current else ''
            opts += f'<option value="{v}"{sel}>{v}</option>'
        return f'<select name="{param}" onchange="this.form.submit()" style="background:#2d3748;color:#e2e8f0;border:1px solid #4a5568;border-radius:4px;padding:3px 8px;font-size:0.8rem">{opts}</select>'

    filter_form = f"""
<form method="get" style="display:flex;align-items:center;gap:1rem;font-size:0.85rem;color:#a0aec0">
  <span>SDK: {_options(all_sdks, filter_sdk, "sdk")}</span>
  <span>Difficulty: {_options(all_diffs, filter_diff, "difficulty")}</span>
</form>"""

    # Header
    diff_headers = "".join(
        f'<th style="text-align:center"><span class="badge badge-{d}">{d.capitalize()}</span></th>'
        for d in _DIFFICULTIES
    )
    header_cells = f"<th>Model</th><th>pass@1</th><th>check coverage</th><th>avg time</th><th>Passed</th>{diff_headers}"

    rows = ""
    for model in models:
        s = model_stats[model]
        short = model.split("/")[-1]
        dur = s["avg_duration"]
        dur_str = f"{dur:.1f}s" if dur < 60 else f"{dur/60:.1f}m"
        dur_color = "#68d391" if dur < 10 else "#f6ad55" if dur < 30 else "#fc8181"
        review_url = f"/review?model={quote(model, safe='')}"
        if filter_sdk:
            review_url += f"&sdk={quote(filter_sdk, safe='')}"
        row = (
            f"<td title='{model}' style='font-family:monospace;font-size:0.8rem'>"
            f"<a href='{review_url}'>{short}</a></td>"
            f"<td>{_bar_cell(s['passed'] / s['total'] if s['total'] else 0)}</td>"
            f"<td>{_bar_cell(s['coverage'])}</td>"
            f"<td style='color:{dur_color};font-variant-numeric:tabular-nums'>{dur_str}</td>"
            f"<td style='color:#a0aec0'>{s['passed']}/{s['total']}</td>"
        )
        for diff in _DIFFICULTIES:
            b = s["buckets"][diff]
            if b["total"] == 0:
                row += "<td class='cell-none' style='text-align:center'>—</td>"
            else:
                color_cls = "cell-pass" if b["pct"] >= 60 else "cell-fail"
                row += f"<td class='{color_cls}'>{b['pct']}% <span style='font-weight:normal;font-size:0.75rem'>({b['passed']}/{b['total']})</span></td>"
        rows += f"<tr>{row}</tr>"

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
<div class="card" style="padding:0;overflow:auto;margin-top:1rem">
  <table>
    <thead><tr>{header_cells}</tr></thead>
    <tbody>{rows}</tbody>
  </table>
  {no_results_msg}
</div>
"""
    return _page("Leaderboard", body)


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
    """Human review view: all cases for a given model + optional SDK filter.

    Query params:
      ?model=groq/llama-3.3-70b-versatile  — required
      ?sdk=mcuxpresso-sdk                   — optional, narrows the case list
    """
    filter_model = request.query_params.get("model", "")
    filter_sdk = request.query_params.get("sdk", "")

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

    # Apply SDK filter
    if filter_sdk:
        visible = [
            r for r in model_results
            if _find_metadata(r.get("case_id", "")).get("sdk") == filter_sdk
        ]
    else:
        visible = model_results

    # Keep only latest attempt per case
    latest: dict[str, dict] = {}
    for r in visible:
        cid = r.get("case_id", "")
        if cid not in latest or r.get("attempt", 0) > latest[cid].get("attempt", 0):
            latest[cid] = r

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
        opts = f'<option value="">All SDKs</option>'
        for sdk in sorted(available_sdks):
            sel = ' selected' if sdk == filter_sdk else ''
            opts += f'<option value="{sdk}"{sel}>{sdk}</option>'
        return (
            f'<select name="sdk" onchange="this.form.submit()" '
            f'style="background:#2d3748;color:#e2e8f0;border:1px solid #4a5568;'
            f'border-radius:4px;padding:3px 8px;font-size:0.8rem">{opts}</select>'
        )

    filter_form = f"""
<form method="get" style="display:flex;align-items:center;gap:1rem;font-size:0.85rem;color:#a0aec0">
  <input type="hidden" name="model" value="{filter_model}">
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
        passed_badge = _pass_badge(r.get("passed", False))
        score = _bar_cell(r.get("total_score", 0))
        layer = r.get("failed_at_layer")
        layer_str = f"L{layer}" if layer is not None else "—"
        detail_url = f"/case/{cid}/{filter_model}"
        rows += f"""<tr>
          <td><a href="{detail_url}">{cid}</a></td>
          <td style="color:#718096;font-size:0.8rem">{sdk_label}</td>
          <td>{diff_badge}</td>
          <td style="color:#718096;font-size:0.8rem">{category}</td>
          <td style="color:#a0aec0;font-size:0.8rem">{title}</td>
          <td>{passed_badge}</td>
          <td>{score}</td>
          <td style="color:#718096;font-size:0.8rem">{layer_str}</td>
          <td style="color:#718096;font-size:0.8rem">{r.get('attempt', 1)}</td>
        </tr>"""

    total = len(sorted_cases)
    passed = sum(1 for r in sorted_cases if r.get("passed"))
    model_short = filter_model.split("/")[-1]

    body = f"""
<div style="margin-bottom:1rem">
  <a href="/" style="color:#718096;font-size:0.85rem">← Leaderboard</a>
</div>
<div class="card" style="margin-bottom:1rem">
  <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap">
    <h1 style="font-family:monospace">{model_short}</h1>
    <span style="color:#718096;font-size:0.85rem" title="{filter_model}">{filter_model}</span>
    <span style="color:#718096;font-size:0.85rem">{passed}/{total} passed</span>
    {_bar_cell(passed / total if total else 0)}
  </div>
</div>
{filter_form}
<div class="card" style="padding:0;overflow:auto;margin-top:1rem">
  <table>
    <thead><tr>
      <th>Case</th><th>SDK</th><th>Difficulty</th><th>Category</th>
      <th>Title</th><th>Result</th><th>Score</th><th>Failed at</th><th>Attempt</th>
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
        bar = _bar_cell(passed / total if total else 0)

        # Total output tokens for the run
        output_tokens = sum(
            c.get("token_usage", {}).get("output_tokens", 0) for c in cases
        )
        tokens_str = f"{output_tokens:,}"

        # A run is complete if every case produced generated_code (non-empty).
        # Cases that errored before the LLM call have empty generated_code.
        incomplete = sum(1 for c in cases if not c.get("generated_code", "").strip())
        if incomplete == 0:
            status_html = '<span class="badge badge-pass">complete</span>'
        else:
            status_html = f'<span class="badge badge-fail">partial ({total - incomplete}/{total})</span>'

        rows += f"""<tr>
          <td style="font-family:monospace;font-size:0.8rem">
            <a href="/history/{run['run_id']}">{run['run_id']}</a>
          </td>
          <td>{model_tags}</td>
          <td>{status_html}</td>
          <td style="color:#a0aec0;text-align:right;font-variant-numeric:tabular-nums">{tokens_str}</td>
          <td>{bar}</td>
          <td style="color:#718096">{passed}/{total}</td>
        </tr>"""

    body = f"""
<h1 style="margin-bottom:1rem">Run History</h1>
<div class="card" style="padding:0;overflow:auto">
  <table>
    <thead><tr><th>Run</th><th>Models</th><th>Status</th><th style="text-align:right">Tokens out</th><th>Score</th><th>Passed</th></tr></thead>
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

    sections = ""
    for result in cases:
        case_id = result.get("case_id", "")
        reference = _find_reference(case_id) or ""
        generated = result.get("generated_code", "")
        overall = _pass_badge(result.get("passed", False))
        score = _bar_cell(result.get("total_score", 0))

        # Checks
        checks_html = ""
        for layer in result.get("layers", []):
            layer_name = layer.get("name", "")
            layer_passed = layer.get("passed", False)
            layer_error = layer.get("error")
            details = layer.get("details", [])
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

        sections += f"""
<div class="card" style="margin-bottom:1.5rem">
  <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem">
    <h2 style="margin:0"><a href="/case/{case_id}">{case_id}</a></h2>
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
<div class="card" style="margin-bottom:1.5rem">
  <div style="display:flex;align-items:center;gap:1rem">
    <h1 style="font-size:1rem;font-family:monospace">{run_id}</h1>
    <span style="color:#718096;font-size:0.85rem">{model.split('/')[-1]}</span>
    <span style="color:#718096;font-size:0.85rem">{passed}/{total} passed</span>
  </div>
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
