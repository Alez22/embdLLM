"""Visual benchmark report — aggregates ALL runs per model and renders
interactive Plotly charts.

Design assumptions (per project owner):
- Every model is expected to eventually cover the full case set. Runs are
  partial only because the benchmark is still in progress. So we aggregate
  ALL runs of a model into one profile rather than picking a single run.
- The report highlights two things: how well a model covers the whole test
  set (pass rate AND coverage), and a per-SDK breakdown.

The HTML body is produced by ``generate_report_body()`` so the dashboard can
embed it under a ``/report`` route, while ``write_standalone_report()`` wraps
it into a self-contained file (Plotly JS inlined) for sharing.

No custom Plotly theme fights here: we pass ``template="plotly_dark"`` so the
charts blend with the dashboard's dark theme and stay readable standalone.
"""

from __future__ import annotations

import json
from pathlib import Path

import plotly.graph_objects as go
import plotly.io as pio

# Heatmap colour scale: red (0%) -> yellow (50%) -> green (100%).
_RDYLGN = "RdYlGn"

# Layer index -> short label, used by the layer pass-rate heatmap. Mirrors the
# `name` field in the detail JSONs but kept compact for axis ticks.
_LAYER_LABELS = {
    0: "L0 static",
    1: "L1 compile",
    2: "L2 runtime",
    3: "L3 heuristic",
    4: "L4 mutation",
}

# One short explainer per section, rendered under each <h2> as a <p class=desc>.
_DESC = {
    "leaderboard": (
        "<p class='desc'>Models ranked by pass@1 (share of covered cases that "
        "pass all evaluation layers). <strong>Coverage</strong> shows how much "
        "of the full test set each model has actually run — a high pass@1 on "
        "low coverage is not yet comparable. The 95% CI (Wilson) reflects how "
        "much to trust the score given the sample size.</p>"
    ),
    "coverage": (
        "<p class='desc'>Green bars: pass@1. Blue bars: coverage of the full "
        "case set. A model is only fully comparable once its blue bar reaches "
        "100% — until then its pass@1 is measured on a partial set.</p>"
    ),
    "category": (
        "<p class='desc'>pass@1 per category. Red cells are blind spots, green "
        "cells are reliable areas. Empty cells mean the model has not covered "
        "that category yet.</p>"
    ),
    "sdk": (
        "<p class='desc'>pass@1 grouped by SDK (Zephyr, NXP MCUXpresso, …). "
        "Shows where each model is strong or weak across the firmware "
        "platforms, independent of the individual category mix.</p>"
    ),
    "layer": (
        "<p class='desc'>Pass-rate per evaluation layer, counted only when the "
        "layer was actually reached (skipped layers excluded). Reveals where "
        "models fail: L0 static patterns, L1 compile, L2 runtime, L3 domain "
        "heuristics, L4 mutation.</p>"
    ),
}


# ---------------------------------------------------------------------------
# Data aggregation
# ---------------------------------------------------------------------------

def _run_timestamp(run_dir: Path) -> str:
    """Return the leading timestamp of a run directory name (sortable).

    Run dirs are named ``YYYY-MM-DD_HHMM_<model_slug>``. The first two
    underscore-separated chunks form a lexicographically sortable timestamp.
    """
    parts = run_dir.name.split("_")
    return "_".join(parts[:2]) if len(parts) >= 2 else run_dir.name


def load_model_profiles(results_dir: Path) -> dict[str, dict[str, dict]]:
    """Aggregate every run into one profile per model.

    For each model, walk all runs newest-first and keep the most recent
    detail record per ``case_id`` (a later run supersedes an earlier one for
    the same case). This unions the case coverage across partial runs.

    @return mapping: model -> { case_id -> detail_dict }.
    """
    runs_root = results_dir / "runs"
    if not runs_root.is_dir():
        return {}

    # Newest run first so the first record we see for a case wins.
    run_dirs = sorted(
        (d for d in runs_root.iterdir() if d.is_dir()),
        key=_run_timestamp,
        reverse=True,
    )

    profiles: dict[str, dict[str, dict]] = {}
    for run_dir in run_dirs:
        details_dir = run_dir / "details"
        if not details_dir.is_dir():
            continue
        for detail_file in details_dir.glob("*.json"):
            try:
                rec = json.loads(detail_file.read_text())
            except Exception:
                continue
            model = rec.get("model")
            case_id = rec.get("case_id")
            if not model or not case_id:
                continue
            by_case = profiles.setdefault(model, {})
            # Newest run seen first → do not overwrite with older data.
            by_case.setdefault(case_id, rec)
    return profiles


