# TODO

Tasks are ordered by **current priority** (updated 2026-05-26).
Mark done with `[x]`. Add notes inline after `—`.

## Priority order (next 2-4 weeks)

1. **Phase 4** — Dashboard: improvements (bug --attempts done)
2. **Phase 6** — Cloud model runs: completare modelli mancanti + docs
3. **Phase 3** — Nuovi task types (refactoring, doxygen, test gen, arch)
4. **Phase 5** — Human Review workflow
5. **Phase 1** — Infrastruttura rimanente (SDK_LAYOUT, Docker)
6. **Phase 7** — Knowledge Currency Probing
7. **Phase 8** — Language-variant evaluation
8. **Backlog** — Hardware-in-the-loop, trap prompts, upstream PR

## Code health (from review 2026-05-26)

Punti emersi dalla review del 2026-05-26 — alcuni risolti, altri tracciati come debito.

### Resolved
- [x] **Bug #1**: feedback loop crashava con `failed_at_layer = None` o `> 1`
  dopo il primo round. Fix in commit `82932cb` (while + bounds check + test).
- [x] **Bug #2**: grade cache memorizzava l'intero `EvalResult` keyed solo su
  `(code_hash, checks_hash)` → leak di metadata cross-model. Fix in commit
  `6e61fd7`: nuovo `GradeCell` con solo campi pure-function; runner ricostruisce
  l'`EvalResult` dai metadati della call corrente. Caching rimosso dai feedback
  round (chiave non distinguente).
- [x] **Smoke regression test** end-to-end: commit `e67d1c1`. 6 scenari di
  caching coperti con mock model.

### Aperti — priorità media

- [ ] **`_extract_code` su fence non chiusi** (`src/embedeval/llm_client.py`).
  Se il modello tronca a metà output (limite token), nessun fence di chiusura →
  `_extract_code` ritorna l'intero testo incluso ragionamento. Fix proposto:
  se trovi `\`\`\`(c|cpp)?` di apertura ma nessun match completo, prendi tutto
  dall'apertura alla fine come fallback.
- [ ] **`_call_litellm` swallowa errori non-retryable**: converte qualsiasi
  `Exception` in `RuntimeError`, perdendo classe specifica
  (`BadRequestError`, `AuthenticationError`). Il caller `_make_error_result`
  già usa `type(exc).__name__`, quindi propagare le eccezioni tipizzate dà più
  informazione. Lasciare `except (RateLimitError, ...)` come ora; rimuovere il
  catch-all `except Exception`.
- [ ] **MOCK_C_CODE usa Zephyr**: `llm_client.py:24` ha `#include <zephyr/kernel.h>`
  che fa fallire `no_cross_platform_hallucination` su casi NXP. Probabile
  residuo upstream. Cambiare in un main.c stile bare-metal NXP, o renderlo
  configurabile per SDK.
- [ ] **Allineamento `Platform` enum vs `metadata.yaml`**: il CLAUDE.md mostra
  `platform: nxp_bare_metal` mentre `EvalPlatform.NXP_BARE_METAL = "nxp_bare_metal"`
  esiste. Verificare se il campo `platform` in `CaseMetadata` è ancora vivo o
  deprecated rispetto a `sdk`. Se deprecated, rimuovere dai metadata.

### Aperti — priorità bassa (debito strutturale)

- [ ] **File enormi senza single responsibility**: `cli.py` 1439 righe,
  `check_utils.py` 1430, `evaluator.py` 1180, `reporter.py` 1148,
  `safety_guide.py` 976, `dashboard.py` 943. Quando uno di questi diventa
  doloroso da modificare, estrarre sub-moduli. Non prioritario in assoluto,
  ma il costo cresce nel tempo.
- [ ] **`_RETRY_AFTER_RE` cattura solo "try again in"**: OpenRouter usa
  formati diversi ("retry after Xs"). Quando Phase 6 attiverà OpenRouter,
  estendere il pattern o renderlo provider-aware.
- [ ] **Nessun retry budget complessivo**: `max_retries=6` è per-call.
  Su run di 12 casi × 5 attempt × 3 feedback con rate limit pesante, il
  benchmark può silenziosamente diventare ore di wait. Aggiungere
  `--run-deadline=2h` o accumulatore di wait globale.
