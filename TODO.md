# TODO

Tasks are ordered by dependency. Complete Phase 1 before moving to Phase 2.
Mark done with `[x]`. Add notes inline after `—`.

---

## Phase 1 — NXP Infrastructure

Foundation required before any NXP cases can be validated.

- [x] **Fork embedeval upstream** and set up this repo as the working base.
- [x] **Add `src/embedeval/check_utils_nxp.py`** — helpers specific to MCUXpresso SDK:
  - `no_nxp_hallucination(code)` → list of foreign APIs found (STM32 HAL, Zephyr, Arduino)
  - `has_clock_gate_before(code, peripheral)` → bool, checks ordering
  - `has_pinmux_before_init(code)` → bool
  - Common NXP SDK token lists: `FSL_HEADERS`, `CLOCK_APIS`, `PORT_APIS`, `GPIO_APIS`
- [ ] **Define `cases/SDK_LAYOUT_NXP.yaml`** — NXP SDK structure, following the pattern
  of the upstream `cases/SDK_LAYOUT.yaml`.
- [ ] **Docker image for NXP compile check (L1):**
  - Base: `debian:bookworm-slim`
  - Install: `arm-none-eabi-gcc`, `arm-none-eabi-newlib`
  - Add: MCUXpresso SDK headers (CMSIS + fsl_* drivers for MCXC144)
  - Target: compile a minimal bare-metal main.c with `-mcpu=cortex-m0plus -mthumb`
  - Dockerfile at `Dockerfile.nxp`
- [x] **Add `nxp_bare_metal` platform to `src/embedeval/models.py`** (Platform enum).
- [x] **Write first reference case `nxp-mcxc-i2c-001`** end-to-end and verify it passes validate.

---

## Phase 2 — NXP Generation Cases (implicit knowledge)

10 core cases covering the most relevant categories for audio amplifier firmware.
Each prompt must NOT mention safety requirements — implicit knowledge only.

- [x] `nxp-gpio-001` — GPIO output init + toggle. Implicit: clock gate, pin mux order.
- [x] `nxp-gpio-002` — GPIO input with edge IRQ. Implicit: NVIC enable, volatile flag, ISR naming.
- [x] `nxp-i2c-001` — I2C master register read. Implicit: clock, pin mux, address shift, error check. — done as `nxp-mcxc-i2c-001`
- [x] `nxp-i2c-002` — I2C master write + read sequence. Implicit: two separate transfers, address not pre-shifted.
- [x] `nxp-spi-001` — SPI master transfer with manual CS. Implicit: CS assert order, clock polarity, idle-high.
- [x] `nxp-uart-001` — UART TX blocking. Implicit: clock enable, enableTx in config.
- [x] `nxp-uart-002` — UART RX interrupt-driven with ring buffer. Implicit: volatile ring buffer, NVIC, RX flag check.
- [x] `nxp-timer-001` — Periodic PIT interrupt. Implicit: clock gate, NVIC, volatile counter, flag clear in ISR.
- [x] `nxp-isr-001` — ISR-to-main data transfer. Implicit: volatile flag + value, ready flag cleared before consume.
- [x] `nxp-flash-001` — Flash sector erase + write + verify. Implicit: erase before write, erase key, status check.
- [x] `nxp-flash-002` — Power-loss safe write pattern. Implicit: two slots, inactive-first, CRC excludes CRC field.
- [x] `nxp-watchdog-001` — WDT init + feed in main loop. Implicit: LPO clock source, long timeout, refresh in loop.

---

## Phase 3 — New Task Types

Task types absent from all existing embedded LLM benchmarks.

### Refactoring (fully automated grading)
- [ ] **Define refactoring case format** — extend `metadata.yaml` with:
  ```yaml
  task_type: refactoring
  metrics:
    cyclomatic_complexity_max: 5   # target ceiling
    stack_budget_bytes: 128        # target ceiling
  ```
- [ ] **Add lizard integration** to check pipeline — measure cyclomatic complexity before/after.
- [ ] `nxp-refactor-001` — Function with complexity > 10, deeply nested, no early returns.
  Target: complexity ≤ 5, same behavior, regression tests green.
- [ ] `nxp-refactor-002` — Function with large stack locals.
  Target: stack usage reduced ≥ 30%, same behavior.

### Documentation generation (human review)
- [ ] **Define `checks/review.py` rubric format** (see CLAUDE.md).
- [ ] `nxp-doxygen-001` — Undocumented module with 3-4 public functions.
  Rubric: @brief present, @param for each argument, @retval for non-void, no hallucinated params.