def count_implemented_cases(cases_dir: Path) -> int:
    """Count every implemented case under cases/, i.e. each metadata.yaml.

    Coverage is measured against ALL implemented cases (whether or not any
    model has run them), so a model that ran the full Zephyr subset but none
    of the NXP cases correctly shows partial coverage. Layout is
    cases/<sdk>/<case_id>/metadata.yaml — a recursive glob also tolerates
    deeper nesting without miscounting.
    """
    if not cases_dir.is_dir():
        return 0
    return sum(1 for _ in cases_dir.glob("*/*/metadata.yaml"))


def _wilson_ci(passed: int, total: int) -> tuple[float, float]:
    """Wilson 95% confidence interval for a binomial proportion.

    Computed locally to avoid a scipy dependency. z = 1.96 (95%).
    Returns (low, high) as fractions in [0, 1]. Empty sample → (0, 0).
    """
    if total == 0:
        return (0.0, 0.0)
    z = 1.96
    phat = passed / total
    denom = 1 + z * z / total
    centre = phat + z * z / (2 * total)
    margin = z * ((phat * (1 - phat) + z * z / (4 * total)) / total) ** 0.5
    low = (centre - margin) / denom
    high = (centre + margin) / denom
    return (max(0.0, low), min(1.0, high))


def _short_model(model: str) -> str:
    """Drop the provider prefix for compact axis labels (groq/x/y -> y)."""
    return model.split("/")[-1]


# ---------------------------------------------------------------------------
# Figure builders — each returns a Plotly Figure
# ---------------------------------------------------------------------------

def _pass_rate(records: list[dict]) -> tuple[int, int]:
    """Return (passed, total) over a list of detail records."""
    total = len(records)
    passed = sum(1 for r in records if r.get("passed"))
    return passed, total


def leaderboard_rows(profiles: dict[str, dict[str, dict]],
                     total_case_count: int) -> list[dict]:
    """Build sorted leaderboard rows with pass@1, coverage, CI, cost, time."""
    rows = []
    for model, by_case in profiles.items():
        records = list(by_case.values())
        passed, total = _pass_rate(records)
        pass_at_1 = passed / total if total else 0.0
        low, high = _wilson_ci(passed, total)
        durations = [r.get("duration_seconds", 0.0) for r in records]
        avg_dur = sum(durations) / len(durations) if durations else 0.0
        cost = sum(r.get("cost_usd", 0.0) or 0.0 for r in records)
        coverage = total / total_case_count if total_case_count else 0.0
        rows.append({
            "model": model,
            "pass_at_1": pass_at_1,
            "ci_low": low,
            "ci_high": high,
            "covered": total,
            "coverage": coverage,
            "avg_duration": avg_dur,
            "cost": cost,
        })
    rows.sort(key=lambda r: r["pass_at_1"], reverse=True)
    return rows


def coverage_figure(rows: list[dict], total_case_count: int) -> go.Figure:
    """Grouped bars: pass@1 vs coverage per model — the headline chart.

    pass@1 = fraction of covered cases that pass.
    coverage = fraction of the full case set the model has run at all.
    A model can have high pass@1 but low coverage; the report must show both.
    """
    models = [_short_model(r["model"]) for r in rows]
    pass_vals = [r["pass_at_1"] * 100 for r in rows]
    cov_vals = [r["coverage"] * 100 for r in rows]

    fig = go.Figure()
    fig.add_bar(
        name="pass@1",
        x=models,
        y=pass_vals,
        marker_color="#48bb78",
        text=[f"{v:.0f}%" for v in pass_vals],
        textposition="outside",
    )
    fig.add_bar(
        name=f"coverage (of {total_case_count} cases)",
        x=models,
        y=cov_vals,
        marker_color="#4299e1",
        text=[f"{v:.0f}%" for v in cov_vals],
        textposition="outside",
    )
    fig.update_layout(
        template="plotly_dark",
        barmode="group",
        title="pass@1 vs test-set coverage",
        yaxis=dict(title="%", range=[0, 110]),
        height=420,
        margin=dict(l=40, r=20, t=60, b=80),
        legend=dict(orientation="h", y=-0.25),
    )
    fig.update_xaxes(tickangle=-30)
    return fig