- [ ] **Test pre-esistenti fragili**: `test_three_runs_cover_same_case_set`
  (test_context_quality_mode_e2e.py) trova 4 casi UART invece di 2,
  `test_sdk_buckets` fallisce su 2 casi. Non causati da modifiche recenti
  ma indicano fixture che drifta con i casi nuovi.
- [ ] **Semantica `feedback_rounds` vs `attempt`**: il `token_usage` finale
  riflette solo l'ultima call LLM, non la somma su tutti i round. Confronti
  di costo tra modelli con feedback attivo sono sottostimati. Decidere se
  sommare o documentare la convenzione.

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
- [x] **Verificare che con `--attempts N` tutti gli attempt vengano salvati**
  come file separati in `results/runs/*/details/` — fix: nome file ora include
  `_attempt{N}` (`reporter.py:698`), era `{case_id}.json` → ogni attempt sovrascriveva.

### Dashboard — Miglioramenti futuri

Miglioramenti noti alla dashboard non ancora risolti, in ordine di utilità:

- [ ] **Syntax highlight codice C** — `highlight.js` funziona sul Python ma non sul C.
  Il bundle `highlight.min.js` da CDN sembra non includere il language pack C.
  Opzioni: usare Pygments lato server (genera HTML colorato senza JS),
  oppure trovare la URL CDN corretta che include tutti i language pack.
- [ ] **Selettore attempt** nella pagina detail `/history/<run_id>` — oggi viene mostrato
  sempre l'attempt più recente. Con `--attempts N > 1` sarebbe utile poter scegliere
  quale attempt visualizzare.
- [ ] **Filtri leaderboard** — filtrare per SDK, categoria o tier senza ricaricare la pagina.
- [ ] **Editor checks** — i file `checks/static.py` e `checks/behavior.py` sono oggi
  read-only. Aggiungere la possibilità di editarli dalla dashboard (POST `/cases/<id>/checks/<file>`).
- [ ] **Link diretto** dalla leaderboard alla pagina caso (`/cases/<id>`) oltre che
  al dettaglio run.

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
- [ ] **Still to run** on all Phase 2 cases:
  - `anthropic/claude-sonnet-4-20250514` (reference ceiling)
  - `groq/qwen/qwen3-32b` (Qwen3 baseline)
- [ ] **Document model strings** in `docs/MODELS.md` — name, provider, approx cost/1k tokens,
  context window, notes on embedded code quality.