- [ ] `nxp-doxygen-002` — ISR + callback-heavy module. Tests if the model documents timing constraints.

### Code explanation (human review)
- [ ] `nxp-explain-001` — Legacy obfuscated bare-metal init sequence (~50 lines).
  Rubric: identifies all peripherals initialized, explains clock tree, flags any unsafe patterns.

### Test generation (automated)
- [ ] **Define Unity test case format** — prompt provides module header + implementation,
  asks for Unity test file.
- [ ] **Grading pipeline:** generated tests compile + link against reference impl (pass),
  then against a mutated impl (must catch the mutation → fail).
- [ ] `nxp-test-001` — Simple module (ring buffer). Generate Unity tests covering: empty, full, wrap-around.
- [ ] `nxp-test-002` — Flash driver module. Generate Unity tests for: write, erase, verify, partial-write recovery.

### Architectural reasoning (human review)
- [ ] `nxp-arch-001` — "Design a power-loss safe configuration storage system for a bare-metal
  NXP device with 256KB flash. Devices may lose power at any point during a write."
  Rubric: WAL or equivalent, scratch area, metadata/CRC validation, recovery on boot, no dynamic alloc.

---

## Phase 4 — Results Dashboard

Web dashboard locale per esplorare i risultati del benchmark: confronto
codice generato vs reference, check pass/fail, leaderboard visiva, storico run.

**Dipendenze:** `fastapi`, `uvicorn` (da aggiungere a `pyproject.toml`).
**Avvio:** `uv run embedeval dashboard` → apre `http://localhost:7860`.
**Fonte dati:** legge direttamente i JSON esistenti in `results/` e i file
`reference/main.c` + `metadata.yaml` dei casi — nessun DB aggiuntivo.

- [x] **Aggiungere `fastapi` e `uvicorn`** a `pyproject.toml`.
- [x] **`src/embedeval/dashboard.py`** — server FastAPI:
  - `GET /` → leaderboard: tabella modelli × casi, celle colorate pass/fail/non-runnato
  - `GET /case/<case_id>/<model>` → dettaglio: check list + diff side-by-side generato vs reference
  - `GET /history` → lista run ordinata per data con Status e Tokens out; click apre dettaglio
  - `GET /history/<run_id>` → per-run detail: checks pass/fail + diff side-by-side per ogni caso
  - `GET /cases` → elenco casi con sdk, difficulty, category, tier, tags
  - `GET /cases/<id>` → prompt e reference editabili (POST per salvare con conferma)
  - `GET /cases/<id>/checks` → static.py e behavior.py read-only con syntax highlight (Python ok, C noto issue)
- [x] **Aggiungere `dashboard` subcommand a `src/embedeval/cli.py`**.
- [ ] **Verificare che con `--attempts N` tutti gli attempt vengano salvati**
  come file separati in `results/runs/*/details/` (bug osservato: con n=3
  viene scritto un solo file).

---

## Phase 5 — Human Review Workflow

- [ ] **`src/embedeval/review.py`** — new module:
  - `load_review_cases(cases_dir)` — discover cases with `checks/review.py`
  - `llm_prescreen(case, generated_code, reviewer_model)` → structured JSON per rubric criterion
  - `run_review_session(cases, results_dir, reviewer_model)` — CLI loop
- [ ] **CLI review interface** (`uv run embedeval review`):
  - Display: prompt / generated code / LLM analysis side by side (rich layout)
  - Per criterion: show LLM score + justification, prompt human confirm/override
  - Save: human scores + override notes to `results/review/` JSON
- [ ] **Add `review` subcommand to `src/embedeval/cli.py`**.
- [ ] **LLM pre-screener prompt** — structured output, JSON only:
  ```
  Evaluate this embedded C code against the rubric.
  For each criterion output: {"criterion": ..., "score": 0|1, "justification": "...", "snippet": "..."}
  ```
- [ ] **Integrate review scores into reporter** — `LEADERBOARD.md` shows automated + review scores separately.

---

## Phase 6 — Cloud Model Integration

- [x] **Verify Groq provider** works end-to-end with embedeval LiteLLM client:
  - `groq/llama-3.3-70b-versatile` ✓
  - `groq/qwen/qwen3-32b` ✓ (con `--no-think` per il limite TPM)
  - `groq/openai/gpt-oss-20b` ✓
  - `groq/openai/gpt-oss-120b` ✓
  - `groq/meta-llama/llama-4-scout-17b-16e-instruct` ✓