def _grid_pass_rate(profiles, key_fn) -> tuple[list[str], list[str], list[list]]:
    """Build a (models x keys) pass-rate matrix.

    @param key_fn  maps a detail record to its bucket key (category or sdk).
    @return (models, keys, z) where z[i][j] is pass% or None when the model
            never covered that bucket (rendered as a gap).
    """
    models = sorted(profiles.keys(), key=lambda m: _short_model(m))
    keys: set[str] = set()
    for by_case in profiles.values():
        for rec in by_case.values():
            k = key_fn(rec)
            if k:
                keys.add(k)
    keys_sorted = sorted(keys)

    z: list[list] = []
    for model in models:
        records = list(profiles[model].values())
        row = []
        for k in keys_sorted:
            bucket = [r for r in records if key_fn(r) == k]
            if not bucket:
                row.append(None)  # uncovered → gap cell
            else:
                passed, total = _pass_rate(bucket)
                row.append(round(100 * passed / total, 0))
        z.append(row)
    return [_short_model(m) for m in models], keys_sorted, z


def _heatmap(models, keys, z, title) -> go.Figure:
    """Render a pass-rate heatmap with cell labels."""
    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=keys,
            y=models,
            colorscale=_RDYLGN,
            zmin=0,
            zmax=100,
            text=[["" if v is None else f"{v:.0f}" for v in row] for row in z],
            texttemplate="%{text}",
            textfont=dict(size=11),
            hoverongaps=False,
            colorbar=dict(title="pass %"),
        )
    )
    fig.update_layout(
        template="plotly_dark",
        title=title,
        height=120 + 40 * len(models),
        margin=dict(l=40, r=20, t=60, b=100),
    )
    fig.update_xaxes(tickangle=-45)
    return fig


def category_heatmap(profiles) -> go.Figure:
    """pass@1 heatmap: model x category. Gaps where a model skipped a category."""
    models, keys, z = _grid_pass_rate(profiles, lambda r: r.get("category"))
    return _heatmap(models, keys, z, "pass@1 by category")


def sdk_figure(profiles) -> go.Figure:
    """Per-SDK pass@1 as grouped bars (one group per SDK, one bar per model)."""
    models, sdks, z = _grid_pass_rate(profiles, lambda r: r.get("sdk"))
    fig = go.Figure()
    for i, model in enumerate(models):
        fig.add_bar(
            name=model,
            x=sdks,
            y=z[i],
            text=[("" if v is None else f"{v:.0f}%") for v in z[i]],
            textposition="outside",
        )
    fig.update_layout(
        template="plotly_dark",
        barmode="group",
        title="pass@1 by SDK",
        yaxis=dict(title="pass@1 %", range=[0, 110]),
        height=440,
        margin=dict(l=40, r=20, t=60, b=80),
        legend=dict(orientation="h", y=-0.25),
    )
    return fig


def layer_heatmap(profiles) -> go.Figure:
    """Layer pass-rate heatmap: model x layer.

    A layer counts toward the denominator only when it actually ran (skipped
    layers — ``error`` starting with 'Skipped:' — are excluded), so the cell
    reflects "when this layer was reached, how often did it pass".
    """
    models = sorted(profiles.keys(), key=lambda m: _short_model(m))
    layer_ids = sorted(_LAYER_LABELS.keys())

    z: list[list] = []
    for model in models:
        records = list(profiles[model].values())
        row = []
        for lid in layer_ids:
            reached = 0
            passed = 0
            for rec in records:
                for ly in rec.get("layers") or []:
                    if ly.get("layer") != lid:
                        continue
                    err = ly.get("error") or ""
                    if err.startswith("Skipped:"):
                        continue
                    reached += 1
                    if ly.get("passed"):
                        passed += 1
            row.append(None if reached == 0 else round(100 * passed / reached, 0))
        z.append(row)

    return _heatmap(
        [_short_model(m) for m in models],
        [_LAYER_LABELS[lid] for lid in layer_ids],
        z,
        "Layer pass-rate (when the layer was reached)",
    )


# ---------------------------------------------------------------------------
# HTML assembly
# ---------------------------------------------------------------------------

def _leaderboard_table(rows: list[dict], total_case_count: int) -> str:
    """Render the leaderboard as an HTML table (dashboard CSS classes)."""
    body = ""
    for r in rows:
        body += (
            "<tr>"
            f"<td><strong>{r['model']}</strong></td>"
            f"<td style='text-align:right'>{r['pass_at_1']*100:.1f}%</td>"
            f"<td style='text-align:right'>"
            f"[{r['ci_low']*100:.0f}, {r['ci_high']*100:.0f}]</td>"
            f"<td style='text-align:right'>{r['covered']}/{total_case_count} "
            f"({r['coverage']*100:.0f}%)</td>"
            f"<td style='text-align:right'>{r['avg_duration']:.2f}s</td>"
            f"<td style='text-align:right'>${r['cost']:.4f}</td>"
            "</tr>"
        )
    return (
        "<table><thead><tr>"
        "<th>Model</th><th style='text-align:right'>pass@1</th>"
        "<th style='text-align:right'>95% CI</th>"
        "<th style='text-align:right'>Coverage</th>"
        "<th style='text-align:right'>Avg time</th>"
        "<th style='text-align:right'>Total cost</th>"
        f"</tr></thead><tbody>{body}</tbody></table>"
    )


