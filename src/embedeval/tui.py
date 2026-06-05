"""EmbedEval TUI dashboard.

Textual-based terminal dashboard for browsing results and launching runs.
Start with:
    uv run embedeval tui
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from queue import Queue
from typing import ClassVar

import yaml
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    Checkbox,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    Log,
    Select,
    Static,
)

# Resolved at startup by the CLI command.
RESULTS_DIR: Path = Path("results")
CASES_DIR: Path = Path("cases")


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _discover_cases(cases_dir: Path) -> list[dict]:
    """Return minimal case metadata dicts from all metadata.yaml files."""
    cases: list[dict] = []
    for meta_file in sorted(cases_dir.rglob("metadata.yaml")):
        try:
            data = yaml.safe_load(meta_file.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "id" in data:
                cases.append(data)
        except Exception:
            pass
    return cases


def _load_results() -> list[dict]:
    """Load all EvalResult detail JSONs from results/runs/*/details/*.json."""
    results: list[dict] = []
    runs_root = RESULTS_DIR / "runs"
    if not runs_root.is_dir():
        return results
    for run_dir in sorted(runs_root.iterdir(), reverse=True):
        details_dir = run_dir / "details"
        if not details_dir.is_dir():
            continue
        for detail_file in sorted(details_dir.glob("*.json")):
            try:
                data = json.loads(detail_file.read_text(encoding="utf-8"))
                # Keep only the most recent attempt per (case_id, model).
                results.append(data)
            except Exception:
                pass
    return results


def _best_results(raw: list[dict]) -> list[dict]:
    """Keep the best attempt per (case_id, model) — highest total_score."""
    best: dict[tuple[str, str], dict] = {}
    for r in raw:
        key = (r.get("case_id", ""), r.get("model", ""))
        prev = best.get(key)
        if prev is None or r.get("total_score", 0) > prev.get("total_score", 0):
            best[key] = r
    return list(best.values())


def _layer_label(r: dict) -> str:
    """Return a short string like 'L0 FAIL' or 'PASS'."""
    if r.get("passed"):
        return "PASS"
    layer = r.get("failed_at_layer")
    if layer is None:
        return "FAIL"
    names = {0: "L0", 1: "L1", 2: "L2", 3: "L3", 4: "L4"}
    return f"{names.get(layer, f'L{layer}')} FAIL"


def _score_bar(score: float, width: int = 8) -> str:
    """Return a simple ASCII progress bar for a [0,1] score."""
    filled = round(score * width)
    return "█" * filled + "░" * (width - filled)


# ---------------------------------------------------------------------------
# Run form modal
# ---------------------------------------------------------------------------

_CUSTOM_MODEL = "__custom__"


def _known_models() -> list[str]:
    """Return model names found in past result JSONs, sorted."""
    models: set[str] = set()
    runs_root = RESULTS_DIR / "runs"
    if runs_root.is_dir():
        for detail_file in runs_root.rglob("details/*.json"):
            try:
                data = json.loads(detail_file.read_text(encoding="utf-8"))
                m = data.get("model", "")
                if m and m != "mock":
                    models.add(m)
            except Exception:
                pass
    return sorted(models)


class RunFormScreen(ModalScreen[dict | None]):
    """Modal dialog to configure and launch a benchmark run."""

    CSS = """
    RunFormScreen {
        align: center middle;
    }
    #run-form {
        background: $surface;
        border: thick $primary;
        padding: 1 2;
        width: 70;
        height: auto;
    }
    #run-form Label {
        margin-top: 1;
    }
    #custom-model-row {
        height: auto;
        display: none;
    }
    #custom-model-row.visible {
        display: block;
    }
    #cases-list {
        height: 10;
        border: solid $primary-darken-2;
        overflow-y: auto;
        padding: 0 1;
    }
    #form-buttons {
        margin-top: 1;
        align: right middle;
        height: 3;
    }
    """

    def __init__(self, cases: list[dict]) -> None:
        super().__init__()
        self._cases = cases

    def compose(self) -> ComposeResult:
        known = _known_models()
        model_options: list[tuple[str, str]] = [(m, m) for m in known]
        model_options.append(("Other (type below)...", _CUSTOM_MODEL))

        # Pre-select first known model, or custom if none known.
        default_model = known[0] if known else _CUSTOM_MODEL

        with Container(id="run-form"):
            yield Label("New Run", id="form-title")

            yield Label("Model")
            yield Select(
                model_options,
                value=default_model,
                id="sel-run-model",
                allow_blank=False,
            )
            with Container(id="custom-model-row"):
                yield Input(
                    placeholder="e.g. groq/llama-3.3-70b-versatile",
                    id="input-custom-model",
                )

            yield Label("Cases dir")
            yield Input(str(CASES_DIR), id="input-cases-dir")

            yield Label("Cases (leave empty = all in dir)")
            with ScrollableContainer(id="cases-list"):
                for case in self._cases:
                    yield Checkbox(
                        case.get("id", ""),
                        id=f"case-{case.get('id', '')}",
                    )

            yield Label("Attempts (1-5)")
            yield Input("1", id="input-attempts")

            yield Checkbox("--force (bypass cache)", id="check-force")
            yield Checkbox("--no-think", id="check-no-think")

            with Horizontal(id="form-buttons"):
                yield Button("Cancel", variant="default", id="btn-cancel")
                yield Button("Run", variant="primary", id="btn-run")

    @on(Select.Changed, "#sel-run-model")
    def on_model_select_changed(self, event: Select.Changed) -> None:
        """Show/hide the custom model input depending on selection."""
        custom_row = self.query_one("#custom-model-row")
        if event.value == _CUSTOM_MODEL:
            custom_row.add_class("visible")
            self.query_one("#input-custom-model", Input).focus()
        else:
            custom_row.remove_class("visible")

    @on(Button.Pressed, "#btn-cancel")
    def cancel(self) -> None:
        self.dismiss(None)

    @on(Button.Pressed, "#btn-run")
    def confirm(self) -> None:
        sel = self.query_one("#sel-run-model", Select)
        if sel.value == _CUSTOM_MODEL:
            model = self.query_one("#input-custom-model", Input).value.strip()
            if not model:
                self.query_one("#input-custom-model", Input).focus()
                return
        else:
            model = str(sel.value)
        if not model:
            return

        cases_dir = self.query_one("#input-cases-dir", Input).value.strip()
        attempts_raw = self.query_one("#input-attempts", Input).value.strip()
        try:
            attempts = max(1, min(5, int(attempts_raw)))
        except ValueError:
            attempts = 1
        force = self.query_one("#check-force", Checkbox).value
        no_think = self.query_one("#check-no-think", Checkbox).value

        # Collect selected cases.
        selected_cases: list[str] = []
        for case in self._cases:
            cid = case.get("id", "")
            cb = self.query_one(f"#case-{cid}", Checkbox)
            if cb.value:
                selected_cases.append(cid)

        self.dismiss(
            {
                "model": model,
                "cases_dir": cases_dir,
                "attempts": attempts,
                "force": force,
                "no_think": no_think,
                "selected_cases": selected_cases,
            }
        )


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------

class EmbedEvalTUI(App):
    """Textual TUI for the EmbedEval benchmark dashboard."""

    TITLE = "EmbedEval TUI"
    CSS = """
    #top-bar {
        height: 3;
        background: $primary-darken-2;
        padding: 0 1;
        align: left middle;
    }
    #top-bar Label {
        margin-right: 2;
    }
    #filter-bar {
        height: 3;
        padding: 0 1;
        background: $surface-darken-1;
    }
    #filter-bar Label {
        margin-right: 1;
        width: auto;
    }
    #filter-bar Select {
        width: 22;
        margin-right: 2;
    }
    #results-table {
        height: 1fr;
    }
    #log-panel {
        height: 12;
        border-top: solid $primary;
    }
    #log-panel Log {
        height: 1fr;
    }
    #summary-bar {
        height: 1;
        background: $surface-darken-2;
        padding: 0 1;
    }
    """

    BINDINGS: ClassVar[list[Binding]] = [
        Binding("r", "refresh", "Refresh"),
        Binding("n", "new_run", "New Run"),
        Binding("q", "quit", "Quit"),
    ]

    # Reactive filter state — changes trigger a table refresh.
    _filter_model: reactive[str] = reactive("all")
    _filter_category: reactive[str] = reactive("all")

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal(id="filter-bar"):
            yield Label("Model:")
            yield Select(
                [("All", "all")],
                value="all",
                id="sel-model",
                allow_blank=False,
            )
            yield Label("Category:")
            yield Select(
                [("All", "all")],
                value="all",
                id="sel-category",
                allow_blank=False,
            )
            yield Button("New Run", variant="primary", id="btn-new-run")

        yield DataTable(id="results-table", cursor_type="row")
        yield Static("", id="summary-bar")

        with Container(id="log-panel"):
            yield Log(id="run-log", highlight=True, auto_scroll=True)

        yield Footer()

    def on_mount(self) -> None:
        self._cases: list[dict] = []
        self._results: list[dict] = []
        self._proc: subprocess.Popen | None = None  # type: ignore[type-arg]
        self._log_queue: Queue[str] = Queue()
        self._log_file: Path = RESULTS_DIR / "tui-run.log"

        table = self.query_one("#results-table", DataTable)
        table.add_columns(
            "Case", "Model", "Score", "Layer", "Category", "SDK", "Attempts"
        )

        self._load_data()

    def _load_data(self) -> None:
        self._cases = _discover_cases(CASES_DIR)
        self._results = _best_results(_load_results())
        self._rebuild_filters()
        self._refresh_table()

    def _rebuild_filters(self) -> None:
        """Repopulate Select widgets with values found in loaded results."""
        models = sorted(
            {r.get("model", "") for r in self._results if r.get("model")}
        )
        cats = sorted(
            {r.get("category", "") for r in self._results if r.get("category")}
        )

        model_sel = self.query_one("#sel-model", Select)
        cat_sel = self.query_one("#sel-category", Select)

        model_sel.set_options([("All", "all")] + [(m, m) for m in models])
        cat_sel.set_options([("All", "all")] + [(c, c) for c in cats])

    def _refresh_table(self) -> None:
        table = self.query_one("#results-table", DataTable)
        table.clear()

        filtered = [
            r for r in self._results
            if (self._filter_model == "all" or r.get("model") == self._filter_model)
            and (
                self._filter_category == "all"
                or r.get("category") == self._filter_category
            )
        ]

        def _sort_key(x: dict) -> tuple[str, str]:
            return (x.get("case_id", ""), x.get("model", ""))

        for r in sorted(filtered, key=_sort_key):
            score = r.get("total_score", 0.0)
            score_str = f"{_score_bar(score)} {score:.2f}"
            layer_str = _layer_label(r)

            # Count how many attempts exist for this (case_id, model).
            attempts = sum(
                1 for x in self._results
                if x.get("case_id") == r.get("case_id")
                and x.get("model") == r.get("model")
            )

            table.add_row(
                r.get("case_id", ""),
                r.get("model", "").split("/")[-1],
                score_str,
                layer_str,
                r.get("category", ""),
                r.get("sdk", ""),
                str(attempts),
            )

        passed = sum(1 for r in filtered if r.get("passed"))
        summary = self.query_one("#summary-bar", Static)
        summary.update(
            f"  {len(filtered)} results | {passed} passed | "
            f"{len(filtered) - passed} failed"
        )

    # -----------------------------------------------------------------------
    # Filter changes
    # -----------------------------------------------------------------------

    @on(Select.Changed, "#sel-model")
    def on_model_changed(self, event: Select.Changed) -> None:
        self._filter_model = str(event.value)
        self._refresh_table()

    @on(Select.Changed, "#sel-category")
    def on_category_changed(self, event: Select.Changed) -> None:
        self._filter_category = str(event.value)
        self._refresh_table()

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    def action_refresh(self) -> None:
        self._load_data()
        log = self.query_one("#run-log", Log)
        log.write_line("[refresh] Results reloaded from disk.")

    def action_new_run(self) -> None:
        self.push_screen(RunFormScreen(self._cases), self._on_run_config)

    @on(Button.Pressed, "#btn-new-run")
    def on_new_run_button(self) -> None:
        self.action_new_run()

    def _on_run_config(self, config: dict | None) -> None:
        if config is None:
            return
        self._launch_run(config)

    # -----------------------------------------------------------------------
    # Subprocess run (background thread + worker)
    # -----------------------------------------------------------------------

    def _launch_run(self, config: dict) -> None:
        if self._proc is not None and self._proc.poll() is None:
            log = self.query_one("#run-log", Log)
            log.write_line("[error] A run is already in progress.")
            return

        cases_path = config["cases_dir"]
        selected = config["selected_cases"]

        cmd = [
            "uv", "run", "embedeval", "run",
            "--model", config["model"],
            "--cases", cases_path,
            "--output-dir", str(RESULTS_DIR),
            "--attempts", str(config["attempts"]),
        ]

        if selected:
            cmd += ["--case-ids", ",".join(selected)]

        if config["force"]:
            cmd.append("--force")
        if config["no_think"]:
            cmd.append("--no-think")

        # Mirror all run output to a plain-text file so it can be copied.
        self._log_file = RESULTS_DIR / "tui-run.log"

        log = self.query_one("#run-log", Log)
        log.write_line(f"[log] {self._log_file}")
        log.write_line(f"[launch] {' '.join(cmd)}")
        self._log_file.write_text(
            f"[launch] {' '.join(cmd)}\n", encoding="utf-8"
        )

        # Load API keys from .env if present.
        env = os.environ.copy()
        dot_env = Path(".env")
        if dot_env.is_file():
            for line in dot_env.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    env[k.strip()] = v.strip()

        # Run from the project root so relative paths (results/, corpus/) resolve.
        project_root = RESULTS_DIR.parent

        self._proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            cwd=project_root,
        )
        self._stream_output()

    @work(thread=True)
    def _stream_output(self) -> None:
        """Read subprocess stdout line-by-line and forward to log widget."""
        if self._proc is None:
            return
        assert self._proc.stdout is not None
        for line in self._proc.stdout:
            self.call_from_thread(self._append_log, line.rstrip())
        self._proc.wait()
        rc = self._proc.returncode
        self.call_from_thread(self._append_log, f"[done] exit code {rc}")
        # Auto-refresh results after a run completes.
        self.call_from_thread(self._load_data)

    def _append_log(self, line: str) -> None:
        log = self.query_one("#run-log", Log)
        log.write_line(line)
        if hasattr(self, "_log_file"):
            with self._log_file.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
