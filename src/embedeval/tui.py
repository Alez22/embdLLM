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


def _load_runs_summary() -> list[dict]:
    """Return one dict per run dir, built from summary.json + detail stats."""
    runs: list[dict] = []
    runs_root = RESULTS_DIR / "runs"
    if not runs_root.is_dir():
        return runs
    for run_dir in sorted(runs_root.iterdir(), reverse=True):
        summary_file = run_dir / "summary.json"
        if not summary_file.is_file():
            continue
        try:
            summary = json.loads(summary_file.read_text(encoding="utf-8"))
        except Exception:
            continue

        # Derive total, passed, score from detail files — the ground truth.
        # summary.json totals can be stale if the run was partially overwritten.
        details_dir = run_dir / "details"
        scores: list[float] = []
        passed = 0
        sdks: set[str] = set()
        if details_dir.is_dir():
            for f in details_dir.glob("*.json"):
                try:
                    d = json.loads(f.read_text(encoding="utf-8"))
                    s = d.get("total_score")
                    if s is not None:
                        scores.append(float(s))
                    if d.get("passed"):
                        passed += 1
                    sdk = d.get("sdk", "")
                    if sdk:
                        sdks.add(sdk)
                except Exception:
                    pass

        avg_score = sum(scores) / len(scores) if scores else 0.0
        total = len(scores)
        model = summary.get("model", "")
        if model == "mock":
            continue
        run_date = summary.get("run_timestamp", run_dir.name[:10])
        run_time = summary.get("run_time", "")
        timestamp = f"{run_date} {run_time}".strip() if run_time else run_date

        # Derive attempts and think from the run dir name or summary fields.
        gen_params = summary.get("generation_params", {})
        no_think = gen_params.get("no_think", False)
        temperature = summary.get("temperature", 0.0)
        max_attempt = max(
            (d.get("attempt", 1) for d in [summary]),
            default=summary.get("n_samples_per_case", 1),
        )
        # n_samples_per_case is the configured attempts count.
        attempts = summary.get("n_samples_per_case", 1)

        runs.append({
            "run_id": run_dir.name,
            "timestamp": timestamp,
            "model": model,
            "total": total,
            "passed": passed,
            "avg_score": avg_score,
            "attempts": attempts,
            "temperature": temperature,
            "no_think": no_think,
            "sdks": sorted(sdks),
        })
    return runs





def _score_bar(score: float, width: int = 8) -> str:
    """Return a simple ASCII progress bar for a [0,1] score."""
    filled = round(score * width)
    return "█" * filled + "░" * (width - filled)


# ---------------------------------------------------------------------------
# Run form modal
# ---------------------------------------------------------------------------

_CUSTOM_MODEL = "__custom__"


# Models available in the New Run form regardless of past results.
_PRESET_MODELS: list[str] = [
    "groq/llama-3.3-70b-versatile",
    "groq/meta-llama/llama-4-scout-17b-16e-instruct",
    "groq/qwen-qwen3-32b",
    "openrouter/deepseek/deepseek-v4-flash",
    "openrouter/google/gemini-2.5-flash",
    "anthropic/claude-haiku-4-5-20251001",
    "mock",
]


