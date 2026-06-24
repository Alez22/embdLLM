"""New Run modal: model selection (dynamic catalog) and case selection."""
from __future__ import annotations

from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    Checkbox,
    Input,
    Label,
    Select,
    SelectionList,
)

from embedeval.model_catalog import ModelInfo, fetch_models
from embedeval.tui import config

_CUSTOM_MODEL = "__custom__"


def _model_label(info: ModelInfo) -> str:
    """Human-readable row label: slug plus price tag.

    Free models are tagged ``[free]``; priced ones show $/Mtok; Groq
    (unknown price) shows ``[?]``.
    """
    if info.price_per_mtok is None:
        tag = "[?]"
    elif info.is_free:
        tag = "[free]"
    else:
        tag = f"${info.price_per_mtok:.2f}/Mtok"
    return f"{info.slug}  {tag}"


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
        height: 14;
        border: solid $primary-darken-2;
    }
    #model-filter-row {
        height: auto;
        margin-top: 1;
    }
    #model-filter-row Select {
        width: 1fr;
        margin-right: 1;
    }
    #input-model-search {
        margin-top: 1;
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
    #model-status {
        height: auto;
        color: $text-muted;
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
        # Full catalog (filled by the background worker) and the slugs the
        # user has selected so selection survives list rebuilds on filtering.
        self._catalog: list[ModelInfo] = []
        self._selected_models: set[str] = set()

    def _sdk_options(self) -> list[tuple[str, str]]:
        sdks = sorted({c.get("sdk", "") for c in self._cases if c.get("sdk")})
        return [("All SDKs", "all")] + [(s, s) for s in sdks]

    def _category_options(self) -> list[tuple[str, str]]:
        cats = sorted(
            {c.get("category", "") for c in self._cases if c.get("category")}
        )
        return [("All categories", "all")] + [(c, c) for c in cats]

    def _visible_models(self) -> list[ModelInfo]:
        """Return catalog entries matching the active model filters.

        Combines: sub-provider Select, free/paid Select, and the search
        substring. Result is sorted by price (unknown last) then slug so
        cheaper models surface first.
        """
        provider = str(self.query_one("#sel-model-provider", Select).value)
        pricing = str(self.query_one("#sel-model-pricing", Select).value)
        search = self.query_one("#input-model-search", Input).value.strip().lower()

        def keep(info: ModelInfo) -> bool:
            if provider != "all" and info.sub_provider != provider:
                return False
            if pricing == "free" and not info.is_free:
                return False
            if pricing == "paid" and (info.is_free or info.price_per_mtok is None):
                return False
            if search and search not in info.slug.lower():
                return False
            return True

        def sort_key(info: ModelInfo) -> tuple[float, str]:
            # Unknown price sorts after all known prices.
            price = info.price_per_mtok
            return (price if price is not None else float("inf"), info.slug)

        return sorted((m for m in self._catalog if keep(m)), key=sort_key)

    def _provider_options(self) -> list[tuple[str, str]]:
        """Build sub-provider Select options from the loaded catalog."""
        subs = sorted({m.sub_provider for m in self._catalog})
        return [("All providers", "all")] + [(s, s) for s in subs]

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
        with Container(id="run-form"):
            yield Label("New Run", id="form-title")

            with Horizontal(id="form-columns"):

                # --- Left column: model config ---
                with Container(id="col-model"):
                    with Horizontal(id="model-filter-row"):
                        yield Select(
                            [("All providers", "all")],
                            value="all",
                            id="sel-model-provider",
                            allow_blank=False,
                        )
                        yield Select(
                            [("All prices", "all"), ("Free only", "free"),
                             ("Paid only", "paid")],
                            value="all",
                            id="sel-model-pricing",
                            allow_blank=False,
                        )
                    yield Input(
                        placeholder="Search models (e.g. claude, qwen)",
                        id="input-model-search",
                    )
                    with Horizontal(id="models-header"):
                        yield Label("Models (select one or more)")
                        yield Button("All", variant="default", id="btn-models-all")
                        yield Button("None", variant="default", id="btn-models-none")
                    yield SelectionList[str](id="models-list")
                    yield Label("Loading models…", id="model-status")
                    with Container(id="custom-model-row"):
                        yield Input(
                            placeholder="Custom model (e.g. groq/llama-3.3-70b-versatile)",
                            id="input-custom-model",
                        )

                    yield Label("Mode")
                    yield Select(
                        [("run (single-shot)", "run"),
                         ("agent (multi-turn)", "agent")],
                        value="run",
                        id="sel-mode",
                        allow_blank=False,
                    )

                    # Agent-only fields. Shown/hidden by on_mode_changed.
                    yield Label("Max turns (agent mode)", id="lbl-max-turns")
                    yield Input("3", id="input-max-turns")
                    yield Label("Resume from run dir (agent, optional)",
                                id="lbl-resume")
                    yield Input(placeholder="results/runs/..._tN",
                                id="input-resume")

                    yield Label("Attempts  (min 5 for consistency metric)")
                    yield Input("5", id="input-attempts")

                    yield Label("Temperature (0.0 = deterministic)")
                    yield Input("0.5", id="input-temperature")

                    yield Checkbox("--force (bypass cache)", id="check-force")
                    yield Checkbox("--no-think", id="check-no-think")

                # --- Right column: case selection ---
                with Container(id="col-cases"):
                    yield Label("Cases dir")
                    yield Input(str(config.CASES_DIR), id="input-cases-dir")

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

                    # Layers to run. L0 (static) is always on. L1/L3 are
                    # compile gates that only work inside the embedeval-nxp
                    # container — selecting either makes the run launch in
                    # Docker (see _launch_run in app.py).
                    yield Label("Layers")
                    yield Checkbox("L0 static (always on)", value=True,
                                   disabled=True, id="check-layer-l0")
                    yield Checkbox("L1 compile gate (runs in Docker)",
                                   value=True, id="check-layer-l1")
                    yield Checkbox("L3 build/run (runs in Docker)",
                                   value=True, id="check-layer-l3")

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

    # --- Model catalog: async load and list rebuild ---

    def on_mount(self) -> None:
        """Kick off the catalog fetch without blocking the UI."""
        self._load_catalog()
        self._update_mode_visibility()

    def _update_mode_visibility(self) -> None:
        """Show agent-only fields only in agent mode, attempts only in run."""
        is_agent = str(self.query_one("#sel-mode", Select).value) == "agent"
        for wid in ("#lbl-max-turns", "#input-max-turns",
                    "#lbl-resume", "#input-resume"):
            self.query_one(wid).display = is_agent
        # Attempts is meaningless in agent mode (turns replace it).
        self.query_one("#input-attempts").display = not is_agent

    @on(Select.Changed, "#sel-mode")
    def on_mode_changed(self) -> None:
        self._update_mode_visibility()

    @work(thread=True, exclusive=True)
    def _load_catalog(self) -> None:
        """Fetch the model catalog in a worker thread, then update the UI."""
        catalog = fetch_models()
        # Hop back to the UI thread to mutate widgets safely.
        self.app.call_from_thread(self._on_catalog_loaded, catalog)

    def _on_catalog_loaded(self, catalog: list[ModelInfo]) -> None:
        """Populate the provider filter and the model list once loaded."""
        self._catalog = catalog
        self.query_one("#sel-model-provider", Select).set_options(
            self._provider_options()
        )
        self._rebuild_model_list()

    def _rebuild_model_list(self) -> None:
        """Refresh the SelectionList from catalog + active filters.

        Preserves prior selections via ``self._selected_models`` so toggling
        filters does not lose what the user already picked.
        """
        sel_list = self.query_one("#models-list", SelectionList)
        sel_list.clear_options()
        visible = self._visible_models()
        for info in visible:
            sel_list.add_option(
                (_model_label(info), info.slug, info.slug in self._selected_models)
            )
        status = self.query_one("#model-status", Label)
        status.update(
            f"{len(visible)} of {len(self._catalog)} models  ·  "
            f"{len(self._selected_models)} selected"
        )

    @on(SelectionList.SelectedChanged, "#models-list")
    def on_models_selection_changed(self) -> None:
        """Track selections so they survive filter-driven rebuilds."""
        sel_list = self.query_one("#models-list", SelectionList)
        visible_slugs = {info.slug for info in self._visible_models()}
        # Keep selections outside the current filter, update the visible ones.
        self._selected_models -= visible_slugs
        self._selected_models |= set(sel_list.selected)
        self.query_one("#model-status", Label).update(
            f"{len(visible_slugs)} of {len(self._catalog)} models  ·  "
            f"{len(self._selected_models)} selected"
        )

    @on(Select.Changed, "#sel-model-provider")
    @on(Select.Changed, "#sel-model-pricing")
    def on_model_filter_changed(self) -> None:
        self._rebuild_model_list()

    @on(Input.Changed, "#input-model-search")
    def on_model_search_changed(self) -> None:
        self._rebuild_model_list()

    @on(Button.Pressed, "#btn-models-all")
    def on_models_select_all(self) -> None:
        """Select every model currently visible under the filters."""
        for info in self._visible_models():
            self._selected_models.add(info.slug)
        self._rebuild_model_list()

    @on(Button.Pressed, "#btn-models-none")
    def on_models_select_none(self) -> None:
        """Deselect every model currently visible under the filters."""
        for info in self._visible_models():
            self._selected_models.discard(info.slug)
        self._rebuild_model_list()

    @on(Button.Pressed, "#btn-cancel")
    def cancel(self) -> None:
        self.dismiss(None)

    @on(Button.Pressed, "#btn-run")
    def confirm(self) -> None:
        # Collect selected catalog models (sorted for stable run order).
        models: list[str] = sorted(self._selected_models)
        # Add custom model if provided (escape hatch for off-catalog slugs).
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
        # L1/L3 are compile gates: either one selected means the run needs
        # the Docker build environment (EMBEDEVAL_ENABLE_BUILD).
        run_in_docker = (
            self.query_one("#check-layer-l1", Checkbox).value
            or self.query_one("#check-layer-l3", Checkbox).value
        )
        mode = str(self.query_one("#sel-mode", Select).value)
        max_turns_raw = self.query_one("#input-max-turns", Input).value.strip()
        try:
            max_turns = max(1, int(max_turns_raw))
        except ValueError:
            max_turns = 3
        resume_from = self.query_one("#input-resume", Input).value.strip()
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
                "mode": mode,
                "max_turns": max_turns,
                "resume_from": resume_from,
                "cases_dir": cases_dir,
                "attempts": attempts,
                "temperature": temperature,
                "force": force,
                "no_think": no_think,
                "run_in_docker": run_in_docker,
                "selected_cases": selected_cases,
                "sdk_filter": sdk_filter,
                "cat_filter": cat_filter,
            }
        )
