"""Miscellaneous commands: agent, guide, tui."""

import json
import logging
from pathlib import Path
from typing import Annotated, Optional

import typer

from embedeval.cli.app import _parse_sdk_filter, app
from embedeval.models import CaseCategory, EvalResult

logger = logging.getLogger(__name__)


@app.command()
def agent(
    model: Annotated[
        str,
        typer.Argument(help="LLM model identifier"),
    ],
    cases_dir: Annotated[
        Path,
        typer.Option("--cases", "-d", help="Path to cases directory"),
    ] = Path("cases"),
    max_turns: Annotated[
        int,
        typer.Option("--max-turns", "-t", help="Maximum agent turns per case"),
    ] = 5,
    category: Annotated[
        Optional[list[str]],
        typer.Option("--category", "-c", help="Filter by category (repeatable)"),
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
    context_pack: Annotated[
        Optional[str],
        typer.Option(
            "--context-pack",
            help=(
                "Run-wide context prepended to every turn. Path to a file, "
                "or 'expert' for the bundled pack. "
                "See docs/CONTEXT-QUALITY-MODE.md."
            ),
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose logging"),
    ] = False,
) -> None:
    """Run benchmark in multi-turn agent mode with error feedback."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG, force=True)

    from embedeval.agent import evaluate_agent
    from embedeval.runner import Filters, discover_cases, filter_cases

    # Agent mode does not write to a tracker, so no hash-mismatch
    # enforcement is needed; just resolve and load the pack content.
    context_pack_text: str | None = None
    if context_pack is not None:
        from embedeval.context_pack import resolve_context_pack

        try:
            pack_path = resolve_context_pack(context_pack)
            context_pack_text = pack_path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            typer.echo(f"Error: {exc}", err=True)
            raise typer.Exit(code=1) from exc
        if not context_pack_text.strip():
            typer.echo(
                f"Error: context pack file is empty or whitespace-only: {pack_path}",
                err=True,
            )
            raise typer.Exit(code=1)
        typer.echo(f"Context pack: {pack_path.name} ({len(context_pack_text)} chars)")

    cases = discover_cases(cases_dir)
    filters = Filters()
    if category:
        filters.categories = [CaseCategory(c) for c in category]
    if sdk:
        filters.sdks = _parse_sdk_filter(sdk)
    cases = filter_cases(cases, filters)

    if not cases:
        typer.echo("No cases found.")
        raise typer.Exit(code=1)

    typer.echo(
        f"Agent mode: model={model}, max_turns={max_turns}, cases={len(cases)}\n"
    )

    from embedeval.runner import _load_prompt

    passed = 0
    failed = 0
    for case_dir, meta in cases:
        prompt = _load_prompt(case_dir)
        result = evaluate_agent(
            case_dir=case_dir,
            model=model,
            prompt=prompt,
            max_turns=max_turns,
            context_pack=context_pack_text,
        )
        status = "PASS" if result.passed else "FAIL"
        turns_info = f"turn {result.turns_used}/{result.max_turns}"
        typer.echo(f"  [{status}] {meta.id:30s} ({turns_info})")
        if result.passed:
            passed += 1
        else:
            failed += 1

    total = passed + failed
    pass_rate = passed / total if total > 0 else 0.0
    typer.echo(f"\nAgent results: {passed}/{total} passed ({pass_rate:.1%})")




@app.command()
def guide(
    results_dir: Annotated[
        Path,
        typer.Option("--results", help="Directory containing result JSON files"),
    ] = Path("results"),
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Output Safety Guide path"),
    ] = Path("SAFETY-GUIDE.md"),
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose logging"),
    ] = False,
) -> None:
    """Generate LLM Embedded Code Safety Guide from benchmark results."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG, force=True)

    from embedeval.safety_guide import generate_safety_guide

    # Load results from run archive detail files
    all_results: list[EvalResult] = []
    for run_dir in sorted(results_dir.glob("runs/*")):
        details_dir = run_dir / "details"
        if not details_dir.is_dir():
            continue
        for detail_file in sorted(details_dir.glob("*.json")):
            try:
                data = json.loads(detail_file.read_text(encoding="utf-8"))
                all_results.append(EvalResult(**data))
            except Exception:
                continue

    if not all_results:
        typer.echo("No benchmark results found. Run a benchmark first.")
        raise typer.Exit(code=1)

    generate_safety_guide(all_results, output)
    typer.echo(f"Safety Guide written to {output}")




@app.command()
def tui(
    results_dir: Annotated[
        Path,
        typer.Option("--results", help="Directory containing run results"),
    ] = Path("results"),
    cases_dir: Annotated[
        Path,
        typer.Option("--cases", help="Path to cases directory"),
    ] = Path("cases"),
) -> None:
    """Start the Textual TUI dashboard."""
    from embedeval.tui import EmbedEvalTUI
    from embedeval.tui import config as _tui_config

    # Override the module-level paths before the app reads them at runtime.
    _tui_config.RESULTS_DIR = results_dir.resolve()
    _tui_config.CASES_DIR = cases_dir.resolve()

    app = EmbedEvalTUI()
    app.run()


