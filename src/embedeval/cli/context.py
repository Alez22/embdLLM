"""Context-window comparison and diagnostic commands."""

import logging
from pathlib import Path
from typing import Annotated, Optional

import typer

from embedeval.cli.app import app
from embedeval.context_diagnose import DEFAULT_GAP_THRESHOLD_PP

logger = logging.getLogger(__name__)


@app.command(name="context-compare")
def context_compare_cmd(
    bare: Annotated[
        Path,
        typer.Option("--bare", help="output_dir of the no-pack baseline run"),
    ],
    expert: Annotated[
        Path,
        typer.Option(
            "--expert",
            help="output_dir of the run with --context-pack expert",
        ),
    ],
    team: Annotated[
        Optional[Path],
        typer.Option(
            "--team", help="output_dir of the run with --context-pack <team file>"
        ),
    ] = None,
    model: Annotated[
        Optional[str],
        typer.Option(
            "--model",
            help="Model to compare. Required when trackers contain multiple models.",
        ),
    ] = None,
    output_json: Annotated[
        Optional[Path],
        typer.Option("--output-json", help="Write the comparison report to JSON"),
    ] = None,
    include_team_effect: Annotated[
        bool,
        typer.Option(
            "--include-team-effect",
            help=(
                "Also classify bare→team per-case effect in JSON output. "
                "Default off — bare→expert is the dominant question."
            ),
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose logging"),
    ] = False,
) -> None:
    """Compare benchmark runs across context packs (Context Quality Mode)."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG, force=True)

    from embedeval.context_compare import (
        compare_runs,
        format_comparison_table,
    )

    if include_team_effect and team is None:
        typer.echo(
            "Error: --include-team-effect requires --team",
            err=True,
        )
        raise typer.Exit(code=1)

    try:
        report = compare_runs(
            bare_dir=bare,
            expert_dir=expert,
            team_dir=team,
            model=model,
            include_team_effect=include_team_effect,
        )
    except ValueError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(format_comparison_table(report))

    if output_json:
        output_json.parent.mkdir(parents=True, exist_ok=True)
        output_json.write_text(
            report.model_dump_json(indent=2) + "\n", encoding="utf-8"
        )
        typer.echo(f"\nJSON: {output_json}")


@app.command(name="context-diagnose")
def context_diagnose_cmd(
    team: Annotated[
        Path,
        typer.Option("--team", help="output_dir of the team's CLAUDE.md run"),
    ],
    expert: Annotated[
        Path,
        typer.Option(
            "--expert",
            help="output_dir of the run with --context-pack expert",
        ),
    ],
    model: Annotated[
        Optional[str],
        typer.Option(
            "--model",
            help="Model to diagnose. Required when trackers contain multiple models.",
        ),
    ] = None,
    gap_threshold: Annotated[
        float,
        typer.Option(
            "--gap-threshold",
            help=(
                "Percentage-point gap above which a category is flagged "
                "as needing CLAUDE.md coverage."
            ),
        ),
    ] = DEFAULT_GAP_THRESHOLD_PP,
    output_json: Annotated[
        Optional[Path],
        typer.Option(
            "--output-json",
            help="Write the full CoverageDiagnosis payload to JSON",
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose logging"),
    ] = False,
) -> None:
    """Diagnose which FAILURE-FACTORS categories the team's CLAUDE.md
    fails to cover, comparing against the expert pack's ceiling. Lists
    High-strength factor IDs per flagged category as action pointers.
    """
    if verbose:
        logging.basicConfig(level=logging.DEBUG, force=True)
    else:
        # Ensure `logger.warning` from context_diagnose surfaces on
        # stderr even without --verbose; otherwise the unmapped-check
        # warning is silently dropped in the default WARNING config.
        logging.basicConfig(level=logging.WARNING, force=True)

    from embedeval.context_diagnose import (
        diagnose_coverage,
        format_diagnosis,
    )

    try:
        diagnosis = diagnose_coverage(
            team_dir=team,
            expert_dir=expert,
            model=model,
            gap_threshold_pp=gap_threshold,
        )
    except ValueError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(format_diagnosis(diagnosis))

    if output_json:
        output_json.parent.mkdir(parents=True, exist_ok=True)
        output_json.write_text(
            diagnosis.model_dump_json(indent=2) + "\n", encoding="utf-8"
        )
        typer.echo(f"\nJSON: {output_json}")


@app.command(name="harmful-inspect")
def harmful_inspect_cmd(
    bare: Annotated[
        Path,
        typer.Option("--bare", help="output_dir of the no-pack baseline run"),
    ],
    expert: Annotated[
        Path,
        typer.Option(
            "--expert",
            help="output_dir of the run whose pack may have regressed cases",
        ),
    ],
    model: Annotated[
        Optional[str],
        typer.Option(
            "--model",
            help="Model to inspect. Required when trackers contain multiple models.",
        ),
    ] = None,
    output_json: Annotated[
        Optional[Path],
        typer.Option(
            "--output-json",
            help="Write per-case classifications to JSON",
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose logging"),
    ] = False,
) -> None:
    """Classify harmful cases (bare pass → expert fail) as likely
    brittleness or likely real regression, using L0-L4 failure layer
    heuristics. Answers "should I edit the pack or the checks?".
    """
    if verbose:
        logging.basicConfig(level=logging.DEBUG, force=True)

    from embedeval.harmful_inspect import (
        format_harmful_table,
        inspect_harmful,
    )

    try:
        cases = inspect_harmful(bare_dir=bare, expert_dir=expert, model=model)
    except ValueError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    typer.echo(format_harmful_table(cases))

    if output_json:
        import json as _json

        output_json.parent.mkdir(parents=True, exist_ok=True)
        output_json.write_text(
            _json.dumps([hc.model_dump(mode="json") for hc in cases], indent=2) + "\n",
            encoding="utf-8",
        )
        typer.echo(f"\nJSON: {output_json}")