def _fig_div(fig: go.Figure, include_js: bool) -> str:
    """Render a figure to an HTML div. JS is inlined once (first call)."""
    return pio.to_html(
        fig,
        include_plotlyjs=("inline" if include_js else False),
        full_html=False,
        config={"displayModeBar": False},
    )


def generate_report_body(results_dir: Path, total_case_count: int | None = None,
                         include_plotly_js: bool = True,
                         cases_dir: Path = Path("cases")) -> str:
    """Build the report HTML body (cards + Plotly divs).

    @param total_case_count  size of the full case set; coverage is measured
        against it. When None, defaults to ALL implemented cases under
        cases_dir (not just the ones that have been run).
    @param include_plotly_js  inline plotly.js (True for standalone; False when
        the embedding page already loaded it).
    @param cases_dir  case root used to count implemented cases for coverage.
    """
    profiles = load_model_profiles(results_dir)
    if not profiles:
        return "<div class='card'><p>No runs found in results/runs/.</p></div>"

    if total_case_count is None:
        # Coverage denominator = all implemented cases, even un-run ones.
        # Fall back to the union of run cases if cases/ is missing/empty.
        total_case_count = count_implemented_cases(cases_dir) or len(
            {cid for by_case in profiles.values() for cid in by_case}
        )

    rows = leaderboard_rows(profiles, total_case_count)

    # First fig carries the inlined plotly.js; the rest reuse it.
    figs = [
        coverage_figure(rows, total_case_count),
        category_heatmap(profiles),
        sdk_figure(profiles),
        layer_heatmap(profiles),
    ]
    fig_html = [_fig_div(figs[0], include_plotly_js)]
    fig_html += [_fig_div(f, False) for f in figs[1:]]

    return (
        "<h1>Benchmark Report</h1>"
        f"<div class='card'><h2>Leaderboard</h2>{_DESC['leaderboard']}"
        f"{_leaderboard_table(rows, total_case_count)}</div>"
        f"<div class='card'><h2>Coverage &amp; pass@1</h2>{_DESC['coverage']}"
        f"{fig_html[0]}</div>"
        f"<div class='card'><h2>By category</h2>{_DESC['category']}{fig_html[1]}</div>"
        f"<div class='card'><h2>By SDK</h2>{_DESC['sdk']}{fig_html[2]}</div>"
        f"<div class='card'><h2>By layer</h2>{_DESC['layer']}{fig_html[3]}</div>"
    )


def write_standalone_report(results_dir: Path, output_path: Path,
                            total_case_count: int | None = None,
                            cases_dir: Path = Path("cases")) -> Path:
    """Write a self-contained HTML report file (plotly.js inlined)."""
    body = generate_report_body(results_dir, total_case_count,
                                include_plotly_js=True, cases_dir=cases_dir)
    # Minimal dark styling so the standalone file reads well on its own; the
    # dashboard supplies its own CSS when embedding the body.
    css = (
        "body{font-family:-apple-system,Segoe UI,sans-serif;background:#0f1117;"
        "color:#e2e8f0;max-width:1200px;margin:0 auto;padding:1.5rem;}"
        ".card{background:#1a1d2e;border:1px solid #2d3748;border-radius:8px;"
        "padding:1.25rem;margin-bottom:1rem;}"
        "table{width:100%;border-collapse:collapse;font-size:0.9rem;}"
        "th{background:#2d3748;padding:0.6rem;text-align:left;color:#a0aec0;}"
        "td{padding:0.5rem 0.6rem;border-bottom:1px solid #2d3748;}"
        "h1{font-size:1.4rem;}h2{font-size:1.1rem;margin-bottom:0.5rem;}"
        ".desc{color:#a0aec0;font-size:0.85rem;line-height:1.5;"
        "margin-bottom:1rem;max-width:80ch;}"
        ".desc strong{color:#e2e8f0;}"
    )
    html = (
        "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        f"<title>EmbedEval Report</title><style>{css}</style></head>"
        f"<body>{body}</body></html>"
    )
    output_path.write_text(html)
    return output_path
