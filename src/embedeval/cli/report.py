"""Reporting commands: report, refresh-tracker, dashboard, report-html."""

import json
import logging
from pathlib import Path
from typing import Annotated, Optional

import typer

from embedeval.cli.app import app


@app.command()
def report(
    results_dir: Annotated[
        Path,
        typer.Option("--results", help="Directory containing result JSON files"),
    ] = Path("results"),
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Output leaderboard path"),
    ] = Path("LEADERBOARD.md"),
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose logging"),
    ] = False,
) -> None:
    """Generate leaderboard from existing results."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG, force=True)

    from embedeval.models import BenchmarkReport
    from embedeval.reporter import generate_leaderboard

    json_files = sorted(results_dir.glob("*.json"))
    if not json_files:
        typer.echo(f"No JSON results found in {results_dir}")
        raise typer.Exit(code=1)

    reports: list[BenchmarkReport] = []
    for jf in json_files:
        data = json.loads(jf.read_text(encoding="utf-8"))
        reports.append(BenchmarkReport(**data))

    generate_leaderboard(reports, output)
    typer.echo(f"Leaderboard written to {output}")




@app.command(name="agent-report")
def agent_report(
    results_dir: Annotated[
        Path,
        typer.Option("--results", help="Directory containing runs/ with agent_run.json"),
    ] = Path("results"),
    output: Annotated[
        Path,
        typer.Option("--output", "-o", help="Output Markdown path"),
    ] = Path("results/reports/AGENT_LEADERBOARD.md"),
) -> None:
    """Generate the agent-mode leaderboard (Markdown + PNG) from agent runs."""
    from embedeval.agent_leaderboard import generate_agent_report

    figure_path = output.with_name("agent_pass_matrix.png")
    figure_written, n = generate_agent_report(results_dir, output, figure_path)
    if n == 0:
        typer.echo("No container agent runs found under results/runs/.")
        raise typer.Exit(code=1)
    typer.echo(f"Agent leaderboard written to {output} ({n} models).")
    if figure_written:
        typer.echo(f"Figure written to {figure_path}.")
    else:
        typer.echo("Figure skipped (matplotlib not installed).")


@app.command(name="perf-report")
def perf_report(
    results_dir: Annotated[
        Path,
        typer.Option("--results", help="Results root containing runs/"),
    ] = Path("results"),
) -> None:
    """Generate the non-agentic performance figures (NXP vs Zephyr)."""
    from embedeval.perf_report import generate_performance_report

    out = generate_performance_report(results_dir)
    typer.echo(f"Performance report figures written to {out}/")


@app.command(name="refresh-tracker")
def refresh_tracker(
    cases_dir: Annotated[
        Path,
        typer.Option("--cases", help="Path to cases directory"),
    ] = Path("cases"),
    results_dir: Annotated[
        Path,
        typer.Option("--results", help="Results directory with tracker"),
    ] = Path("results"),
) -> None:
    """Refresh test tracker after TC changes (used by /wrapup)."""
    from embedeval.result_tracker import (
        detect_changed_cases_from_git,
        generate_results_doc,
        load_tracker,
        mark_cases_changed,
        save_tracker,
    )

    tracker = load_tracker(results_dir)
    if not tracker.results:
        typer.echo("No test results tracked yet.")
        raise typer.Exit(code=0)

    changed = detect_changed_cases_from_git(cases_dir)
    if not changed:
        typer.echo("No cases changed in last commit.")
    else:
        n = mark_cases_changed(tracker, changed, cases_dir)
        save_tracker(tracker, results_dir)
        typer.echo(f"Marked {n} case/model pairs for retest: {', '.join(changed)}")

    reports_dir = results_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    generate_results_doc(tracker, reports_dir / "TEST_RESULTS.md", cases_dir)
    typer.echo("TEST_RESULTS.md refreshed.")




@app.command()
def dashboard(
    results_dir: Annotated[
        Path,
        typer.Option("--results", help="Directory containing run results"),
    ] = Path("results"),
    cases_dir: Annotated[
        Path,
        typer.Option("--cases", help="Path to cases directory"),
    ] = Path("cases"),
    port: Annotated[
        int,
        typer.Option("--port", "-p", help="Port to listen on"),
    ] = 7860,
    no_browser: Annotated[
        bool,
        typer.Option("--no-browser", help="Do not open browser automatically"),
    ] = False,
) -> None:
    """Start the results dashboard web app."""
    import uvicorn

    import embedeval.dashboard as _dash

    _dash.RESULTS_DIR = results_dir.resolve()
    _dash.CASES_DIR = cases_dir.resolve()

    url = f"http://localhost:{port}"
    typer.echo(f"Dashboard: {url}  (Ctrl+C to stop)")

    if not no_browser:
        from threading import Timer

        Timer(1.0, lambda: __import__("webbrowser").open(url)).start()

    uvicorn.run(_dash.app, host="0.0.0.0", port=port, log_level="warning")




@app.command(name="report-html")
def report_html(
    results_dir: Annotated[
        Path,
        typer.Option("--results", help="Directory containing runs/ result files"),
    ] = Path("results"),
    output: Annotated[
        Optional[Path],
        typer.Option(
            "--output", "-o",
            help="Output HTML path (default: <results>/reports/report.html)",
        ),
    ] = None,
    cases_dir: Annotated[
        Path,
        typer.Option("--cases", help="Case root used to count cases for coverage"),
    ] = Path("cases"),
    total_cases: Annotated[
        Optional[int],
        typer.Option(
            "--total-cases",
            help="Override coverage denominator (default: all implemented cases)",
        ),
    ] = None,
) -> None:
    """Generate a standalone visual benchmark report (interactive HTML)."""
    from embedeval.report import write_standalone_report

    out = output or (results_dir / "reports" / "report.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    path = write_standalone_report(results_dir, out, total_cases, cases_dir)
    typer.echo(f"Report written to {path}")
