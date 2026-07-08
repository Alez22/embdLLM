"""Render the agent leaderboard as a static Markdown report + PNG figure.

Audience: the Powersoft local-deploy decision. The report ranks models on the
multi-turn agent probe, flags which ones can run on local infrastructure, and
calls out the RT1170 IOMUXC block — the case family that discriminates the
ranking (see the agent-mode findings).
"""

from __future__ import annotations

from pathlib import Path

from embedeval.agent_summary import ModelSummary, build_leaderboard

# The RT1170 IOMUXC cases are the ranking discriminator: most models apply the
# Kinetis/STM32 3-arg pin-mux mental model and never close them.
_RT1170_PREFIX = "nxp-rt1170"


def _short_model(model: str) -> str:
    """Drop the provider prefix for compact display (openrouter/z-ai/glm-5.2 -> glm-5.2)."""
    return model.rsplit("/", 1)[-1]


def _fmt_recovery(rate: float | None) -> str:
    return "—" if rate is None else f"{rate * 100:.0f}%"


def _rt1170_cases(rows: list[ModelSummary]) -> list[str]:
    """Sorted list of RT1170 case ids present in any run."""
    cases: set[str] = set()
    for row in rows:
        cases.update(
            c for c in row.passed_at_turn if c.startswith(_RT1170_PREFIX)
        )
    return sorted(cases)


