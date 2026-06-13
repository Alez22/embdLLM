"""Case-inventory commands: categories, list, sensitivity."""

import logging
from pathlib import Path
from typing import Annotated, Optional

import typer

from embedeval.cli.app import _parse_sdk_filter, app
from embedeval.models import CaseCategory, DifficultyTier

logger = logging.getLogger(__name__)


@app.command(name="categories")
def list_categories(
    cases_dir: Annotated[
        Path,
        typer.Option("--cases", help="Path to cases directory"),
    ] = Path("cases"),
) -> None:
    """List available categories with case counts."""
    from collections import Counter

    from embedeval.runner import discover_cases

    cases = discover_cases(cases_dir)
    if not cases:
        typer.echo("No cases found.")
        raise typer.Exit(code=0)

    cat_counts: Counter[str] = Counter()
    diff_counts: dict[str, Counter[str]] = {}
    for _, meta in cases:
        cat = meta.category.value
        cat_counts[cat] += 1
        diff_counts.setdefault(cat, Counter())[meta.difficulty.value] += 1

    typer.echo(f"{len(cat_counts)} categories, {len(cases)} total cases:\n")
    typer.echo(
        f"  {'Category':<20s} {'Cases':>5s}  {'Easy':>4s} {'Med':>4s} {'Hard':>4s}"
    )
    typer.echo(f"  {'─' * 20} {'─' * 5}  {'─' * 4} {'─' * 4} {'─' * 4}")
    for cat in sorted(cat_counts):
        dc = diff_counts[cat]
        typer.echo(
            f"  {cat:<20s} {cat_counts[cat]:>5d}"
            f"  {dc.get('easy', 0):>4d} {dc.get('medium', 0):>4d}"
            f"  {dc.get('hard', 0):>4d}"
        )




@app.command()
def sensitivity(
    model: Annotated[
        str,
        typer.Argument(help="LLM model identifier"),
    ],
    cases_dir: Annotated[
        Path,
        typer.Option("--cases", help="Path to cases directory"),
    ] = Path("cases"),
    sample: Annotated[
        int,
        typer.Option("--sample", "-s", help="Number of cases to sample (0=all)"),
    ] = 30,
    variants: Annotated[
        int,
        typer.Option("--variants", "-n", help="Number of prompt variants per case"),
    ] = 3,
    seed: Annotated[
        int,
        typer.Option("--seed", help="Random seed for reproducible sampling"),
    ] = 42,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose logging"),
    ] = False,
) -> None:
    """Run prompt sensitivity analysis to measure benchmark robustness."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG, force=True)

    from embedeval.sensitivity import run_sensitivity_analysis

    typer.echo(
        f"Sensitivity analysis: model={model}, sample={sample}, "
        f"variants={variants}, seed={seed}"
    )
    report = run_sensitivity_analysis(
        cases_dir=cases_dir,
        model=model,
        sample_size=sample,
        variants_per_case=variants,
        seed=seed,
    )

    typer.echo(f"\nAvg robustness: {report.avg_robustness:.1%}")
    typer.echo(f"Cases analyzed: {report.total_cases}")

    if report.most_sensitive:
        typer.echo("\nMost sensitive cases:")
        for cid in report.most_sensitive:
            case = next(c for c in report.cases if c.case_id == cid)
            typer.echo(f"  {cid}: robustness={case.robustness:.0%}")

    if report.most_robust:
        typer.echo(f"\nMost robust cases ({len(report.most_robust)}):")
        for cid in report.most_robust[:3]:
            typer.echo(f"  {cid}: robustness=100%")




@app.command(name="list")
def list_cases(
    cases_dir: Annotated[
        Path,
        typer.Option("--cases", help="Path to cases directory"),
    ] = Path("cases"),
    category: Annotated[
        Optional[str],
        typer.Option("--category", "-c", help="Filter by category"),
    ] = None,
    difficulty: Annotated[
        Optional[str],
        typer.Option("--difficulty", "-d", help="Filter by difficulty"),
    ] = None,
    sdk: Annotated[
        Optional[str],
        typer.Option(
            "--sdk",
            help=(
                "Filter by SDK bucket (comma-separated): zephyr, "
                "embedded-linux, freertos, esp-idf, stm32-hal"
            ),
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose logging"),
    ] = False,
) -> None:
    """List available benchmark cases."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG, force=True)

    from embedeval.runner import Filters, discover_cases, filter_cases

    cases = discover_cases(cases_dir)
    filters = Filters()
    if category:
        filters.categories = [CaseCategory(category)]
    if difficulty:
        filters.difficulties = [DifficultyTier(difficulty)]
    if sdk:
        filters.sdks = _parse_sdk_filter(sdk)

    cases = filter_cases(cases, filters)

    if not cases:
        typer.echo("No cases found.")
        raise typer.Exit(code=0)

    typer.echo(f"Found {len(cases)} cases:\n")
    for _case_dir, meta in cases:
        typer.echo(
            f"  [{meta.difficulty.value:6s}] {meta.id:20s} "
            f"{meta.sdk.value:15s} {meta.category.value:15s} — {meta.title}"
        )


