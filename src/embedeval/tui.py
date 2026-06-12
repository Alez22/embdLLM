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


def _load_leaderboard(cases: list[dict]) -> tuple[list[str], list[dict]]:
    """Aggregate run results into a per-config leaderboard.

    A leaderboard row is identified by the tuple (model, temperature,
    no_think, attempts) — the same model run with different parameters is a
    distinct row. Multiple runs sharing that config are merged: for each case
    the most recent run wins.

    Coverage per SDK = distinct cases tested / total cases of that SDK present
    on disk (cases/). The total score is the global pass-rate (passed cases /
    tested cases) across all SDKs.

    @param cases  Discovered case metadata dicts (provides the SDK denominators).
    @return (sdk_list, rows) where sdk_list is every SDK discovered on disk and
            rows is the leaderboard sorted by pass-rate descending.
    """
    # --- denominator: total cases per SDK from discovery ---
    total_by_sdk: dict[str, int] = {}
    for c in cases:
        sdk = c.get("sdk", "")
        if sdk:
            total_by_sdk[sdk] = total_by_sdk.get(sdk, 0) + 1
    sdk_list = sorted(total_by_sdk)

    runs_root = RESULTS_DIR / "runs"
    if not runs_root.is_dir():
        return sdk_list, []

    # config_key -> {meta, cases: {case_id: {passed, sdk}}}
    groups: dict[tuple, dict] = {}

    # Iterate ascending so later runs overwrite earlier ones per case.
    for run_dir in sorted(runs_root.iterdir()):
        summary_file = run_dir / "summary.json"
        if not summary_file.is_file():
            continue
        try:
            summary = json.loads(summary_file.read_text(encoding="utf-8"))
        except Exception:
            continue

        model = summary.get("model", "")
        if model == "mock" or not model:
            continue

        gen_params = summary.get("generation_params", {})
        no_think = bool(gen_params.get("no_think", False))
        temperature = float(summary.get("temperature", 0.0))
        attempts = int(summary.get("n_samples_per_case", 1))
        key = (model, temperature, no_think, attempts)

        group = groups.setdefault(key, {
            "model": model,
            "temperature": temperature,
            "no_think": no_think,
            "attempts": attempts,
            "cases": {},
        })

        details_dir = run_dir / "details"
        if not details_dir.is_dir():
            continue
        for f in details_dir.glob("*.json"):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            case_id = d.get("case_id") or f.stem
            group["cases"][case_id] = {
                "passed": bool(d.get("passed")),
                "sdk": d.get("sdk", ""),
            }

    rows: list[dict] = []
    for group in groups.values():
        tested_by_sdk: dict[str, int] = {}
        tested_total = 0
        passed_total = 0
        for info in group["cases"].values():
            tested_total += 1
            if info["passed"]:
                passed_total += 1
            sdk = info["sdk"]
            if sdk:
                tested_by_sdk[sdk] = tested_by_sdk.get(sdk, 0) + 1

        coverage: dict[str, tuple[int, int]] = {}
        for sdk in sdk_list:
            coverage[sdk] = (tested_by_sdk.get(sdk, 0), total_by_sdk[sdk])

        pass_rate = passed_total / tested_total if tested_total else 0.0
        rows.append({
            "model": group["model"],
            "temperature": group["temperature"],
            "no_think": group["no_think"],
            "attempts": group["attempts"],
            "coverage": coverage,
            "tested_total": tested_total,
            "passed_total": passed_total,
            "pass_rate": pass_rate,
        })

    rows.sort(key=lambda r: r["pass_rate"], reverse=True)
    return sdk_list, rows





def _score_bar(score: float, width: int = 8) -> str:
    """Return a simple ASCII progress bar for a [0,1] score."""
    filled = round(score * width)
    return "█" * filled + "░" * (width - filled)


# ---------------------------------------------------------------------------
# Run form modal
# ---------------------------------------------------------------------------

_CUSTOM_MODEL = "__custom__"


