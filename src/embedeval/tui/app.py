"""Main TUI application: leaderboard table, run launching, log streaming."""
from __future__ import annotations

import os
import re
import subprocess
import time
from pathlib import Path
from queue import Queue
from typing import ClassVar

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Log,
    Static,
)

# Aliased to avoid shadowing by local `config` dicts (run configs) in
# methods like _launch_run / _on_run_config.
from embedeval.tui import config as tui_config
from embedeval.tui.data import _discover_cases, _load_runs_summary, _score_bar
from embedeval.tui.log_format import (
    _AGENT_RESULT_RE,
    _CASE_UNHANDLED_RE,
    _format_log_line,
)
from embedeval.tui.run_form import RunFormScreen


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
        Binding("s", "stop_run", "Stop Run"),
        Binding("d", "open_dashboard", "Dashboard"),
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal(id="filter-bar"):
            yield Button("New Run", variant="primary", id="btn-new-run")
            yield Button("Stop", variant="error", id="btn-stop-run")

        yield DataTable(id="results-table", cursor_type="row")
        yield Static("", id="summary-bar")

        with Container(id="log-panel"):
            yield Log(id="run-log", highlight=True, auto_scroll=True)

        yield Footer()

    def on_mount(self) -> None:
        self._cases: list[dict] = _discover_cases(tui_config.CASES_DIR)
        self._proc: subprocess.Popen | None = None  # type: ignore[type-arg]
        self._dash_proc: subprocess.Popen | None = None  # type: ignore[type-arg]
        self._pending_runs: list[dict] = []  # queued configs waiting for current run to finish
        self._log_queue: Queue[str] = Queue()
        self._log_file: Path = tui_config.RESULTS_DIR / "tui-run.log"

        # Progress tracking during an active run.
        self._run_total: int = 0
        self._run_done: int = 0
        self._run_pass: int = 0
        self._run_fail: int = 0
        self._run_error: int = 0
        self._run_current: str = ""
        self._run_model: str = ""
        # Wall-clock start of the active run, and the 1s ticker that keeps
        # the elapsed time in the progress bar moving between case events.
        self._run_started_at: float = 0.0
        self._run_timer = None
        # Track (case_id, attempt) already counted: the runner can emit both an
        # "unhandled" retry line and a final PASS/FAIL for the same attempt, so
        # counting every matching line double-counts and the bar overshoots 100%.
        self._run_seen: set[tuple[str, str]] = set()

        self._rows: list[dict] = []
        self._load_data()

    def _build_columns(self) -> None:
        """Build the run-history columns (fixed set)."""
        table = self.query_one("#results-table", DataTable)
        table.clear(columns=True)
        table.cursor_type = "row"
        table.add_column("When", key="when")
        table.add_column("Mode", key="mode")
        table.add_column("Model", key="model")
        table.add_column("Temp", key="temperature")
        table.add_column("Think", key="think")
        table.add_column("Att/Turns", key="budget")
        table.add_column("Cases", key="cases")
        table.add_column("Result", key="result")
        table.add_column("Tokens", key="tokens")

    def _load_data(self) -> None:
        self._rows = _load_runs_summary()
        self._build_columns()
        self._refresh_table()

    def _refresh_table(self) -> None:
        """One row per launched run, newest first."""
        table = self.query_one("#results-table", DataTable)
        table.clear()

        for r in self._rows:
            is_agent = r.get("mode") == "agent"
            mode = "agent"
            if is_agent and r.get("context_pack"):
                mode = f"agent ({r['context_pack']})"
            elif not is_agent:
                mode = "gen"
            if is_agent:
                think_str = "—"
                budget = f"t{r.get('max_turns', 0)}"
            else:
                think_str = "no" if r.get("no_think", False) else "yes"
                budget = f"a{r.get('attempts', 1)}"
            total = r.get("total", 0)
            passed = r.get("passed", 0)
            pass_rate = passed / total if total else 0.0
            sdks = ",".join(s.replace("-sdk", "") for s in r.get("sdks", []))
            tokens = r.get("tokens")
            cells = [
                r.get("timestamp", ""),
                mode,
                r.get("model", "").split("/")[-1],
                f"{r.get('temperature', 0.0):.1f}",
                think_str,
                budget,
                f"{total}" + (f" · {sdks}" if sdks else ""),
                f"{_score_bar(pass_rate)} {passed}/{total}",
                f"{tokens:,}" if tokens else "—",
            ]
            table.add_row(*cells, key=r.get("run_id", ""))

        summary = self.query_one("#summary-bar", Static)
        summary.update(
            f"  {len(self._rows)} runs  ·  newest first  ·  "
            f"Enter on a row prints its path (for --resume)"
        )

    @on(DataTable.RowSelected, "#results-table")
    def on_run_row_selected(self, event: DataTable.RowSelected) -> None:
        """Print the selected run's directory — handy for agent --resume."""
        run_id = event.row_key.value
        if run_id:
            log = self.query_one("#run-log", Log)
            log.write_line(f"[run] {tui_config.RESULTS_DIR / 'runs' / run_id}")

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    def action_refresh(self) -> None:
        self._load_data()
        log = self.query_one("#run-log", Log)
        log.write_line("[refresh] Results reloaded from disk.")

    def action_open_dashboard(self) -> None:
        """Launch the results dashboard web app (detached) and open the browser.

        The dashboard is a uvicorn server, so it must not run in the
        foreground or it would block the TUI. We spawn it detached and let it
        open the browser itself. A second press reuses the running server.
        """
        log = self.query_one("#run-log", Log)
        if self._dash_proc is not None and self._dash_proc.poll() is None:
            log.write_line("[dashboard] Already running at http://localhost:7860")
            return
        self._dash_proc = subprocess.Popen(
            ["uv", "run", "embedeval", "dashboard",
             "--results", str(tui_config.RESULTS_DIR),
             "--cases", str(tui_config.CASES_DIR)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        log.write_line("[dashboard] Starting at http://localhost:7860 …")

    def action_new_run(self) -> None:
        self.push_screen(RunFormScreen(self._cases), self._on_run_config)

    @on(Button.Pressed, "#btn-new-run")
    def on_new_run_button(self) -> None:
        self.action_new_run()

    def action_stop_run(self) -> None:
        """Terminate the active run and drop any queued runs."""
        log = self.query_one("#run-log", Log)
        dropped = len(self._pending_runs)
        self._pending_runs.clear()
        if self._proc is None or self._proc.poll() is not None:
            log.write_line("[stop] No run is currently active.")
            return
        # Ask the child to stop, then force-kill if it ignores SIGTERM.
        self._proc.terminate()
        try:
            self._proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self._proc.kill()
        msg = "[stop] Run interrupted by user."
        if dropped:
            msg += f" Dropped {dropped} queued run(s)."
        log.write_line(msg)
        # _stream_output will observe the exit and call _finish_run, which
        # refreshes the leaderboard and clears the progress bar.

    @on(Button.Pressed, "#btn-stop-run")
    def on_stop_run_button(self) -> None:
        self.action_stop_run()

    def _on_run_config(self, config: dict | None) -> None:
        if config is None:
            return
        models = config.pop("models")
        # Build one config per model and queue them all.
        configs = [{**config, "model": m} for m in models]
        if self._proc is not None and self._proc.poll() is None:
            # A run is already active — queue everything for later.
            self._pending_runs.extend(configs)
            log = self.query_one("#run-log", Log)
            log.write_line(f"[queued] {len(configs)} model run(s) queued.")
            return
        # Launch first immediately, queue the rest.
        self._pending_runs.extend(configs[1:])
        self._launch_run(configs[0])

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
        run_in_docker = bool(config.get("run_in_docker"))

        # Inside the container the compose service mounts ./cases -> /app/cases
        # and ./results -> /app/results, with WORKDIR /app. A host-absolute
        # path would not exist in the container, so use the fixed mount paths.
        if run_in_docker:
            cases_arg = "cases"
            output_arg = "results"
        else:
            cases_arg = cases_path
            output_arg = str(tui_config.RESULTS_DIR)

        mode = config.get("mode", "run")
        if mode == "agent":
            # Agent mode: model is a positional arg, turns replace attempts.
            cmd = [
                "uv", "run", "embedeval", "agent",
                config["model"],
                "--cases", cases_arg,
                "--output-dir", output_arg,
                "--max-turns", str(config["max_turns"]),
            ]
            if selected:
                cmd += ["--case-ids", ",".join(selected)]
            else:
                if config.get("sdk_filter", "all") != "all":
                    cmd += ["--sdk", config["sdk_filter"]]
                if config.get("cat_filter", "all") != "all":
                    cmd += ["--category", config["cat_filter"]]
            if config.get("resume_from"):
                cmd += ["--resume", config["resume_from"]]
            if config.get("context_pack", "none") != "none":
                cmd += ["--context-pack", config["context_pack"]]
        else:
            cmd = [
                "uv", "run", "embedeval", "run",
                "--model", config["model"],
                "--cases", cases_arg,
                "--output-dir", output_arg,
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
        if mode == "run" and config["force"]:
            cmd.append("--force")
        if mode == "run" and config["no_think"]:
            cmd.append("--no-think")
        # Verbose so runner emits INFO lines ("Case X attempt N: PASS/FAIL")
        # which the TUI parses to drive the progress bar.
        cmd.append("--verbose")

        # L1/L3 compile gates only work inside the embedeval-nxp container
        # (host has no arm-none-eabi toolchain). When requested, wrap the
        # command in `docker compose run`: the service already mounts
        # cases/results and sets EMBEDEVAL_ENABLE_BUILD=1. API keys are
        # forwarded by name (-e KEY) from the env we build below, so they
        # never appear in the logged command line.
        if run_in_docker:
            key_flags: list[str] = []
            for key in ("GROQ_API_KEY", "OPENROUTER_API_KEY"):
                key_flags += ["-e", key]
            # sudo is required to reach the Docker socket on this host
            # (-n: never prompt — a password prompt would hang the subprocess).
            # The image ENTRYPOINT is ["uv", "run", "embedeval"], so we drop
            # that prefix from cmd and pass only the subcommand + args.
            inner_args = cmd[3:]  # strip leading "uv run embedeval"
            cmd = [
                "sudo", "-n", "docker", "compose", "run", "--rm",
                *key_flags, "embedeval-nxp",
            ] + inner_args

        # Mirror all run output to a plain-text file so it can be copied.
        self._log_file = tui_config.RESULTS_DIR / "tui-run.log"

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
        # Agent mode emits exactly one completion event per case (regardless
        # of how many turns it took); run mode does `attempts` samples per case.
        per_case = 1 if mode == "agent" else config["attempts"]
        self._run_total = n_cases * per_case
        self._run_done = 0
        self._run_pass = 0
        self._run_fail = 0
        self._run_error = 0
        self._run_current = ""
        self._run_model = config["model"]
        self._run_started_at = time.monotonic()
        self._run_seen = set()
        # Tick once a second so elapsed time advances even while a single
        # case is running (no case event arrives to redraw the bar).
        if self._run_timer is not None:
            self._run_timer.stop()
        self._run_timer = self.set_interval(1.0, self._update_progress_bar)

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
        project_root = tui_config.RESULTS_DIR.parent

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
        self.call_from_thread(
            self._append_log,
            f"[done] exit {rc}  —  {self._run_pass} pass  "
            f"{self._run_fail} fail  {self._run_error} error",
        )
        # Auto-refresh results after a run completes.
        self.call_from_thread(self._finish_run)

    def _finish_run(self) -> None:
        """Called on the main thread when the subprocess exits."""
        self._load_data()
        # Stop the elapsed-time ticker; a queued run will restart it.
        if self._run_timer is not None:
            self._run_timer.stop()
            self._run_timer = None
        self._run_total = 0
        self._run_done = 0
        # Launch next queued run if any.
        if self._pending_runs:
            next_config = self._pending_runs.pop(0)
            log = self.query_one("#run-log", Log)
            remaining = len(self._pending_runs)
            log.write_line(
                f"[queue] Starting next run: {next_config['model']}"
                + (f"  ({remaining} more queued)" if remaining else "")
            )
            self._launch_run(next_config)
        else:
            # No more runs: replace the progress bar with the leaderboard
            # summary so a stale "Running…" line does not linger.
            self._refresh_table()

    def _append_log(self, line: str) -> None:
        # Always write full output to file for debugging.
        if hasattr(self, "_log_file"):
            with self._log_file.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
        self._parse_progress(line)
        # Write only human-relevant events to the widget.
        widget_line = _format_log_line(line)
        if widget_line is not None:
            log = self.query_one("#run-log", Log)
            log.write_line(widget_line)

    def _parse_progress(self, line: str) -> None:
        """Extract case completion events from verbose runner output.

        The runner emits: "Case <id> attempt <n>: PASS" or "FAIL@L<n>"
        via logger.info (visible only with --verbose).
        """
        # e.g. "INFO:embedeval.runner:Case nxp-mcxc-i2c-001 attempt 1: PASS"
        # Infrastructure errors use a different log format — handled separately below.
        u = _CASE_UNHANDLED_RE.search(line)
        if u:
            case_id, attempt = u.group(1), u.group(2)
            self._run_current = case_id
            # Count each (case, attempt) only once — see _run_seen note.
            if (case_id, attempt) in self._run_seen:
                return
            self._run_seen.add((case_id, attempt))
            self._run_done += 1
            self._run_error += 1
            self._update_progress_bar()
            return

        # Agent mode: one completion event per case (passed/failed on turn N/M).
        # Dedup on case_id alone since the agent emits exactly one such line.
        a = _AGENT_RESULT_RE.search(line)
        if a:
            case_id, status = a.group(1), a.group(2)
            self._run_current = case_id
            if (case_id, "agent") in self._run_seen:
                return
            self._run_seen.add((case_id, "agent"))
            self._run_done += 1
            if status == "passed":
                self._run_pass += 1
            else:
                self._run_fail += 1
            self._update_progress_bar()
            return

        m = re.search(r"Case (\S+) attempt (\d+): (PASS|FAIL@L\S+|FAIL)", line)
        if not m:
            return
        case_id, attempt, status = m.group(1), m.group(2), m.group(3)
        self._run_current = case_id
        if (case_id, attempt) in self._run_seen:
            return
        self._run_seen.add((case_id, attempt))
        self._run_done += 1
        if status == "PASS":
            self._run_pass += 1
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
        # Clamp so a miscount can never render a bar past 100%.
        frac = min(done / total, 1.0)
        filled = round(frac * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)
        pct = int(frac * 100)
        elapsed = self._format_elapsed(time.monotonic() - self._run_started_at)
        summary = self.query_one("#summary-bar", Static)
        summary.update(
            f"  Running  [{bar}]  {done}/{total} ({pct}%)"
            f"  {self._run_model}  {self._run_current}"
            f"  ·  {elapsed} elapsed"
            f"  ·  {self._run_pass} pass  {self._run_fail} fail  {self._run_error} error"
        )

    @staticmethod
    def _format_elapsed(seconds: float) -> str:
        """Format an elapsed duration as M:SS (or H:MM:SS past an hour)."""
        total = int(seconds)
        hours, rem = divmod(total, 3600)
        minutes, secs = divmod(rem, 60)
        if hours:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"
