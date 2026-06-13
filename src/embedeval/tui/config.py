"""Runtime paths for the TUI, resolved by the CLI at startup.

These are module-level so the CLI can override them before the app is
constructed (``embedeval.tui.RESULTS_DIR = ...``). Every reader must access
them as ``config.RESULTS_DIR`` (not ``from config import RESULTS_DIR``) so
the override is seen at call time.
"""
from __future__ import annotations

from pathlib import Path

RESULTS_DIR: Path = Path("results")
CASES_DIR: Path = Path("cases")