# Models available in the New Run form regardless of past results.
# Only providers with API keys in .env: Groq and OpenRouter.
_PRESET_MODELS: list[str] = [
    # Groq — verified available via /v1/models (2026-06-07)
    "groq/llama-3.3-70b-versatile",
    "groq/meta-llama/llama-4-scout-17b-16e-instruct",
    "groq/qwen/qwen3-32b",
    "groq/openai/gpt-oss-20b",
    "groq/openai/gpt-oss-120b",
    # OpenRouter — verified available via /api/v1/models (2026-06-07)
    "openrouter/deepseek/deepseek-r1-0528",
    "openrouter/deepseek/deepseek-chat-v3-0324",
    "openrouter/deepseek/deepseek-v4-flash",
    "openrouter/meta-llama/llama-4-maverick",
    "openrouter/meta-llama/llama-3.3-70b-instruct",
    "openrouter/qwen/qwen3-235b-a22b",
    "openrouter/qwen/qwen3-30b-a3b",
    "openrouter/google/gemini-2.5-flash",
    "openrouter/google/gemini-2.5-pro",
    "openrouter/mistralai/mistral-small-3.2-24b-instruct",
]


def _model_to_id(model: str) -> str:
    """Convert model slug to a valid Textual widget ID (no dots, slashes, etc.)."""
    return model.replace("/", "__").replace(".", "_").replace("-", "_")