- [ ] **Verify OpenRouter provider**:
  - `openrouter/mistralai/devstral-small`
  - `openrouter/qwen/qwen3-coder`
- [ ] **Document model strings** in `docs/MODELS.md` — name, provider, approx cost/1k tokens,
  context window, notes on embedded code quality.
- [x] **Run baseline on all Phase 2 cases** — 3 models × 12 NXP cases completed:
  - `groq/llama-3.3-70b-versatile`: 0/12 pass, 61% avg — omits fsl_clock.h/fsl_port.h
  - `groq/openai/gpt-oss-120b`: 3/12 pass, 84% avg — best overall
  - `groq/openai/gpt-oss-20b`: 1/12 pass, 51% avg — inconsistent on ISR cases
  - [ ] Still to run: `anthropic/claude-sonnet-4-20250514` (reference ceiling), Qwen3
- [x] **Publish initial leaderboard** in `results/LEADERBOARD.md`. — aggiornato ad ogni run

---

## Phase 7 — Knowledge Currency Probing

Tests whether the model's knowledge of a framework is current or stale.
This is a separate axis from capability — a highly capable model with an old training
cutoff will fail these. Score separately in the leaderboard (currency score vs capability score).

### Infrastructure
- [ ] **Extend `metadata.yaml`** with `knowledge_probe` block:
  ```yaml
  knowledge_probe:
    framework: zephyr          # zephyr | mcuxpresso | freertos
    framework_version_required: "3.6"
    deprecated_pattern: device_get_binding
    current_pattern: DEVICE_DT_GET
    change_introduced_in: "2.7"
    change_description: "device_get_binding() deprecated, DEVICE_DT_GET() macro introduced"
  ```
- [ ] **Add `--probe-only` filter** to CLI — run only knowledge_probe cases.
- [ ] **Separate currency score** in reporter and LEADERBOARD.md:
  - `capability_score`: all non-probe cases
  - `currency_score`: probe cases only, broken down by framework and change version
- [ ] **Correlate with training cutoff** — add a `results/CURRENCY-ANALYSIS.md` that maps
  per-model currency scores to known training cutoff dates.

### Zephyr — Breaking API Changes

Each case: prompt asks to use a feature, static check verifies current vs deprecated API.

- [ ] `zephyr-probe-device-001` — Device access pattern.
  - Deprecated: `device_get_binding("I2C_0")` (removed in 3.x)
  - Current: `DEVICE_DT_GET(DT_NODELABEL(i2c0))`
  - Change introduced: Zephyr 2.7

- [ ] `zephyr-probe-i2c-001` — I2C burst read.
  - Deprecated: `i2c_burst_read()`
  - Current: `i2c_write_read()`
  - Change introduced: Zephyr 3.0

- [ ] `zephyr-probe-gpio-001` — GPIO pin write.
  - Deprecated: `gpio_pin_write()`
  - Current: `gpio_pin_set()`
  - Change introduced: Zephyr 2.5

- [ ] `zephyr-probe-include-001` — Kernel include path.
  - Deprecated: `#include <kernel.h>`
  - Current: `#include <zephyr/kernel.h>` (zephyr/ prefix)
  - Change introduced: Zephyr 3.0

- [ ] `zephyr-probe-dt-001` — Device tree label macro.
  - Deprecated: `DT_LABEL(DT_NODELABEL(uart0))`
  - Current: direct node reference without DT_LABEL
  - Change introduced: Zephyr 3.0

- [ ] `zephyr-probe-flash-001` — Flash write protection.
  - Deprecated: `flash_write_protection_set()` (removed entirely)
  - Current: protection handled via partition manager, not explicit API call
  - Change introduced: Zephyr 3.1

- [ ] `zephyr-probe-thread-001` — Thread stack definition.
  - Deprecated: `K_THREAD_STACK_DEFINE` with old parameter order
  - Current: verify model uses correct `K_THREAD_DEFINE` signature for current Zephyr
  - Change introduced: Zephyr 2.6

### MCUXpresso SDK — Breaking API Changes

More opaque changelog than Zephyr — populate from SDK release notes as encountered.

- [ ] Research MCUXpresso SDK 2.x → 3.x breaking changes and document in
  `docs/NXP-CHANGELOG-PROBE.md` before writing cases.