def _leaderboard_table(rows: list[ModelSummary]) -> str:
    """@brief Main ranking table."""
    # Cost column is intentionally omitted: OpenRouter/Groq via litellm do not
    # report cost_usd, so it is always 0. Tokens are real and act as a relative
    # cost proxy. Re-add cost only if a provider starts populating it.
    lines = [
        "| # | model | pass | recovery | local? | provider | tokens |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, start=1):
        local = "✅" if r.is_open_weight else "❌ cloud"
        lines.append(
            f"| {i} | `{_short_model(r.model)}` | {r.passed}/{r.total} | "
            f"{_fmt_recovery(r.recovery_rate)} | {local} | {r.provider} | "
            f"{r.total_tokens:,} |"
        )
    return "\n".join(lines)


def _rt1170_table(rows: list[ModelSummary]) -> str:
    """@brief RT1170 discriminator: turn-of-pass per model, or ✗ if never."""
    cases = _rt1170_cases(rows)
    if not cases:
        return "_No RT1170 cases in these runs._"

    short_cases = [c.replace(_RT1170_PREFIX + "-", "") for c in cases]
    header = "| model | " + " | ".join(short_cases) + " | closed |"
    sep = "|---|" + "|".join(["---"] * len(cases)) + "|---|"
    lines = [header, sep]
    for r in rows:
        cells = []
        closed = 0
        for c in cases:
            turn = r.passed_at_turn.get(c)
            if turn is None:
                cells.append("✗")
            else:
                cells.append(f"t{turn}")
                closed += 1
        lines.append(
            f"| `{_short_model(r.model)}` | " + " | ".join(cells)
            + f" | {closed}/{len(cases)} |"
        )
    return "\n".join(lines)


def _recommendation(rows: list[ModelSummary]) -> str:
    """@brief Deploy recommendation: best open-weight model wins."""
    deployable = [r for r in rows if r.is_open_weight]
    if not deployable:
        return "_No open-weight (locally deployable) model in these runs._"
    best = deployable[0]  # rows already sorted best-first
    cloud_best = next((r for r in rows if not r.is_open_weight), None)
    note = ""
    if cloud_best is not None:
        note = (
            f" It beats the best cloud-only reference "
            f"(`{_short_model(cloud_best.model)}`, {cloud_best.passed}/{cloud_best.total}), "
            "while staying deployable on local infrastructure."
        )
    return (
        f"**Recommended for local deploy: `{_short_model(best.model)}`** "
        f"({best.passed}/{best.total}, provider {best.provider}).{note}"
    )


def _run_conditions(rows: list[ModelSummary]) -> str:
    """@brief Footer with the experimental conditions for reproducibility."""
    if not rows:
        return ""
    sample = rows[0]
    pack = sample.context_pack or "none"
    return (
        f"- Turn budget: t{sample.max_turns}  ·  context pack: `{pack}`\n"
        f"- Gates: L0 (static) + L1 (arm-none-eabi-gcc compile) + L3 (behavior), "
        "container mode only\n"
        f"- Cases: {sample.total} NXP bare-metal (MCXC + RT1170)\n"
        "- Latest container run per (model, turns, pack); host-mode runs excluded"
    )


def render_markdown(rows: list[ModelSummary], figure_name: str | None) -> str:
    """@brief Assemble the full Markdown report."""
    parts = [
        "# Agent Mode Leaderboard — NXP Bare-Metal",
        "",
        "Multi-turn agent probe with compile-error feedback. "
        "Audience: Powersoft local-deploy decision.",
        "",
        "## Ranking",
        "",
        _leaderboard_table(rows),
        "",
        "## The RT1170 discriminator",
        "",
        "The RT1170 `IOMUXC_SetPinMux` 5-arg tuple-macro idiom is what separates "
        "the field: models that apply the Kinetis/STM32 3-arg pin-mux model never "
        "close these cases. Turn each model closed each case (✗ = never):",
        "",
        _rt1170_table(rows),
        "",
        "## Recommendation",
        "",
        _recommendation(rows),
    ]
    if figure_name:
        parts += ["", "## Pass-by-turn matrix", "", f"![Agent pass matrix]({figure_name})"]
    parts += ["", "## Run conditions", "", _run_conditions(rows), ""]
    return "\n".join(parts)


def render_figure(rows: list[ModelSummary], out_path: Path) -> bool:
    """@brief Render a model×case heatmap colored by turn-of-pass.

    Green (early pass) → yellow (late pass) → red (never). Returns False if
    matplotlib is not installed (optional dependency; the Markdown report is
    generated regardless).
    """
    try:
        import matplotlib

        matplotlib.use("Agg")  # headless: no display needed in container/CLI
        import matplotlib.pyplot as plt
        from matplotlib.colors import BoundaryNorm, ListedColormap
    except ImportError:
        return False

    if not rows:
        return False

    # All case ids across runs, MCXC first then RT1170, stable order.
    case_ids = sorted(
        {c for r in rows for c in r.passed_at_turn},
        key=lambda c: (c.startswith(_RT1170_PREFIX), c),
    )
    max_turns = max((r.max_turns for r in rows), default=5)

    # Cell value: turn-of-pass (1..max_turns), or max_turns+1 for "never".
    never = max_turns + 1
    grid = [
        [(r.passed_at_turn.get(c) or never) for c in case_ids] for r in rows
    ]

    # Discrete colormap: turn 1 = darkest green … last turn = yellow, never = red.
    greens = plt.cm.YlGn(
        [0.9 - 0.6 * (t / max(max_turns - 1, 1)) for t in range(max_turns)]
    )
    colors = list(greens) + [(0.8, 0.1, 0.1, 1.0)]  # red for "never"
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(list(range(1, never + 2)), cmap.N)

    fig_h = max(2.0, 0.5 * len(rows))
    fig_w = max(6.0, 0.7 * len(case_ids))
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.imshow(grid, cmap=cmap, norm=norm, aspect="auto")

    ax.set_xticks(range(len(case_ids)))
    ax.set_xticklabels(
        [c.replace("nxp-", "") for c in case_ids], rotation=45, ha="right", fontsize=8
    )
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([_short_model(r.model) for r in rows], fontsize=9)

    # Annotate each cell with t<N> or ✗.
    for y, r in enumerate(rows):
        for x, c in enumerate(case_ids):
            turn = r.passed_at_turn.get(c)
            label = f"t{turn}" if turn else "✗"
            ax.text(x, y, label, ha="center", va="center", fontsize=7)

    ax.set_title("Agent pass-by-turn (green=early, red=never)", fontsize=10)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return True


def generate_agent_report(
    results_dir: Path, output_md: Path, figure_path: Path
) -> tuple[bool, int]:
    """@brief Generate the Markdown report and (optionally) the PNG figure.

    @return (figure_written, model_count). figure_written is False when
        matplotlib is absent or there is nothing to plot.
    """
    rows = build_leaderboard(results_dir)
    figure_written = render_figure(rows, figure_path) if rows else False
    md = render_markdown(rows, figure_path.name if figure_written else None)
    output_md.write_text(md, encoding="utf-8")
    return figure_written, len(rows)