- [ ] **Re-run baseline on all Phase 2 cases** — previous results wiped in
  commit `6b4ac0b` because the runs predated the cache + reporter fixes
  (bugs #1, #2, attempt-file overwrite). Numeri attesi storici per
  riferimento prima del wipe:
  - `groq/llama-3.3-70b-versatile`: 0/12 pass, 61% avg — omits fsl_clock.h/fsl_port.h
  - `groq/openai/gpt-oss-120b`: 3/12 pass, 84% avg — best overall
  - `groq/openai/gpt-oss-20b`: 1/12 pass, 51% avg — inconsistent on ISR cases
- [ ] **Re-publish leaderboard** in `results/LEADERBOARD.md` dopo la prima
  run pulita.

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

## Phase 5 — Human Review Workflow

**Depends on:** Phase 3 (review.py rubric format defined for doxygen/explain/arch cases).

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

## Phase 1 — NXP Infrastructure (remaining)

Foundation items still open — not blocking Phase 2-6 but needed for L1 compile checks.

- [x] Fork embedeval upstream and set up this repo as the working base.
- [x] Add `src/embedeval/check_utils_nxp.py` — helpers specific to MCUXpresso SDK.
- [x] Add `nxp_bare_metal` platform to `src/embedeval/models.py` (Platform enum).
- [x] Write first reference case `nxp-mcxc-i2c-001` end-to-end and verify it passes validate.
- [ ] **Define `cases/SDK_LAYOUT_NXP.yaml`** — NXP SDK structure, following the pattern
  of the upstream `cases/SDK_LAYOUT.yaml`.
- [ ] **Docker image for NXP compile check (L1):**
  - Base: `debian:bookworm-slim`
  - Install: `arm-none-eabi-gcc`, `arm-none-eabi-newlib`
  - Add: MCUXpresso SDK headers (CMSIS + fsl_* drivers for MCXC144)
  - Target: compile a minimal bare-metal main.c with `-mcpu=cortex-m0plus -mthumb`
  - Dockerfile at `Dockerfile.nxp`

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
  Deprecated: `device_get_binding("I2C_0")` → Current: `DEVICE_DT_GET(DT_NODELABEL(i2c0))` (Zephyr 2.7)
- [ ] `zephyr-probe-i2c-001` — I2C burst read.
  Deprecated: `i2c_burst_read()` → Current: `i2c_write_read()` (Zephyr 3.0)
- [ ] `zephyr-probe-gpio-001` — GPIO pin write.
  Deprecated: `gpio_pin_write()` → Current: `gpio_pin_set()` (Zephyr 2.5)
- [ ] `zephyr-probe-include-001` — Kernel include path.
  Deprecated: `#include <kernel.h>` → Current: `#include <zephyr/kernel.h>` (Zephyr 3.0)
- [ ] `zephyr-probe-dt-001` — Device tree label macro.
  Deprecated: `DT_LABEL(DT_NODELABEL(uart0))` → Current: direct node reference (Zephyr 3.0)
- [ ] `zephyr-probe-flash-001` — Flash write protection.
  Deprecated: `flash_write_protection_set()` removed entirely → Current: partition manager (Zephyr 3.1)
- [ ] `zephyr-probe-thread-001` — Thread stack definition signature (Zephyr 2.6).

### MCUXpresso SDK — Breaking API Changes

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

### Objective
Measure whether prompt language (IT vs EN), at identical specification, affects
code quality and consistency beyond normal sampling noise.

### Tasks
- [ ] **Select 3 tasks per benchmark category**, stratified by difficulty (1 easy, 1 medium, 1 hard).
  Start with 3-4 categories to validate the method before scaling (~30 tasks × 2 langs × 5 reps = 300 runs/model).
- [ ] **Prepare each task in two prompt variants** — `prompt.md` (EN) + `prompt.it.md` (IT), identical spec.
- [ ] **Run 5 repetitions per variant**, temperature > 0.
- [ ] **Define the metric aggregation method** — normalize bool/int/bytes metrics before comparing
  intra-variant variance vs inter-variant difference. Document in `docs/LANGUAGE-VARIANT-METHOD.md`.
- [ ] **Handle the binary metric correctly** — compile y/n is a proportion (4/5), use standard error.
- [ ] **Report per model** — per-category "language sensitivity" in `results/LEADERBOARD.md`.

**Reading rule:** language effect is real only if inter-variant difference > intra-variant variance.

---

## Completed — Phase 2 (NXP Generation Cases)

All 12 core NXP generation cases done. Each prompt omits safety requirements — implicit knowledge only.

- [x] `nxp-gpio-001` — GPIO output init + toggle
- [x] `nxp-gpio-002` — GPIO input with edge IRQ
- [x] `nxp-i2c-001` / `nxp-mcxc-i2c-001` — I2C master register read
- [x] `nxp-i2c-002` — I2C master write + read sequence
- [x] `nxp-spi-001` — SPI master transfer with manual CS
- [x] `nxp-uart-001` — UART TX blocking
- [x] `nxp-uart-002` — UART RX interrupt-driven with ring buffer
- [x] `nxp-timer-001` — Periodic PIT interrupt
- [x] `nxp-isr-001` — ISR-to-main data transfer
- [x] `nxp-flash-001` — Flash sector erase + write + verify
- [x] `nxp-flash-002` — Power-loss safe write pattern
- [x] `nxp-watchdog-001` — WDT init + feed in main loop

---

## Completed — Phase 9 (Incremental execution / two-tier cache)

- [x] Generation cache (`results/corpus/<model_slug>/<case_id>/<attempt>.json`)
- [x] Grading cache (`results/corpus/grades/<code_hash>/<checks_hash>.json`)
- [x] ensure-N-samples semantics + top-up + lowering attempts is a no-op
- [x] `--force` flag to regenerate all cells in scope
- [x] Temperature + generation_params persisted in stored results

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
- Fix retry delay per modelli thinking (Qwen3): `_parse_retry_after` non gestisce il formato
  "350ms" — aggiungere il parsing dei millisecondi.
- Indagare perché `gpt-oss-20b` (63%) batte `gpt-oss-120b` (45%) — possibile che il modello
  più grande sia più prolisso e triggeri check negativi (no_zephyr_apis, no_cross_platform_hallucination).
- Document in `docs/INCREMENTAL-EXECUTION.md` the non-determinism note from corpus.py docstring.