- [ ] `nxp-probe-clock-001` — Clock enable API (if changed between SDK versions).
- [ ] `nxp-probe-dma-001` — DMA channel config structure (if fields renamed).

### Methodology note
- [ ] Add section to `docs/NXP-CONSIDERATIONS.md` explaining the currency vs capability
  distinction and how to interpret the two scores together.

---

## Phase 8 — Language-variant evaluation (IT/EN prompt reproducibility)

**Depends on:** Phase 1 (L1 compile) and Phase 3 (lizard + .text measurement).
Reuses the existing repetition mechanism (`--attempts`) — not a new subsystem,
just a second prompt variant layered on top of existing repetitions.

### Objective
Measure how much the prompt language (Italian vs English), at identical
specification and level of detail, affects the quality and consistency of the
code a model produces.

### Why
An LLM is non-deterministic: the same prompt at temperature > 0 produces
different outputs across runs. There is a baseline "sampling noise" independent
of language. The goal is NOT perfect reproducibility (unreachable) but to
determine whether language is a source of variation *significant relative to
that noise*. Language sensitivity is itself a reliability indicator: a model
that yields the same result in IT and EN is preferable to one that degrades in
one language. Especially relevant for small local models, which have seen less
Italian technical text.

### Tasks
- [ ] **Select 3 tasks per benchmark category**, stratified by difficulty:
  1 easy, 1 medium, 1 hard. Rationale: the language effect can interact with
  difficulty (tends to grow on harder tasks). Choosing 3 easy tasks would hide
  exactly the most interesting phenomenon.
  - Note: start with a subset of categories (e.g. 3-4) to validate the method
    before scaling to all NXP categories — full run is ~30 tasks x 2 langs x 5
    reps = 300 runs/model. Decide scope before generating cases.
- [ ] **Prepare each task in two prompt variants, IT and EN**, with identical
  specification and detail. Only the prompt language changes.
  - Store as `prompt.md` (EN) + `prompt.it.md` (IT) in the same case folder.
- [ ] **Run 5 repetitions per variant**, temperature > 0.

### Metrics (objective only, already in the harness)
- compiles with arm-gcc (yes/no)
- passes unit tests (% of tests passed)
- cyclomatic complexity (lizard)
- .text section size

From these, two quantities to compare:
- **Intra-variant variance**: divergence across the 5 runs of the same language.
  This is the sampling-noise floor.
- **Inter-variant difference**: divergence between IT and EN results.

### Implementation gaps to resolve first
- [ ] **Define the metric aggregation method.** The four metrics have different
  units (bool / % / int / bytes). Normalize before comparing intra vs inter
  variance — use coefficient of variation per metric, or z-score normalization,
  then aggregate into a single per-category sensitivity number. Document the
  chosen method in `docs/LANGUAGE-VARIANT-METHOD.md`.
- [ ] **Handle the binary metric correctly.** "Compiles y/n" over 5 runs is a
  pass proportion (e.g. 4/5), not a continuous std-dev. Treat it as a proportion
  (use its standard error), not as a deviation.

### Reading rule
The language effect is real only if the inter-variant difference EXCEEDS the
intra-variant variance. Below that threshold, the difference is
indistinguishable from sampling noise and is reported as "no measurable effect".

### Output
- [ ] Per model, a per-category "language sensitivity" reported alongside the
  other benchmark metrics as a reliability indicator, in `results/LEADERBOARD.md`.

---

## Phase 9 — Incremental execution (two-tier cache)

**Goal:** consume the fewest tokens possible and avoid useless regenerations.
Treat results as a persistent corpus, not as one-shot runs. Each launch reconciles
the requested grid (cases x models x attempts at given params) against what already
exists, and runs ONLY the missing cells.

**Timing:** worth doing BEFORE the token-heavy phases (5, 6, 7) so iterative
re-runs while authoring cases don't re-burn the LLM calls.

### Two separate caches

- [x] **Generation cache** — stores the model output (`generated_code`).
  - Key: `(prompt_hash, model, temperature, generation_params, attempt_index)`
  - `prompt_hash` = SHA256 of the full prompt as sent (post context_pack + no_think).
    Editing a prompt causes a cache miss and regenerates.
  - `generation_params` = `{feedback_rounds, no_think}` (sorted dict, stable key).
  - Store: `results/corpus/<model_slug>/<case_id>/<attempt>.json` (CorpusCell).
  - Implemented in `src/embedeval/corpus.py`.