def _known_models() -> list[str]:
    """Return preset models merged with any model found in past results."""
    models: set[str] = set(_PRESET_MODELS)
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
    # Preserve preset order first, then any extra models from results.
    preset_set = set(_PRESET_MODELS)
    extras = sorted(m for m in models if m not in preset_set)
    return _PRESET_MODELS + extras


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
    #form-filter-row {
        height: auto;
        margin-top: 1;
    }
    #form-filter-row Select {
        width: 1fr;
    }
    #cases-list {
        height: 10;
        border: solid $primary-darken-2;
        overflow-y: auto;
        padding: 0 1;
    }
    #cases-header {
        height: auto;
        margin-top: 1;
        align: left middle;
    }
    #cases-header Label {
        margin-top: 0;
        width: 1fr;
    }
    #cases-header Button {
        margin-left: 1;
        min-width: 14;
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

    def _sdk_options(self) -> list[tuple[str, str]]:
        sdks = sorted({c.get("sdk", "") for c in self._cases if c.get("sdk")})
        return [("All SDKs", "all")] + [(s, s) for s in sdks]

    def _category_options(self) -> list[tuple[str, str]]:
        cats = sorted(
            {c.get("category", "") for c in self._cases if c.get("category")}
        )
        return [("All categories", "all")] + [(c, c) for c in cats]

    def _visible_cases(self) -> list[dict]:
        """Return cases matching the current SDK/category filter in the form."""
        sdk = str(self.query_one("#sel-form-sdk", Select).value)
        cat = str(self.query_one("#sel-form-category", Select).value)
        return [
            c for c in self._cases
            if (sdk == "all" or c.get("sdk") == sdk)
            and (cat == "all" or c.get("category") == cat)
        ]

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

            with Horizontal(id="form-filter-row"):
                yield Select(
                    self._sdk_options(),
                    value="all",
                    id="sel-form-sdk",
                    allow_blank=False,
                )
                yield Select(
                    self._category_options(),
                    value="all",
                    id="sel-form-category",
                    allow_blank=False,
                )

            with Horizontal(id="cases-header"):
                yield Label("Cases (leave empty = all matching filters)")
                yield Button("Select all", variant="default", id="btn-select-all")
                yield Button("Clear", variant="default", id="btn-clear-all")
            with ScrollableContainer(id="cases-list"):
                for case in self._cases:
                    yield Checkbox(
                        case.get("id", ""),
                        id=f"case-{case.get('id', '')}",
                    )

            yield Label("Attempts (1-5)")
            yield Input("1", id="input-attempts")

            yield Label("Temperature (0.0 = deterministic)")
            yield Input("0.0", id="input-temperature")

            yield Checkbox("--force (bypass cache)", id="check-force")
            yield Checkbox("--no-think", id="check-no-think")

            with Horizontal(id="form-buttons"):
                yield Button("Cancel", variant="default", id="btn-cancel")
                yield Button("Run", variant="primary", id="btn-run")

    def _update_case_visibility(self) -> None:
        """Show/hide case checkboxes based on SDK/category form filters."""
        visible_ids = {c.get("id") for c in self._visible_cases()}
        for case in self._cases:
            cid = case.get("id", "")
            cb = self.query_one(f"#case-{cid}", Checkbox)
            cb.display = cid in visible_ids

    @on(Select.Changed, "#sel-form-sdk")
    @on(Select.Changed, "#sel-form-category")
    def on_form_filter_changed(self, event: Select.Changed) -> None:
        self._update_case_visibility()

    @on(Button.Pressed, "#btn-select-all")
    def on_select_all(self) -> None:
        """Check all currently visible case checkboxes."""
        for case in self._visible_cases():
            cid = case.get("id", "")
            self.query_one(f"#case-{cid}", Checkbox).value = True

    @on(Button.Pressed, "#btn-clear-all")
    def on_clear_all(self) -> None:
        """Uncheck all case checkboxes."""
        for case in self._cases:
            cid = case.get("id", "")
            self.query_one(f"#case-{cid}", Checkbox).value = False

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
        temperature_raw = self.query_one("#input-temperature", Input).value.strip()
        try:
            temperature = max(0.0, min(2.0, float(temperature_raw)))
        except ValueError:
            temperature = 0.0
        force = self.query_one("#check-force", Checkbox).value
        no_think = self.query_one("#check-no-think", Checkbox).value
        sdk_filter = str(self.query_one("#sel-form-sdk", Select).value)
        cat_filter = str(self.query_one("#sel-form-category", Select).value)

        # Collect explicitly checked cases; fall back to all visible ones.
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
                "temperature": temperature,
                "force": force,
                "no_think": no_think,
                "selected_cases": selected_cases,
                "sdk_filter": sdk_filter,
                "cat_filter": cat_filter,
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

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal(id="filter-bar"):
            yield Button("New Run", variant="primary", id="btn-new-run")

        yield DataTable(id="results-table", cursor_type="row")
        yield Static("", id="summary-bar")

        with Container(id="log-panel"):
            yield Log(id="run-log", highlight=True, auto_scroll=True)

        yield Footer()

    def on_mount(self) -> None:
        self._cases: list[dict] = _discover_cases(CASES_DIR)
        self._runs: list[dict] = []
        self._proc: subprocess.Popen | None = None  # type: ignore[type-arg]
        self._log_queue: Queue[str] = Queue()
        self._log_file: Path = RESULTS_DIR / "tui-run.log"

        # Progress tracking during an active run.
        self._run_total: int = 0
        self._run_done: int = 0
        self._run_pass: int = 0
        self._run_fail: int = 0
        self._run_error: int = 0
        self._run_current: str = ""

        table = self.query_one("#results-table", DataTable)
        table.cursor_type = "row"
        table.add_column("Run", key="run_id")
        table.add_column("Model", key="model")
        table.add_column("Cases", key="cases")
        table.add_column("Att.", key="attempts")
        table.add_column("Temp", key="temperature")
        table.add_column("Think", key="think")
        table.add_column("SDKs", key="sdks")
        table.add_column("Score", key="score")
        table.add_column("Passed", key="passed")

        self._load_data()

    def _load_data(self) -> None:
        self._runs = _load_runs_summary()
        self._refresh_table()

    def _refresh_table(self) -> None:
        table = self.query_one("#results-table", DataTable)
        table.clear()

        for r in self._runs:
            score = r.get("avg_score", 0.0)
            score_str = f"{_score_bar(score)} {score:.2f}"
            total = r.get("total", 0)
            passed = r.get("passed", 0)
            no_think = r.get("no_think", False)
            think_str = "no" if no_think else "yes"
            temp = r.get("temperature", 0.0)
            sdks_str = ", ".join(r.get("sdks", [])) or "—"
            table.add_row(
                r.get("run_id", ""),
                r.get("model", "").split("/")[-1],
                str(total),
                str(r.get("attempts", 1)),
                f"{temp:.1f}",
                think_str,
                sdks_str,
                score_str,
                f"{passed}/{total}",
            )

        summary = self.query_one("#summary-bar", Static)
        summary.update(f"  {len(self._runs)} runs")

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
        else:
            # No explicit case selection: apply SDK/category filters if set.
            if config.get("sdk_filter", "all") != "all":
                cmd += ["--sdk", config["sdk_filter"]]
            if config.get("cat_filter", "all") != "all":
                cmd += ["--category", config["cat_filter"]]

        temperature = config.get("temperature", 0.0)
        if temperature != 0.0:
            cmd += ["--temperature", str(temperature)]
        if config["force"]:
            cmd.append("--force")
        if config["no_think"]:
            cmd.append("--no-think")
        # Verbose so runner emits INFO lines ("Case X attempt N: PASS/FAIL")
        # which the TUI parses to drive the progress bar.
        cmd.append("--verbose")

        # Mirror all run output to a plain-text file so it can be copied.
        self._log_file = RESULTS_DIR / "tui-run.log"

        # Compute expected total tasks for the progress bar.
        if selected:
            n_cases = len(selected)
        else:
            sdk_f = config.get("sdk_filter", "all")
            cat_f = config.get("cat_filter", "all")
            n_cases = sum(
                1 for c in self._cases
                if (sdk_f == "all" or c.get("sdk") == sdk_f)
                and (cat_f == "all" or c.get("category") == cat_f)
            )
        self._run_total = n_cases * config["attempts"]
        self._run_done = 0
        self._run_pass = 0
        self._run_fail = 0
        self._run_error = 0
        self._run_current = ""

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
        self.call_from_thread(self._finish_run)

    def _finish_run(self) -> None:
        """Called on the main thread when the subprocess exits."""
        self._load_data()
        # Summary bar will be repopulated by _refresh_table via _load_data.
        # Reset run state so stale progress isn't shown on next run.
        self._run_total = 0
        self._run_done = 0

    def _append_log(self, line: str) -> None:
        log = self.query_one("#run-log", Log)
        log.write_line(line)
        if hasattr(self, "_log_file"):
            with self._log_file.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
        self._parse_progress(line)

    def _parse_progress(self, line: str) -> None:
        """Extract case completion events from verbose runner output.

        The runner emits: "Case <id> attempt <n>: PASS" or "FAIL@L<n>"
        via logger.info (visible only with --verbose).
        """
        # e.g. "INFO:embedeval.runner:Case nxp-mcxc-i2c-001 attempt 1: PASS"
        import re
        m = re.search(r"Case (\S+) attempt \d+: (PASS|FAIL@L\S+)", line)
        if not m:
            return
        case_id, status = m.group(1), m.group(2)
        self._run_done += 1
        self._run_current = case_id
        if status == "PASS":
            self._run_pass += 1
        elif "FAIL" in status:
            # Distinguish infra errors (output_tokens unknown here — use layer 0)
            if status == "FAIL@LNone" or status == "FAIL@L0":
                self._run_error += 1
            else:
                self._run_fail += 1
        self._update_progress_bar()

    def _update_progress_bar(self) -> None:
        """Render progress into #summary-bar while a run is active."""
        total = self._run_total
        done = self._run_done
        if total == 0:
            return
        bar_width = 20
        filled = round(done / total * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)
        pct = int(done / total * 100)
        summary = self.query_one("#summary-bar", Static)
        summary.update(
            f"  Running  [{bar}]  {done}/{total} ({pct}%)"
            f"  {self._run_current}"
            f"  ·  {self._run_pass} pass  {self._run_fail} fail  {self._run_error} error"
        )
