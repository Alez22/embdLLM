"""Miscellaneous commands: agent, guide, tui."""

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Optional

import typer

from embedeval.cli.app import _parse_sdk_filter, app
from embedeval.models import CaseCategory, EvalResult

if TYPE_CHECKING:
    from embedeval.agent import AgentResult

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
                "or a bundled keyword ('expert', 'nxp'). "
                "See docs/CONTEXT-QUALITY-MODE.md."
            ),
        ),
    ] = None,
    temperature: Annotated[
        float,
        typer.Option(
            "--temperature",
            help="LLM temperature (recorded in agent_run.json metadata)",
        ),
    ] = 0.0,
    resume: Annotated[
        Optional[Path],
        typer.Option(
            "--resume",
            help=(
                "Continue a previous agent run directory: cases that already "
                "passed are copied as-is (0 LLM calls); failed cases resume "
                "from turn N+1 up to the new --max-turns."
            ),
        ),
    ] = None,
    output_dir: Annotated[
        Path,
        typer.Option("--output-dir", "-o", help="Directory for run archives"),
    ] = Path("results"),
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
    context_pack_name: str | None = None
    context_pack_hash: str | None = None
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
        # Record pack identity (name + short content hash) so the dashboard
        # can separate with-pack from without-pack runs.
        import hashlib

        context_pack_name = pack_path.name
        context_pack_hash = hashlib.sha256(
            context_pack_text.encode("utf-8")
        ).hexdigest()[:12]
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

    # --- resume: load prior run so we can skip already-passed cases ---
    from embedeval.agent import AgentResult
    from embedeval.agent_report import (
        build_run_dir,
        load_agent_run,
        write_agent_run,
    )

    resumed_from: str | None = None
    prior_by_case: dict[str, AgentResult] = {}
    if resume is not None:
        archive = load_agent_run(resume)
        resumed_from = str(resume)
        prior_by_case = {r.case_id: r for r in archive.results}
        if max_turns <= archive.max_turns:
            typer.echo(
                f"Warning: --max-turns {max_turns} <= resumed run's "
                f"{archive.max_turns}; no extra turns will be run.",
                err=True,
            )

    typer.echo(
        f"Agent mode: model={model}, max_turns={max_turns}, "
        f"cases={len(cases)}{' (resume)' if resume else ''}\n"
    )

    from embedeval.runner import _load_prompt

    results: list[AgentResult] = []
    passed = 0
    failed = 0
    for case_dir, meta in cases:
        prior = prior_by_case.get(meta.id)
        if prior is not None and prior.passed:
            # Already solved in the resumed run: copy, 0 LLM calls.
            result = prior
            note = " (cached)"
        else:
            prompt = _load_prompt(case_dir)
            start_turn, initial_context, prior_history = _resume_state(prior)
            result = evaluate_agent(
                case_dir=case_dir,
                model=model,
                prompt=prompt,
                max_turns=max_turns,
                context_pack=context_pack_text,
                start_turn=start_turn,
                initial_context=initial_context,
                prior_history=prior_history,
            )
            note = " (resumed)" if prior is not None else ""

        results.append(result)
        status = "PASS" if result.passed else "FAIL"
        turns_info = f"turn {result.turns_used}/{result.max_turns}"
        typer.echo(f"  [{status}] {meta.id:30s} ({turns_info}){note}")
        if result.passed:
            passed += 1
        else:
            failed += 1

    total = passed + failed
    pass_rate = passed / total if total > 0 else 0.0

    run_dir = build_run_dir(output_dir, model, max_turns)
    out_path = write_agent_run(
        run_dir=run_dir,
        model=model,
        max_turns=max_turns,
        temperature=temperature,
        results=results,
        resumed_from=resumed_from,
        context_pack_name=context_pack_name,
        context_pack_hash=context_pack_hash,
    )

    typer.echo(f"\nAgent results: {passed}/{total} passed ({pass_rate:.1%})")
    typer.echo(f"Archive: {out_path}")


def _resume_state(
    prior: "AgentResult | None",
) -> tuple[int, list[str], list[EvalResult]]:
    """@brief Build evaluate_agent resume args from a prior failed case.

    Reconstructs the accumulated error context exactly as the agent loop
    would have, so the next turn sees the same feedback. Returns
    (start_turn, initial_context, prior_history); start_turn==1 with empty
    state when there is nothing to resume from.

    @param prior Prior AgentResult for this case, or None for a fresh case.
    """
    if prior is None or not prior.history:
        return 1, [], []

    context: list[str] = []
    for turn, res in enumerate(prior.history, start=1):
        if res.failed_at_layer is None:
            continue
        layer = res.layers[res.failed_at_layer]
        error_summary = layer.error or ""
        failed_checks = [
            f"- {d.check_name}: expected={d.expected}, actual={d.actual}"
            for d in layer.details
            if not d.passed
        ]
        context.append(
            f"Turn {turn} failed at {layer.name}:\n"
            f"{error_summary}\n" + "\n".join(failed_checks[:5])
        )

    start_turn = len(prior.history) + 1
    return start_turn, context, list(prior.history)




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