- [ ] **Grading cache** — stores check results, applied on top of generated_code.
  - Key: `(generated_code_hash, checks_hash)`
  - `checks_hash` = content hash of static.py / behavior.py / review rubric.
  - Effect: tweaking ONLY a check (not the prompt) re-grades from the cached
    generation — no LLM call, near-zero cost. This is the main efficiency win.

### Reconcile logic

- [x] **Subtract present cells** found in the corpus store → skip LLM call on hit.
- [x] **Run only missing cells.** Store each cell immediately after the LLM call.
- [ ] **ensure-N-samples semantics:** "make sure at least N attempts exist", NOT
  "skip if any exists". At temperature > 0 each attempt_index is a distinct sample —
  required for pass@k and the Phase 7 repetition methodology.
  — Currently: all N attempts are re-checked against the corpus; if attempt k exists
  it is reused, if not it is generated. Already correct for the N→N+M top-up case.
  The "5→10 attempts" scenario (generating only indices 6-10) is not yet implemented:
  today the runner iterates `range(1, attempts+1)` and checks each cell individually,
  so it already handles this correctly as long as cells 1-5 are cached. Verify.
- [x] **Lowering attempts is a no-op:** request 3 when 5 exist → corpus hits for 1-3,
  cells 4-5 are ignored (runner only iterates up to `attempts`).

### Force and storage

- [x] **`--force` flag** — bypasses the corpus lookup and regenerates all cells in
  scope, overwriting existing entries. Long form only (`-f` taken by `--feedback-rounds`).
- [x] **Build on a durable store separate from the checkpoint.**
  `results/corpus/` is persistent; `.checkpoint_*.jsonl` remains crash-recovery only.
- [x] **Persist temperature + generation_params in the stored result.**
  `EvalResult` now carries `temperature` and `generation_params`; `CorpusCell` stores
  them as part of the key so mismatches are detected on load.

### Non-determinism note
- [ ] Document in `docs/INCREMENTAL-EXECUTION.md`: stored samples are the ground
  truth. Most providers expose no seed, so a specific past sample cannot be
  reproduced — `--force` generates NEW samples, it does not reproduce old ones.

---

## Dashboard — Miglioramenti futuri

Miglioramenti noti alla dashboard (`src/embedeval/dashboard.py`) non ancora risolti.

- [ ] **Syntax highlight codice C** — `highlight.js` funziona sul Python ma non sul C.
  Il bundle `highlight.min.js` da CDN sembra non includere il language pack C.
  Opzioni da esplorare: usare Pygments lato server (genera HTML colorato senza JS),
  oppure trovare la URL CDN corretta che include tutti i language pack.
- [ ] **Editor checks** — i file `checks/static.py` e `checks/behavior.py` sono oggi
  read-only. Aggiungere la possibilità di editarli dalla dashboard (POST `/cases/<id>/checks/<file>`).
- [ ] **Selettore attempt** nella pagina detail `/history/<run_id>` — oggi viene mostrato
  sempre l'attempt più recente. Con `--attempts N > 1` sarebbe utile poter scegliere
  quale attempt visualizzare.
- [ ] **Filtri leaderboard** — filtrare per SDK, categoria o tier senza ricaricare la pagina.
- [ ] **Link diretto** dalla leaderboard alla pagina caso (`/cases/<id>`) oltre che
  al dettaglio run.

---

## Backlog (not scheduled)

- Hardware-in-the-loop (L5): flash code to real MCXC144 board, verify via serial output.
- Anti-hallucination trap prompts: ask for a peripheral that doesn't exist on MCXC144,
  verify the model refuses or flags the inconsistency instead of fabricating register addresses.
- Sensitivity analysis: run same case with 5 prompt variants, measure score variance.
- Contribute NXP cases upstream to embedeval via PR.
- NXP include pattern: llama-3.3-70b and gpt-oss-20b consistently use `board.h` instead
  of explicit `fsl_clock.h` / `fsl_port.h` — fails L0 on every case. Consider whether
  to relax the check (accept transitive includes) or keep it strict (explicit headers required).
- Fix retry delay per modelli thinking (Qwen3): il `_parse_retry_after` parsifica
  correttamente "try again in Xs" ma non gestisce il formato "350ms" — aggiungere
  il parsing dei millisecondi.
- Indagare perché `gpt-oss-20b` (63%) batte `gpt-oss-120b` (45%) su questo
  benchmark — possibile che il modello più grande sia più prolisso e triggeri
  check negativi (es. `no_zephyr_apis`, `no_cross_platform_hallucination`).
