"""EmbedEval CLI package.

Importing this package builds the Typer ``app`` and registers every command
by importing the command modules (whose ``@app.command()`` decorators run on
import). The console entrypoint ``embedeval.cli:app`` resolves here.
"""

# Import for side effect: each module registers its commands on ``app``.
from embedeval.cli import (  # noqa: E402,F401
    cases,
    context,
    misc,
    report,
    run,
    validate,
)
from embedeval.cli.app import _parse_sdk_filter, app

# Re-exported for backward compatibility with code/tests that imported
# these from the old flat ``embedeval.cli`` module.
from embedeval.cli.run import _build_comprehensive_results  # noqa: E402

__all__ = ["app", "_parse_sdk_filter", "_build_comprehensive_results"]
