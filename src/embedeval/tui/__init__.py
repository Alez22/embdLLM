"""EmbedEval TUI dashboard package.

Textual-based terminal dashboard for browsing results and launching runs.
Start with::

    uv run embedeval tui

Public API: :class:`EmbedEvalTUI` and the :mod:`config` module holding the
runtime paths (``config.RESULTS_DIR`` / ``config.CASES_DIR``), which the CLI
overrides before constructing the app.
"""
from __future__ import annotations

from embedeval.tui import config
from embedeval.tui.app import EmbedEvalTUI

__all__ = ["EmbedEvalTUI", "config"]
