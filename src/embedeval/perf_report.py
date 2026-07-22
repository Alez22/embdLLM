"""Generate the non-agentic performance report (NXP vs Zephyr).

Exposed as the `embedeval perf-report` CLI command (see cli/report.py);
outputs land in <results>/reports/.

Aggregation (`load_groups`, the canonical implementation — it used to mirror
the TUI leaderboard, which has since been replaced by a run history): all
`generation` runs are merged, grouped by (model, temperature, no_think,
attempts); within a group the last-written record per case_id wins. The
reported rate is that config's pass-rate over the cases it covers.

Charts follow the dataviz skill: single-hue magnitude bars, recessive axes,
direct value labels, fixed categorical hues only where NXP/Zephyr differ.
"""
import json
from pathlib import Path

import matplotlib

# Headless backend must be selected before pyplot is imported.
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# --- design tokens (dataviz reference palette, light surface) ---
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, AQUA, MUTED = "#2a78d6", "#1baf7a", "#c3c2b7"
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "font.size": 11,
    "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2,
    "ytick.color": INK2, "axes.edgecolor": GRID,
})


def load_groups(runs_dir: Path):
    """Union-of-runs grouping by (model, temp, no_think, attempts), per-SDK."""
    groups = {}  # (model,temp,nt,att) -> {case_id: {passed, sdk}}
    for run_dir in sorted(runs_dir.iterdir()):
        sf = run_dir / "summary.json"
        if not sf.is_file():
            continue
        try:
            s = json.loads(sf.read_text())
        except Exception:
            continue
        model = s.get("model", "")
        if model == "mock" or not model or s.get("scenario") != "generation":
            continue
        gp = s.get("generation_params", {})
        key = (model, float(s.get("temperature", 0.0)),
               bool(gp.get("no_think", False)), int(s.get("n_samples_per_case", 1)))
        cases = groups.setdefault(key, {})
        dd = run_dir / "details"
        if not dd.is_dir():
            continue
        for f in dd.glob("*.json"):
            try:
                d = json.loads(f.read_text())
            except Exception:
                continue
            cid = d.get("case_id") or f.stem
            cases[cid] = {"passed": bool(d.get("passed")), "sdk": d.get("sdk", "")}
    return groups


def rows_for(groups, sdk):
    out = []
    for (model, temp, nt, att), cases in groups.items():
        passed = tested = 0
        for info in cases.values():
            if info["sdk"] != sdk:
                continue
            tested += 1
            passed += info["passed"]
        if tested:
            out.append(dict(model=model, temp=temp, att=att,
                            passed=passed, tested=tested, rate=passed / tested))
    return sorted(out, key=lambda r: r["rate"], reverse=True)


def short(m):
    return m.split("/", 1)[1] if "/" in m else m


def label(r):
    return f"{short(r['model'])}  (t{r['temp']}·a{r['att']})"


