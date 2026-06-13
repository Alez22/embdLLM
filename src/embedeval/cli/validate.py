"""Validation commands: reference solutions and case metadata."""

import logging
from pathlib import Path
from typing import Annotated, Optional

import typer

from embedeval.cli.app import _parse_sdk_filter, app
from embedeval.models import CaseCategory

logger = logging.getLogger(__name__)


@app.command()
def validate(
    cases_dir: Annotated[
        Path,
        typer.Option("--cases", help="Path to cases directory"),
    ] = Path("cases"),
    category: Annotated[
        Optional[str],
        typer.Option("--category", "-c", help="Filter by category"),
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
    """Validate reference solutions for cases."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG, force=True)

    from embedeval.runner import Filters, discover_cases, filter_cases

    cases = discover_cases(cases_dir)
    _filters = Filters()
    if category:
        _filters.categories = [CaseCategory(category)]
    if sdk:
        _filters.sdks = _parse_sdk_filter(sdk)
    if _filters.categories or _filters.sdks:
        cases = filter_cases(cases, _filters)

    if not cases:
        typer.echo("No cases found.")
        raise typer.Exit(code=1)

    from embedeval.evaluator import evaluate

    passed_count = 0
    failed_count = 0

    for case_dir, meta in cases:
        ref_file = case_dir / "reference" / "main.c"
        if not ref_file.is_file():
            typer.echo(f"  SKIP {meta.id}: no reference solution")
            continue

        ref_code = ref_file.read_text(encoding="utf-8")
        result = evaluate(case_dir=case_dir, generated_code=ref_code, model="reference")

        if result.passed:
            typer.echo(f"  PASS {meta.id}")
            passed_count += 1
        else:
            typer.echo(f"  FAIL {meta.id} (layer {result.failed_at_layer})")
            failed_count += 1

    typer.echo(f"\nValidation: {passed_count} passed, {failed_count} failed")


@app.command(name="validate-metadata")
def validate_metadata(
    cases_dir: Annotated[
        Path,
        typer.Option("--cases", help="Path to cases directory"),
    ] = Path("cases"),
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose logging"),
    ] = False,
) -> None:
    """Validate metadata consistency across all cases."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG, force=True)

    from embedeval.runner import discover_cases

    cases = discover_cases(cases_dir)
    if not cases:
        typer.echo("No cases found.")
        raise typer.Exit(code=1)

    warnings: list[str] = []
    for case_dir, meta in cases:
        board = meta.build_board or "native_sim"
        has_cmake = (case_dir / "CMakeLists.txt").is_file()

        # Warn: compilable board target but no CMakeLists.txt
        # and l1_skip not set — possibly misconfigured
        if not meta.l1_skip and not has_cmake and board == "native_sim":
            warnings.append(
                f"  WARN {meta.id}: no CMakeLists.txt and "
                f"l1_skip not set (non-compilable case?)"
            )

        # Warn: compilable case without l1_skip should have
        # reference solution
        if has_cmake and not meta.l1_skip:
            ref = case_dir / "reference" / "main.c"
            if not ref.is_file():
                warnings.append(
                    f"  WARN {meta.id}: compilable case "
                    f"(CMakeLists.txt) but no reference/main.c"
                )

    # Summary by category
    from collections import defaultdict

    by_cat: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "total": 0,
            "l1_skip": 0,
            "l2_skip": 0,
            "hw_board": 0,
        }
    )
    for _, meta in cases:
        cat = meta.category.value
        by_cat[cat]["total"] += 1
        if meta.l1_skip:
            by_cat[cat]["l1_skip"] += 1
        if meta.l2_skip:
            by_cat[cat]["l2_skip"] += 1
        board = meta.build_board or "native_sim"
        if board != "native_sim":
            by_cat[cat]["hw_board"] += 1

    typer.echo("Category Layer Applicability:\n")
    typer.echo(
        f"  {'Category':<20s} {'Total':>5s}  "
        f"{'L1 Skip':>7s} {'L2 Skip':>7s} {'HW Board':>8s}"
    )
    typer.echo(f"  {'─' * 20} {'─' * 5}  {'─' * 7} {'─' * 7} {'─' * 8}")
    for cat in sorted(by_cat):
        c = by_cat[cat]
        typer.echo(
            f"  {cat:<20s} {c['total']:>5d}  "
            f"{c['l1_skip']:>7d} {c['l2_skip']:>7d} "
            f"{c['hw_board']:>8d}"
        )

    if warnings:
        typer.echo(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            typer.echo(w)
    else:
        typer.echo("\nNo metadata warnings.")

    typer.echo(
        f"\nTotal: {len(cases)} cases, "
        f"{sum(c['l1_skip'] for c in by_cat.values())} l1_skip, "
        f"{sum(c['l2_skip'] for c in by_cat.values())} l2_skip"
    )