def _known_models() -> list[str]:
    """Return the verified preset model list only."""
    return _PRESET_MODELS


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
        width: 90%;
        max-width: 160;
        height: 80%;
        overflow-y: auto;
    }
    #form-columns {
        height: auto;
        margin-top: 1;
    }
    #col-model {
        width: 1fr;
        padding-right: 2;
        height: auto;
    }
    #col-cases {
        width: 1fr;
        padding-left: 2;
        border-left: solid $primary-darken-2;
        height: auto;
    }
    #col-model Label, #col-cases Label {
        margin-top: 1;
    }
    #models-list {
        height: 12;
        border: solid $primary-darken-2;
        overflow-y: auto;
        padding: 0 1;
    }
    #provider-filter {
        height: auto;
        margin-top: 1;
        align: left middle;
    }
    #provider-filter Button {
        margin-right: 1;
        min-width: 12;
    }
    #models-header {
        height: auto;
        margin-top: 1;
        align: left middle;
    }
    #models-header Label {
        margin-top: 0;
        width: 1fr;
    }
    #models-header Button {
        margin-left: 1;
        min-width: 6;
    }
    #custom-model-row {
        height: auto;
        margin-top: 1;
    }
    #form-filter-row {
        height: auto;
        margin-top: 1;
    }
    #form-filter-row Select {
        width: 1fr;
    }
    #cases-list {
        height: 16;
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
        min-width: 8;
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
        self._provider_filter: str = "all"

    def _sdk_options(self) -> list[tuple[str, str]]:
        sdks = sorted({c.get("sdk", "") for c in self._cases if c.get("sdk")})
        return [("All SDKs", "all")] + [(s, s) for s in sdks]

    def _category_options(self) -> list[tuple[str, str]]:
        cats = sorted(
            {c.get("category", "") for c in self._cases if c.get("category")}
        )
        return [("All categories", "all")] + [(c, c) for c in cats]

    def _provider_of(self, model: str) -> str:
        """Return the top-level provider name from a model slug (e.g. 'groq')."""
        return model.split("/")[0]

    def _visible_models(self) -> list[str]:
        """Return preset models matching the active provider filter."""
        active = getattr(self, "_provider_filter", "all")
        return [m for m in _known_models() if active == "all" or self._provider_of(m) == active]

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

        with Container(id="run-form"):
            yield Label("New Run", id="form-title")

            with Horizontal(id="form-columns"):

                # --- Left column: model config ---
                with Container(id="col-model"):
                    with Horizontal(id="provider-filter"):
                        yield Button("All providers", variant="primary", id="btn-prov-all")
                        yield Button("Groq", variant="default", id="btn-prov-groq")
                        yield Button("OpenRouter", variant="default", id="btn-prov-openrouter")
                    with Horizontal(id="models-header"):
                        yield Label("Models (select one or more)")
                        yield Button("All", variant="default", id="btn-models-all")
                        yield Button("None", variant="default", id="btn-models-none")
                    with ScrollableContainer(id="models-list"):
                        for model in known:
                            yield Checkbox(model, id=f"model-{_model_to_id(model)}")
                    with Container(id="custom-model-row"):
                        yield Input(
                            placeholder="Custom model (e.g. groq/llama-3.3-70b-versatile)",
                            id="input-custom-model",
                        )

                    yield Label("Attempts  (min 5 for consistency metric)")
                    yield Input("5", id="input-attempts")

                    yield Label("Temperature (0.0 = deterministic)")
                    yield Input("0.5", id="input-temperature")

                    yield Checkbox("--force (bypass cache)", id="check-force")
                    yield Checkbox("--no-think", id="check-no-think")

                # --- Right column: case selection ---
                with Container(id="col-cases"):
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
                        yield Label("Cases (empty = all matching filters)")
                        yield Button("All", variant="default", id="btn-select-all")
                        yield Button("Clear", variant="default", id="btn-clear-all")
                    with ScrollableContainer(id="cases-list"):
                        for case in self._cases:
                            yield Checkbox(
                                case.get("id", ""),
                                id=f"case-{case.get('id', '')}",
                            )

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

    def _apply_provider_filter(self, provider: str) -> None:
        """Show only models belonging to provider; update button variants."""
        self._provider_filter = provider
        for model in _known_models():
            cb = self.query_one(f"#model-{_model_to_id(model)}", Checkbox)
            cb.display = (provider == "all" or self._provider_of(model) == provider)
        # Highlight the active button
        for btn_id, prov in [
            ("btn-prov-all", "all"),
            ("btn-prov-groq", "groq"),
            ("btn-prov-openrouter", "openrouter"),
        ]:
            self.query_one(f"#{btn_id}", Button).variant = (
                "primary" if prov == provider else "default"
            )

    @on(Button.Pressed, "#btn-prov-all")
    def on_prov_all(self) -> None:
        self._apply_provider_filter("all")

    @on(Button.Pressed, "#btn-prov-groq")
    def on_prov_groq(self) -> None:
        self._apply_provider_filter("groq")

    @on(Button.Pressed, "#btn-prov-openrouter")
    def on_prov_openrouter(self) -> None:
        self._apply_provider_filter("openrouter")

    @on(Button.Pressed, "#btn-models-all")
    def on_models_select_all(self) -> None:
        """Check all currently visible model checkboxes."""
        for model in self._visible_models():
            self.query_one(f"#model-{_model_to_id(model)}", Checkbox).value = True

    @on(Button.Pressed, "#btn-models-none")
    def on_models_select_none(self) -> None:
        """Uncheck all currently visible model checkboxes."""
        for model in self._visible_models():
            self.query_one(f"#model-{_model_to_id(model)}", Checkbox).value = False

    @on(Button.Pressed, "#btn-cancel")
    def cancel(self) -> None:
        self.dismiss(None)

    @on(Button.Pressed, "#btn-run")
    def confirm(self) -> None:
        # Collect selected preset models.
        models: list[str] = []
        for model in _known_models():
            cb = self.query_one(f"#model-{_model_to_id(model)}", Checkbox)
            if cb.value:
                models.append(model)
        # Add custom model if provided.
        custom = self.query_one("#input-custom-model", Input).value.strip()
        if custom and custom not in models:
            models.append(custom)
        if not models:
            self.query_one("#input-custom-model", Input).focus()
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

        selected_cases: list[str] = []
        for case in self._cases:
            cid = case.get("id", "")
            cb = self.query_one(f"#case-{cid}", Checkbox)
            if cb.value:
                selected_cases.append(cid)

        self.dismiss(
            {
                "models": models,
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
# Log filtering helpers
# ---------------------------------------------------------------------------

import re as _re

_CASE_RESULT_RE = _re.compile(r"Case (\S+) attempt (\d+): (PASS|FAIL@L(\S+)|FAIL)")
_CASE_UNHANDLED_RE = _re.compile(r"Case (\S+) attempt (\d+): unhandled (\S+)")


def _format_log_line(line: str) -> str | None:
    """Return a human-readable widget line, or None to suppress the line.

    The full raw output is always written to the log file; this function
    controls what appears in the TUI log panel.
    """
    # Launch and done markers.
    if line.startswith("[launch]") or line.startswith("[done]"):
        return line

    # Infrastructure error: unhandled exception in runner (API failure, timeout, etc.)
    u = _CASE_UNHANDLED_RE.search(line)
    if u:
        return f"[ERROR] {u.group(1)} #{u.group(2)}  ({u.group(3)})"

    # Per-attempt result: reformat into a compact, aligned line.
    m = _CASE_RESULT_RE.search(line)
    if m:
        case_id, attempt, status = m.group(1), m.group(2), m.group(3)
        if status == "PASS":
            return f"[ PASS ] {case_id} #{attempt}"
        layer = m.group(4) or "?"
        return f"[ FAIL ] {case_id} #{attempt}  →  L{layer}"

    # Rate-limit warnings worth surfacing.
    low = line.lower()
    if "rate limit" in low or "ratelimiterror" in low:
        return f"[warn ] rate limit — {line.strip()}"

    # Prose response warning: model returned text instead of code.
    if "returned prose" in low:
        # Strip log prefix (e.g. "WARNING:embedeval.llm_client:LLM ...")
        msg = _re.sub(r"^[A-Z]+:[^:]+:", "", line).strip()
        return f"[warn ] {msg}"

    # Generation cache hit — show so the operator knows no LLM call was made.
    mc = _re.search(r"Corpus hit: (\S+) attempt (\d+)", line)
    if mc:
        return f"[cache] {mc.group(1)} #{mc.group(2)}"

    return None


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
        Binding("s", "stop_run", "Stop Run"),
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
        self._cases: list[dict] = _discover_cases(CASES_DIR)
        self._proc: subprocess.Popen | None = None  # type: ignore[type-arg]
        self._pending_runs: list[dict] = []  # queued configs waiting for current run to finish
        self._log_queue: Queue[str] = Queue()
        self._log_file: Path = RESULTS_DIR / "tui-run.log"

        # Progress tracking during an active run.
        self._run_total: int = 0
        self._run_done: int = 0
        self._run_pass: int = 0
        self._run_fail: int = 0
        self._run_error: int = 0
        self._run_current: str = ""
        # Track (case_id, attempt) already counted: the runner can emit both an
        # "unhandled" retry line and a final PASS/FAIL for the same attempt, so
        # counting every matching line double-counts and the bar overshoots 100%.
        self._run_seen: set[tuple[str, str]] = set()

        # Leaderboard columns are built dynamically once SDKs are known.
        self._sdk_list: list[str] = []
        self._rows: list[dict] = []
        self._load_data()

    def _build_columns(self, sdk_list: list[str]) -> None:
        """(Re)build the leaderboard columns for the discovered SDKs."""
        table = self.query_one("#results-table", DataTable)
        table.clear(columns=True)
        table.cursor_type = "row"
        table.add_column("Model", key="model")
        table.add_column("Temp", key="temperature")
        table.add_column("Think", key="think")
        table.add_column("Att.", key="attempts")
        for sdk in sdk_list:
            table.add_column(sdk, key=f"sdk:{sdk}")
        table.add_column("Score", key="score")

    def _load_data(self) -> None:
        self._sdk_list, self._rows = _load_leaderboard(self._cases)
        self._build_columns(self._sdk_list)
        self._refresh_table()

    def _refresh_table(self) -> None:
        table = self.query_one("#results-table", DataTable)
        table.clear()

        for r in self._rows:
            think_str = "no" if r.get("no_think", False) else "yes"
            temp = r.get("temperature", 0.0)
            cells = [
                r.get("model", "").split("/")[-1],
                f"{temp:.1f}",
                think_str,
                str(r.get("attempts", 1)),
            ]
            coverage = r.get("coverage", {})
            for sdk in self._sdk_list:
                tested, total = coverage.get(sdk, (0, 0))
                if total == 0:
                    cells.append("—")
                else:
                    pct = int(tested / total * 100)
                    cells.append(f"{tested}/{total} {pct}%")
            pass_rate = r.get("pass_rate", 0.0)
            cells.append(f"{_score_bar(pass_rate)} {pass_rate:.2f}")
            table.add_row(*cells)

        summary = self.query_one("#summary-bar", Static)
        summary.update(
            f"  {len(self._rows)} model configs  ·  "
            f"coverage = tested/total cases per SDK  ·  "
            f"score = global pass-rate"
        )

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
        self._run_seen = set()

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
        import re
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
        summary = self.query_one("#summary-bar", Static)
        summary.update(
            f"  Running  [{bar}]  {done}/{total} ({pct}%)"
            f"  {self._run_current}"
            f"  ·  {self._run_pass} pass  {self._run_fail} fail  {self._run_error} error"
        )