def hbar(rows, title, subtitle, bar_color, path, figh, cov_by_model=None):
    """Check-coverage leaderboard. The primary (coloured) bar is check-coverage —
    it ranks the models, since on hard SDKs pass-rate is mostly zero and coverage
    is what discriminates. The pass-rate is overlaid as a narrower dark bar (the
    fraction of coverage that turned into a full pass). Rows without a coverage
    reading fall to the bottom, ranked by pass-rate."""
    def cov_of(r):
        return cov_by_model.get(r["model"]) if cov_by_model is not None else None

    # rank by coverage (primary); rows with no coverage sink below, by pass-rate
    rows = sorted(rows, key=lambda r: (cov_of(r) is not None,
                                       cov_of(r) if cov_of(r) is not None else r["rate"]))
    fig, ax = plt.subplots(figsize=(10, figh))
    y = range(len(rows))
    colors = [bar_color(r) for r in rows]
    # primary bar = coverage (fallback to pass-rate when coverage is n/a)
    ax.barh(y, [cov_of(r) if cov_of(r) is not None else r["rate"] for r in rows],
            color=colors, height=0.66, zorder=2, edgecolor=SURFACE, linewidth=1.5)
    # secondary bar = pass-rate, narrower and darker, sitting inside the cov bar
    ax.barh(y, [r["rate"] for r in rows], color=INK2, height=0.30, zorder=3)
    ax.set_yticks(list(y))
    ax.set_yticklabels([label(r) for r in rows], fontsize=8.5)
    ax.set_xlim(0, 1.35)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    for i, r in enumerate(rows):
        cov = cov_of(r)
        end = max(r["rate"], cov or 0.0)
        cov_txt = f"{cov*100:.0f}% cov" if cov is not None else "cov n/a"
        ax.text(end + 0.012, i,
                f"{cov_txt} · {r['rate']*100:.0f}% pass  ({r['passed']}/{r['tested']})",
                va="center", ha="left", fontsize=8, color=INK2)
    ax.set_xlabel("coloured bar = check-coverage (ranks) · dark bar = pass-rate",
                  fontsize=9.5)
    ax.grid(axis="x", color=GRID, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    fig.suptitle(title, fontsize=14, fontweight="bold", color=INK, x=0.02, ha="left", y=0.98)
    fig.text(0.02, 0.925, subtitle, fontsize=9, color=INK2, ha="left", va="top")
    fig.subplots_adjust(left=0.38, right=0.97, top=0.86, bottom=0.11)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def consistency_rows(runs_dir: Path, sdk):
    """One row per model: pass@1/3/5 from its richest temp=0.5, attempts=5 run.

    Uses the project's official consistency metric (Chen et al. 2021 pass@k,
    already stored in each summary as pass_at_1/3/5). We pick, per model, the
    a5·t0.5 summary that covers the most cases of this SDK — the sturdiest
    denominator. pass@5 − pass@1 is the flakiness (larger = more sampling-luck).
    """
    best = {}  # model -> (n_cases, p1, p3, p5)
    for run_dir in sorted(runs_dir.iterdir()):
        sf = run_dir / "summary.json"
        if not sf.is_file():
            continue
        try:
            s = json.loads(sf.read_text())
        except Exception:
            continue
        if (s.get("scenario") != "generation"
                or s.get("n_samples_per_case") != 5
                or float(s.get("temperature", 0.0)) != 0.5):
            continue
        # only keep summaries whose cases are (majority) this SDK
        sdk_scores = {e["sdk"]: e for e in s.get("sdk_scores", [])}
        if sdk not in sdk_scores:
            continue
        for m in s.get("models", []):
            model = m.get("model", "")
            n = m.get("total_cases", 0) or 0
            # attribute the summary to this SDK only if the run is single-SDK,
            # otherwise pass@k mixes SDKs — skip mixed runs for a clean metric
            if len(sdk_scores) != 1:
                continue
            row = (n, m.get("pass_at_1", 0.0), m.get("pass_at_3", 0.0),
                   m.get("pass_at_5", 0.0), m.get("check_coverage", 0.0))
            if model not in best or row[0] > best[model][0]:
                best[model] = row
    rows = [dict(model=k, n=v[0], p1=v[1], p3=v[2], p5=v[3], cov=v[4])
            for k, v in best.items()]
    return sorted(rows, key=lambda r: r["p5"])


def dumbbell(rows, title, subtitle, path, figh,
             lo="p1", hi="p5", hi_color=BLUE, xlabel=None, sort_key=None):
    """Generic lo→hi dumbbell; segment length = the gap between the two metrics.

    Defaults draw pass@1 → pass@5 (consistency). Pass lo/hi to draw other pairs,
    e.g. lo='p1', hi='cov' for pass-rate → check-coverage."""
    rows = sorted(rows, key=sort_key or (lambda r: r[hi]))
    fig, ax = plt.subplots(figsize=(10, figh))
    y = range(len(rows))
    for i, r in enumerate(rows):
        a, b = r[lo], r[hi]
        ax.plot([a, b], [i, i], color=GRID, linewidth=3,
                solid_capstyle="round", zorder=2)
        ax.scatter(a, i, s=70, color=MUTED, zorder=3,
                   edgecolor=SURFACE, linewidth=1.5)      # lower metric
        ax.scatter(b, i, s=70, color=hi_color, zorder=4,
                   edgecolor=SURFACE, linewidth=1.5)      # higher metric
        ax.text(max(a, b) + 0.02, i,
                f"{a*100:.0f}→{b*100:.0f}%  (Δ{(b-a)*100:.0f}, n={r['n']})",
                va="center", ha="left", fontsize=8.5, color=INK2)
    ax.set_yticks(list(y))
    ax.set_yticklabels([short(r["model"]) for r in rows], fontsize=8.5)
    ax.set_xlim(0, 1.25)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel(xlabel or "pass-rate — grey ● pass@1, blue ● pass@5 (Δ = flakiness)",
                  fontsize=9.5)
    ax.grid(axis="x", color=GRID, zorder=0)
    ax.set_axisbelow(True)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(length=0)
    fig.suptitle(title, fontsize=14, fontweight="bold", color=INK, x=0.02, ha="left", y=0.98)
    fig.text(0.02, 0.925, subtitle, fontsize=9, color=INK2, ha="left", va="top")
    fig.subplots_adjust(left=0.30, right=0.97, top=0.86, bottom=0.11)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def generate_performance_report(results_dir: Path) -> Path:
    """@brief Build the NXP-vs-Zephyr PNG figures + data JSON under <results>/reports/.

    @param results_dir Results root containing runs/.
    @return The reports directory the artifacts were written to.
    """
    runs_dir = results_dir / "runs"
    out = results_dir / "reports"
    out.mkdir(parents=True, exist_ok=True)
    groups = load_groups(runs_dir)

    # Both views compare like-for-like sampling: temperature=0.5, attempts=5 only.
    # For NXP this drops the strongest a1 probe rows (Opus, qwen3-235b-2507,
    # deepseek); those are tracked for a fresh a5 run in NXP_RERUN_CANDIDATES.md.
    def canonical(r):
        return r["att"] == 5 and r["temp"] == 0.5

    nxp = [r for r in rows_for(groups, "mcuxpresso-sdk") if canonical(r)]
    zep = [r for r in rows_for(groups, "zephyr") if canonical(r)]

    # colour = SDK identity only; the ranking is carried by bar length (coverage).
    def nxp_color(r):
        return BLUE

    def zep_color(r):
        return AQUA

    # check-coverage per model (richest a5·t0.5 single-SDK run) — reused below.
    zep_cons = consistency_rows(runs_dir, "zephyr")
    nxp_cons = consistency_rows(runs_dir, "mcuxpresso-sdk")
    zep_cov = {r["model"]: r["cov"] for r in zep_cons}
    nxp_cov = {r["model"]: r["cov"] for r in nxp_cons}

    hbar(nxp, "NXP MCUXpresso — ranked by check-coverage",
         "temp=0.5 · attempts=5. Bar = check-coverage (ranks); dark inset = pass-rate. "
         "Best a1 rows excluded (see re-run checklist).",
         nxp_color, out / "report_nxp_pass1.png", 3.2, cov_by_model=nxp_cov)
    hbar(zep, "Zephyr RTOS — ranked by check-coverage",
         "temp=0.5 · attempts=5. Bar = check-coverage (ranks); dark inset = pass-rate.",
         zep_color, out / "report_zephyr_pass1.png", 5.4, cov_by_model=zep_cov)

    # difficulty gap on the primary metric = check-coverage (from richest runs)
    def cov_stats(cons_rows):
        vals = sorted(r["cov"] for r in cons_rows)
        n = len(vals)
        med = vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2
        return max(vals), med, n

    nxp_best, nxp_med, nxp_n = cov_stats(nxp_cons)
    zep_best, zep_med, zep_n = cov_stats(zep_cons)

    fig, ax = plt.subplots(figsize=(7.5, 4))
    x = range(2)
    w = 0.36
    ax.bar([i - w / 2 for i in x], [nxp_best, nxp_med], w, color=BLUE, zorder=3,
           edgecolor=SURFACE, linewidth=1.5, label=f"NXP (n={nxp_n} models)")
    ax.bar([i + w / 2 for i in x], [zep_best, zep_med], w, color=AQUA, zorder=3,
           edgecolor=SURFACE, linewidth=1.5, label=f"Zephyr (n={zep_n} models)")
    for i, v in enumerate([nxp_best, nxp_med]):
        ax.text(i - w / 2, v + 0.015, f"{v*100:.0f}%", ha="center", fontsize=10, color=INK)
    for i, v in enumerate([zep_best, zep_med]):
        ax.text(i + w / 2, v + 0.015, f"{v*100:.0f}%", ha="center", fontsize=10, color=INK)
    ax.set_xticks(list(x))
    ax.set_xticklabels(["Best model", "Median model"])
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("check-coverage")
    ax.grid(axis="y", color=GRID, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.set_title("Difficulty gap: NXP bare-metal vs Zephyr (check-coverage)", fontsize=14,
                 fontweight="bold", color=INK, loc="left", pad=18)
    ax.text(0, 1.02, "Best/median check-coverage per SDK. Even on coverage, NXP trails Zephyr.",
            transform=ax.transAxes, fontsize=9.5, color=INK2, va="bottom")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    fig.subplots_adjust(left=0.10, right=0.97, top=0.82, bottom=0.10)
    fig.savefig(out / "report_difficulty_gap.png", dpi=150)
    plt.close(fig)

    # consistency (pass@1 → pass@5) — reuses zep_cons/nxp_cons from above
    dumbbell(zep_cons, "Zephyr — consistency (pass@1 → pass@5)",
             "temp=0.5 · attempts=5, per model. Short Δ = stable; "
             "long Δ = needs multiple tries (flaky).",
             out / "report_zephyr_consistency.png", 5.0)
    if nxp_cons:
        dumbbell(nxp_cons, "NXP — consistency (pass@1 → pass@5)",
                 "temp=0.5 · attempts=5, per model. Short Δ = stable; long Δ = flaky.",
                 out / "report_nxp_consistency.png", max(3.2, 0.5 * len(nxp_cons) + 1.2))

    # check-coverage gap: pass@1 (blue) → check-coverage (aqua). Long Δ = the model
    # writes mostly-correct code but misses the last checks ("near-miss").
    cov_xlabel = "grey ● pass@1, aqua ● check-coverage (Δ = near-miss gap)"
    dumbbell(zep_cons, "Zephyr — check-coverage vs pass-rate",
             "temp=0.5 · attempts=5, per model. Long Δ = many checks satisfied "
             "but case not fully passed.",
             out / "report_zephyr_coverage.png", 5.0,
             lo="p1", hi="cov", hi_color=AQUA, xlabel=cov_xlabel,
             sort_key=lambda r: r["cov"])
    if nxp_cons:
        dumbbell(nxp_cons, "NXP — check-coverage vs pass-rate",
                 "temp=0.5 · attempts=5, per model. Long Δ = mostly-correct code "
                 "missing the last implicit-knowledge checks.",
                 out / "report_nxp_coverage.png", max(3.2, 0.5 * len(nxp_cons) + 1.2),
                 lo="p1", hi="cov", hi_color=AQUA, xlabel=cov_xlabel,
                 sort_key=lambda r: r["cov"])

    json.dump({"nxp": nxp, "zephyr": zep,
               "gap": {"nxp": [nxp_best, nxp_med, nxp_n],
                       "zephyr": [zep_best, zep_med, zep_n]},
               "consistency": {"zephyr": zep_cons, "nxp": nxp_cons}},
              open(out / "_report_data.json", "w"), indent=1)
    print("NXP rows:", len(nxp), "Zephyr rows:", len(zep),
          "| consistency zep:", len(zep_cons), "nxp:", len(nxp_cons))
    print(f"gap NXP best={nxp_best:.2f} med={nxp_med:.2f} | "
          f"Zephyr best={zep_best:.2f} med={zep_med:.2f}")
    return out


if __name__ == "__main__":
    generate_performance_report(Path("results"))
