"""Headless smoke tests for the New Run form (RunFormScreen).

Uses Textual's run_test pilot: no terminal, no network assertions (the
model catalog loads in a worker and may fall back to the preset list).
"""

from __future__ import annotations

import pytest
from textual.widgets import Checkbox, Label, Select

from embedeval.tui.app import EmbedEvalTUI
from embedeval.tui.run_form import RunFormScreen


def _case_checkboxes(screen: RunFormScreen) -> list[Checkbox]:
    return [cb for cb in screen.query(Checkbox) if (cb.id or "").startswith("case-")]


def _cases_header_text(screen: RunFormScreen) -> str:
    return str(screen.query_one("#lbl-cases-header", Label).render())


@pytest.mark.asyncio
async def test_run_form_layout_counter_and_mode_visibility() -> None:
    app = EmbedEvalTUI()
    async with app.run_test(size=(160, 50)) as pilot:
        await pilot.press("n")
        await pilot.pause()
        screen = app.screen
        assert isinstance(screen, RunFormScreen)

        # Cancel/Run must not scroll away with the form body.
        body = screen.query_one("#form-body")
        assert body not in screen.query_one("#form-buttons").ancestors
        assert body in screen.query_one("#form-columns").ancestors

        # Ticked-cases counter follows checkbox changes.
        cbs = _case_checkboxes(screen)
        cbs[0].value = True
        cbs[1].value = True
        await pilot.pause()
        assert "2 ticked" in _cases_header_text(screen)
        cbs[0].value = False
        await pilot.pause()
        assert "1 ticked" in _cases_header_text(screen)

        # Agent mode hides run-only fields, shows agent-only ones.
        screen.query_one("#sel-mode", Select).value = "agent"
        await pilot.pause()
        assert not screen.query_one("#check-force").display
        assert not screen.query_one("#check-no-think").display
        assert not screen.query_one("#lbl-attempts").display
        assert screen.query_one("#sel-context-pack").display

        # Escape closes the form without a result.
        await pilot.press("escape")
        await pilot.pause()
        assert not isinstance(app.screen, RunFormScreen)
