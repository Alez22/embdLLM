"""Headless smoke tests for the TUI: run-history table and New Run form.

Uses Textual's run_test pilot: no terminal, no network assertions (the
model catalog loads in a worker and may fall back to the preset list).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from textual.widgets import Checkbox, DataTable, Label, Select

from embedeval.tui import config as tui_config
from embedeval.tui.app import EmbedEvalTUI
from embedeval.tui.data import _load_runs_summary
from embedeval.tui.run_form import RunFormScreen


def _write_generation_run(runs_root: Path, run_id: str, model: str) -> None:
    run_dir = runs_root / run_id
    (run_dir / "details").mkdir(parents=True)
    (run_dir / "summary.json").write_text(json.dumps({
        "model": model,
        "temperature": 0.5,
        "n_samples_per_case": 5,
        "scenario": "generation",
        "generation_params": {"no_think": False},
    }))
    # One detail file per (case, attempt): case-0 passes on the 2nd attempt,
    # case-1 never passes — the row must show 1/2, not 1/4.
    attempts = [("case-0", 1, False), ("case-0", 2, True),
                ("case-1", 1, False), ("case-1", 2, False)]
    for case_id, attempt, passed in attempts:
        (run_dir / "details" / f"{case_id}_attempt{attempt}.json").write_text(
            json.dumps({
                "case_id": case_id, "attempt": attempt,
                "passed": passed, "sdk": "mcuxpresso-sdk",
            })
        )


def _write_agent_run(runs_root: Path, run_id: str, model: str) -> None:
    run_dir = runs_root / run_id
    run_dir.mkdir(parents=True)
    (run_dir / "agent_run.json").write_text(json.dumps({
        "model": model,
        "max_turns": 5,
        "temperature": 0.0,
        "context_pack": "nxp.md",
        "cases": [
            {"case_id": "a", "passed": True},
            {"case_id": "b", "passed": False},
        ],
        "summary": {"total_tokens": 12345},
    }))


@pytest.fixture
def history_results_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the TUI at a temp results dir with one gen + one agent run."""
    runs_root = tmp_path / "runs"
    _write_generation_run(
        runs_root, "2026-07-01_1000_openrouter_deepseek_deepseek-v4-flash",
        "openrouter/deepseek/deepseek-v4-flash",
    )
    _write_agent_run(
        runs_root, "2026-07-02_2200_openrouter_z-ai_glm-5.2_t5",
        "openrouter/z-ai/glm-5.2",
    )
    _write_agent_run(runs_root, "2026-07-03_0900_mock_t1", "mock")
    monkeypatch.setattr(tui_config, "RESULTS_DIR", tmp_path)
    return tmp_path


def test_load_runs_summary_covers_gen_and_agent(history_results_dir: Path) -> None:
    rows = _load_runs_summary()
    # Mock run skipped; newest (agent) first.
    assert [r["mode"] for r in rows] == ["agent", "gen"]

    agent, gen = rows
    assert agent["timestamp"] == "2026-07-02 22:00"
    assert agent["max_turns"] == 5
    assert agent["context_pack"] == "nxp.md"
    assert (agent["passed"], agent["total"]) == (1, 2)
    assert agent["tokens"] == 12345

    assert gen["attempts"] == 5
    assert (gen["passed"], gen["total"]) == (1, 2)
    assert gen["sdks"] == ["mcuxpresso-sdk"]


@pytest.mark.asyncio
async def test_history_table_shows_runs(history_results_dir: Path) -> None:
    app = EmbedEvalTUI()
    async with app.run_test(size=(160, 50)) as pilot:
        await pilot.pause()
        table = app.query_one("#results-table", DataTable)
        assert table.row_count == 2
        first = [str(c) for c in table.get_row_at(0)]
        assert first[0] == "2026-07-02 22:00"
        assert first[1] == "agent (nxp.md)"
        assert first[2] == "glm-5.2"
        assert "1/2" in first[7]
        assert first[8] == "12,345"


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
