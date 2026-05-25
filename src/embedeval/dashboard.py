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

import yaml
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

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
.score-bar { display: inline-block; height: 8px; border-radius: 4px;
             background: #2d3748; width: 80px; vertical-align: middle;
             position: relative; overflow: hidden; }
.score-fill { height: 100%; border-radius: 4px; }
"""

_NAV = """
<nav class="nav">
  <h1>EmbedEval</h1>
  <a href="/">Leaderboard</a>
  <a href="/history">Run History</a>
</nav>
"""


def _page(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — EmbedEval</title>
  <style>{_BASE_CSS}</style>
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
    pct = int(score * 100)
    color = "#68d391" if score >= 0.8 else "#f6ad55" if score >= 0.5 else "#fc8181"
    return (
        f'<span class="score-bar">'
        f'<span class="score-fill" style="width:{pct}%;background:{color}"></span>'
        f'</span> {pct}%'
    )


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
def leaderboard() -> str:
    """Leaderboard: rows=models, columns=difficulty buckets (easy/medium/hard)."""
    results = _all_results()

    if not results:
        return _page("Leaderboard", "<div class='card'><p>No results found in results/. Run a benchmark first.</p></div>")

    # Collect unique models (insertion order)
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
        model_stats[model] = {
            "passed": passed, "total": total, "pct": pct,
            "buckets": {d: _bucket_stats(model, d) for d in _DIFFICULTIES},
        }

    # Sort models by overall pass rate descending
    models = sorted(models, key=lambda m: model_stats[m]["pct"], reverse=True)

    # Header
    diff_headers = "".join(
        f'<th style="text-align:center"><span class="badge badge-{d}">{d.capitalize()}</span></th>'
        for d in _DIFFICULTIES
    )
    header_cells = f"<th>Model</th><th>Overall</th><th>Passed</th>{diff_headers}"

    rows = ""
    for model in models:
        s = model_stats[model]
        short = model.split("/")[-1]
        score_cell = _score_bar(s["passed"] / s["total"] if s["total"] else 0)
        row = (
            f"<td title='{model}' style='font-family:monospace;font-size:0.8rem'>{short}</td>"
            f"<td>{score_cell}</td>"
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

    body = f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem">
  <h1>Leaderboard</h1>
  <span style="color:#718096;font-size:0.85rem">{len(models)} models · {sum(diff_counts.values())} cases ({", ".join(subtitle_parts)})</span>
</div>
<div class="card" style="padding:0;overflow:auto">
  <table>
    <thead><tr>{header_cells}</tr></thead>
    <tbody>{rows}</tbody>
  </table>
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
        score = _score_bar(r.get("total_score", 0))
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

        badge = _pass_badge(layer_passed)
        checks_html += f'<div style="margin-bottom:1rem"><h3>L{layer["layer"]} — {layer_name} {badge}</h3>'

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
          <pre>{ref_esc}</pre>
        </div>
        <div>
          <h3>Generated</h3>
          <pre>{gen_esc}</pre>
        </div>
      </div>
    </div>
  </div>

</div>
"""
    return _page(f"{case_id} / {model_short}", body)


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
        pct = int(passed / total * 100) if total else 0
        bar = _score_bar(passed / total if total else 0)
        rows += f"""<tr>
          <td style="font-family:monospace">{run['run_id']}</td>
          <td>{model_tags}</td>
          <td>{bar}</td>
          <td style="color:#718096">{passed}/{total}</td>
        </tr>"""

    body = f"""
<h1 style="margin-bottom:1rem">Run History</h1>
<div class="card" style="padding:0;overflow:auto">
  <table>
    <thead><tr><th>Run</th><th>Models</th><th>Score</th><th>Passed</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>
"""
    return _page("History", body)
