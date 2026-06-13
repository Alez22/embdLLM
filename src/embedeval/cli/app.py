"""Typer application object and shared CLI helpers.

The single ``app`` instance lives here so every command module can register
on it with ``@app.command()``. ``embedeval.cli`` imports those modules to
trigger registration, then re-exports ``app`` as the console entrypoint.
"""

import logging
from typing import TYPE_CHECKING, Annotated

import typer

from embedeval.models import Sdk

if TYPE_CHECKING:
    from embedeval.models import CaseMetadata, EvalResult  # noqa: F401
    from embedeval.result_tracker import TrackerData  # noqa: F401

app = typer.Typer(help="EmbedEval: Embedded firmware LLM benchmark")

logger = logging.getLogger(__name__)


def _parse_sdk_filter(raw: str | None) -> list[Sdk]:
    """Parse a comma-separated --sdk string into a list of Sdk enum values.

    Empty/None returns an empty list (no filter). Unknown values raise a
    typer.Exit with a readable error listing the valid buckets.
    """
    if not raw:
        return []
    result: list[Sdk] = []
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        try:
            result.append(Sdk(token))
        except ValueError as exc:
            valid = ", ".join(s.value for s in Sdk)
            typer.echo(
                f"Error: unknown --sdk value '{token}'. Valid: {valid}", err=True
            )
            raise typer.Exit(code=1) from exc
    return result


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose logging"),
    ] = False,
) -> None:
    """EmbedEval benchmark tool."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    if ctx.invoked_subcommand is None:
        typer.echo("EmbedEval v0.1.0 — use --help for commands")

