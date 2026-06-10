# TODO

Tasks are ordered by **current priority** (updated 2026-05-26).
Mark done with `[x]`. Add notes inline after `—`.

## Priority order (next 2-4 weeks)

1. **Phase 4** — Dashboard: improvements (bug --attempts done)
2. **Phase 6** — Cloud model runs: complete missing models + docs
3. **Phase 3** — New task types (refactoring, doxygen, test gen, arch)
4. **Phase 5** — Human Review workflow
5. **Phase 1** — Remaining infrastructure (SDK_LAYOUT, Docker)
6. **Phase 7** — Knowledge Currency Probing
7. **Phase 8** — Language-variant evaluation
8. **Backlog** — Hardware-in-the-loop, trap prompts, upstream PR

## Negatives coverage debt (upstream Zephyr + Embedded Linux cases)

30 upstream cases have `negatives.py` written before the ≥80% coverage gate existed.
They are currently exempted via `plans/coverage-grandfather.txt`. Until fixed,
`--strict-coverage` cannot be trusted as a meaningful gate on the full case suite.

**How to fix:** for each case in the grandfather list, bring coverage to ≥80% then
remove it from the list. When the list is empty, the file and the grandfather logic
in `verify_negatives_oracle.py` can be deleted.

**Work per case:**
1. Run `uv run python scripts/verify_negatives_oracle.py --case <case_id> --coverage`
   to see which checks are uncovered (`uncovered=` field in output).
2. For each uncovered check, add a new entry to `NEGATIVES` in `checks/negatives.py`:
   a mutation of `reference/main.c` that removes or corrupts exactly that check's
   target pattern, plus `"should_fail": ["<check_name>"]`.
3. Re-run the oracle to confirm coverage ≥80% and all mutations PASS (i.e. the
   mutated code is correctly rejected by the check).
4. Remove the case_id from `plans/coverage-grandfather.txt`.

**Cases to fix (30 total, all upstream):**

| case_id | sdk bucket | current coverage |
|---------|------------|-----------------|
| dma-001 | zephyr | 23% (3/13 checks) |
| dma-008 | zephyr | unknown — run oracle |
| dma-009 | zephyr | unknown — run oracle |
| ble-008 | zephyr | unknown — run oracle |
| boot-001 | zephyr | unknown — run oracle |
| device-tree-001 | zephyr | unknown — run oracle |
| esp-gpio-001 | esp-idf | unknown — run oracle |
| gpio-basic-001 | zephyr | unknown — run oracle |
| gpio-basic-006 | zephyr | unknown — run oracle |
| isr-concurrency-003 | zephyr | unknown — run oracle |
| isr-concurrency-008 | zephyr | unknown — run oracle |
| kconfig-001 | zephyr | unknown — run oracle |
| linux-driver-001 | embedded-linux | unknown — run oracle |
| linux-driver-002 | embedded-linux | unknown — run oracle |
| memory-opt-001 | zephyr | unknown — run oracle |
| memory-opt-012 | zephyr | unknown — run oracle |
| networking-001 | zephyr | unknown — run oracle |
| ota-001 | zephyr | unknown — run oracle |
| power-mgmt-001 | zephyr | unknown — run oracle |
| pwm-001 | zephyr | unknown — run oracle |
| security-001 | zephyr | unknown — run oracle |
| sensor-driver-001 | zephyr | unknown — run oracle |
| storage-001 | zephyr | unknown — run oracle |
| threading-001 | zephyr | unknown — run oracle |
| timer-001 | zephyr | unknown — run oracle |
| timer-007 | zephyr | unknown — run oracle |
| uart-001 | zephyr | unknown — run oracle |
| watchdog-005 | zephyr | unknown — run oracle |
| yocto-001 | embedded-linux | unknown — run oracle |
| yocto-008 | embedded-linux | unknown — run oracle |

**First step:** run the oracle su tutti e 30 per avere i numeri reali:

```bash
uv run python scripts/verify_negatives_oracle.py --coverage \
  $(grep -v "^#\|^$" plans/coverage-grandfather.txt | \
    while read id; do find cases/ -type d -name "$id" -printf "--cases %p "; done)
```

**Suggested order:** tackle by SDK bucket — zephyr first (26 cases), then
embedded-linux (2), then esp-idf (1 + 1 already done by zephyr pass).
Each bucket shares similar check patterns so mutations can be written faster.

---

## Code health (from review 2026-05-26)

Issues from the 2026-05-26 review — some resolved, others tracked as debt.

### Resolved
- [x] **Bug #1**: feedback loop crashed with `failed_at_layer = None` or `> 1`
  after the first round. Fixed in commit `82932cb` (while + bounds check + test).
- [x] **Bug #2**: grade cache stored the entire `EvalResult` keyed only on
  `(code_hash, checks_hash)` → cross-model metadata leak. Fixed in commit
  `6e61fd7`: new `GradeCell` with pure-function fields only; runner rebuilds
  `EvalResult` from current call metadata. Caching removed from feedback rounds
  (key is not distinguishing).
- [x] **Smoke regression test** end-to-end: commit `e67d1c1`. 6 caching
  scenarios covered with mock model.

### Open — medium priority

- [ ] **`_extract_code` on unclosed fences** (`src/embedeval/llm_client.py`).
  If the model truncates mid-output (token limit), no closing fence →
  `_extract_code` returns the entire text including reasoning. Proposed fix:
  if an opening ` ```(c|cpp)?` is found but no complete match, take everything
  from the opening to the end as a fallback.
- [ ] **`_call_litellm` swallows non-retryable errors**: converts any
  `Exception` to `RuntimeError`, losing the specific class
  (`BadRequestError`, `AuthenticationError`). The caller `_make_error_result`
  already uses `type(exc).__name__`, so propagating typed exceptions gives more
  information. Keep `except (RateLimitError, ...)` as-is; remove the catch-all
  `except Exception`.
- [ ] **MOCK_C_CODE uses Zephyr**: `llm_client.py:24` has `#include <zephyr/kernel.h>`
  which fails `no_cross_platform_hallucination` on NXP cases. Likely an upstream
  leftover. Replace with a bare-metal NXP-style main.c, or make it SDK-configurable.
- [ ] **`Platform` enum vs `metadata.yaml` alignment**: CLAUDE.md shows
  `platform: nxp_bare_metal` and `EvalPlatform.NXP_BARE_METAL = "nxp_bare_metal"`
  exists. Verify whether the `platform` field in `CaseMetadata` is still active or
  deprecated in favour of `sdk`. If deprecated, remove from metadata.

### Open — low priority (structural debt)

- [ ] **Oversized files with no single responsibility**: `cli.py` 1439 lines,
  `check_utils.py` 1430, `evaluator.py` 1180, `reporter.py` 1148,
  `safety_guide.py` 976, `dashboard.py` 943. When one becomes painful to modify,
  extract sub-modules. Not immediately critical but cost grows over time.
- [ ] **`_RETRY_AFTER_RE` only captures "try again in"**: OpenRouter uses different
  formats ("retry after Xs"). When Phase 6 activates OpenRouter, extend the pattern
  or make it provider-aware.
- [ ] **No global retry budget**: `max_retries=6` is per-call. On a run of
  12 cases × 5 attempts × 3 feedback rounds under heavy rate limiting, the benchmark
  can silently stretch to hours. Add `--run-deadline=2h` or a global wait accumulator.
- [ ] **Brittle pre-existing tests**: `test_three_runs_cover_same_case_set`
  (test_context_quality_mode_e2e.py) finds 4 UART cases instead of 2,
  `test_sdk_buckets` fails on 2 cases. Not caused by recent changes but indicate
  fixtures drifting as new cases are added.
- [ ] **`feedback_rounds` vs `attempt` semantics**: final `token_usage` reflects
  only the last LLM call, not the sum across all rounds. Cost comparisons between
  models with feedback enabled are underestimated. Decide whether to sum or document
  the convention.

---

## Phase 4 — Results Dashboard

Local web dashboard for exploring benchmark results: generated vs reference diff,
check pass/fail, visual leaderboard, run history.

**Dependencies:** `fastapi`, `uvicorn` (added to `pyproject.toml`).
**Start:** `uv run embedeval dashboard` → opens `http://localhost:7860`.
**Data source:** reads existing JSONs in `results/` and case `reference/main.c` +
`metadata.yaml` files directly — no additional DB.

- [x] **Add `fastapi` and `uvicorn`** to `pyproject.toml`.
- [x] **`src/embedeval/dashboard.py`** — FastAPI server:
  - `GET /` → leaderboard: models × cases table, colored pass/fail/not-run cells
  - `GET /case/<case_id>/<model>` → detail: check list + side-by-side diff generated vs reference
  - `GET /history` → run list sorted by date with status and tokens out; click opens detail
  - `GET /history/<run_id>` → per-run detail: checks pass/fail + side-by-side diff per case
  - `GET /cases` → case list with sdk, difficulty, category, tier, tags
  - `GET /cases/<id>` → editable prompt and reference (POST to save with confirmation)
  - `GET /cases/<id>/checks` → static.py and behavior.py read-only with syntax highlight (Python ok, C known issue)
- [x] **Add `dashboard` subcommand to `src/embedeval/cli.py`**.
- [x] **Verify that with `--attempts N` all attempts are saved** as separate files
  in `results/runs/*/details/` — fix: filename now includes `_attempt{N}`
  (`reporter.py:698`), was `{case_id}.json` → each attempt overwrote the previous.

### Dashboard — Future improvements

Known dashboard improvements not yet resolved, in order of usefulness:

- [ ] **Verbosity check in L0** — add a `CheckDetail` with `check_name="verbosity_ratio"`
  computed in `_run_static_checks()` (evaluator.py) where `case_dir` is already available.
  Formula: `gen_lines / ref_lines` (non-empty, non-comment lines). PASS if ≤ 2.0x.
  Environment-skip if no reference exists. No impact on the 231 existing check files.
  Flags models that "spray" output hoping the correct answer is included.

- [ ] **C syntax highlight** — `highlight.js` works for Python but not C.
  The CDN `highlight.min.js` bundle appears to exclude the C language pack.
  Options: use Pygments server-side (generates coloured HTML without JS),
  or find the correct CDN URL that includes all language packs.
- [ ] **Attempt selector** on the `/history/<run_id>` detail page — currently always shows
  the most recent attempt. With `--attempts N > 1` it would be useful to choose which
  attempt to display.
- [x] **Leaderboard filters** — filter by SDK and difficulty via query params (`?sdk=zephyr&difficulty=medium`).
- [x] **Average response time per model** — show average time per case (avg `duration_seconds`
  across results) in the leaderboard. A slow but accurate model has a real operational cost.
  Show as an extra column in the dashboard leaderboard and in the markdown leaderboard.
  The `duration_seconds` field is already present in `EvalResult`.
  Fix: `llm_response.duration_seconds` now propagated to `EvalResult` in all paths of `runner.py`.
- [ ] **Check editor** — `checks/static.py` and `checks/behavior.py` are currently read-only.
  Add the ability to edit them from the dashboard (POST `/cases/<id>/checks/<file>`).
- [ ] **Direct link** from the leaderboard to the case page (`/cases/<id>`) in addition
  to the run detail.

---

## Phase 6 — Cloud Model Integration

- [x] **Verify Groq provider** works end-to-end with embedeval LiteLLM client:
  - `groq/llama-3.3-70b-versatile` ✓
  - `groq/qwen/qwen3-32b` ✓ (with `--no-think` due to TPM limit)
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
  (bugs #1, #2, attempt-file overwrite). Historical expected numbers for
  reference before the wipe:
  - `groq/llama-3.3-70b-versatile`: 0/12 pass, 61% avg — omits fsl_clock.h/fsl_port.h
  - `groq/openai/gpt-oss-120b`: 3/12 pass, 84% avg — best overall
  - `groq/openai/gpt-oss-20b`: 1/12 pass, 51% avg — inconsistent on ISR cases
- [ ] **Re-publish leaderboard** in `results/LEADERBOARD.md` after the first
  clean run.

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

### Check quality improvements

- **Deep embedded checks** — i casi esistenti raggiungono pass rate >90% con i
  modelli migliori perché i check coprono solo conoscenza embedded di base. Per
  alzare la difficoltà: aggiungere check avanzati ai casi `hard` già esistenti
  (007-010 per categoria) senza creare nuovi casi. Target: HW memory model,
  vincoli ISR context, real-time timing, resource alignment. Nessun nuovo caso
  da creare — solo nuovi check in `behavior.py` di quelli esistenti.

- **Subtle negatives** — i `negatives.py` attuali usano mutation ovvie (rimozione
  completa di un pattern). Aggiungere mutation "sottili" che aggirano il check
  mantenendo il bug semantico (es. `key = k_spin_lock(...)` → `k_spin_lock(...); key = {0}`).
  Obiettivo: ~50% delle mutation sottili non dovrebbe essere catturato dai check
  attuali — queste diventano la roadmap per rafforzare i check. Dettaglio in
  `plans/PLAN-subtle-negatives.md` (15 mutation candidate identificate).

- **Remaining check blind spots** — 6 check specifici già identificati con la fix
  esatta da applicare. Dettaglio in `plans/PLAN-remaining-blindspots.md`:
  `dma-008/error_detected_but_no_return`, `isr-003/spinlock_key_hardcoded_zero`,
  `linux-001/partial_cleanup_only` e altri 3. Lavoro puntuale, bassa complessità.

### Scope discipline for anti-hallucination loops

- **`scoped_contains_any` helper** — i ~151 check anti-hallucination usano il
  pattern `any(api in generated_code for api in api_list)` (es. lista di API
  Zephyr/Arduino/STM32 proibite). Questi loop NON applicano scope discipline:
  un'API proibita scritta dentro un commento (es. `// non usare k_thread_create`)
  o una stringa di log darebbe un falso positivo di "contaminazione cross-platform".
  La migrazione `scoped_contains` (REQ-03) ha già coperto i substring check a
  singola stringa costante, ma i loop su lista sono rimasti scoperti perché
  iterano una lista.
  **Fix proposta:** aggiungere `scoped_contains_any(code, needles, *, scope=...)`
  in `check_utils.py` che applica lo stesso strip di commenti/stringhe a ogni
  elemento, e sostituire i loop `any(x in generated_code for x in LIST)`.
  Nota: è un miglioramento di design nuovo, non il completamento di REQ-03
  (quella migrazione è completa — `apply_scope_migration.py` rimosso). Da
  valutare l'impatto sui verdetti: stringere lo scope può far cambiare il
  risultato di check che prima matchavano dentro commenti.

### New CLI features

- **`embedeval run --context-pack`** + **`embedeval context-compare`** — misurare
  quanto il contesto iniettato nel prompt (bare / team CLAUDE.md / expert pack)
  impatta il pass rate. Output: *Context Lift* (effetto del contesto team) e
  *Context Gap* (distanza dall'expert). Per ogni caso: classificare l'effetto come
  helpful / harmful / no-effect. Utile per validare oggettivamente se un CLAUDE.md
  migliora i risultati. Dettaglio in `plans/PLAN-context-quality-mode.md` e
  `plans/PLAN-per-case-effect-classification.md`.

- **`embedeval context-diagnose`** — nuovo comando che legge i risultati di un run
  e mappa ogni check fallito alla sua categoria in `FAILURE-FACTORS.md`, segnalando
  le categorie dove il team è sotto l'expert di ≥10pp. Output: lista di factor ID
  ad alta priorità da aggiungere al CLAUDE.md. Dettaglio in
  `plans/PLAN-context-diagnose.md`.

- **Bug-fix scenario** (`task_type: bugfix`) — nuovo scenario di valutazione: il
  modello riceve codice con un bug deliberato (preso da `negatives.py`) e deve
  identificarlo e correggerlo. Il codice corretto viene poi valutato con i check
  esistenti. Riusa tutto il lavoro L4 già fatto senza nuova infrastruttura. Dettaglio
  in `plans/PLAN-bugfix-scenario.md`.

### Embedded Linux case expansion

- **Linux OTA — SWUpdate + RAUC** (6-8 casi): testare la capacità del modello
  di scrivere manifest e configurazioni per i due sistemi OTA più diffusi
  nell'embedded Linux industriale. SWUpdate: `sw-description` con layout
  dual-bank, signed update, embedded scripts. RAUC: `manifest.raucm`,
  slot config, atomic switchover. Zero cambiamenti infrastrutturali — riusa
  i pattern dei casi Yocto/systemd già esistenti. Alta priorità perché copre
  un dominio produttivo reale non ancora rappresentato.

- **Linux networking kernel — netfilter / socket / netlink** (5-7 casi):
  hook netfilter (`NF_INET_PRE_ROUTING`), gestione `sk_buff`, socket netlink,
  packet filter BPF classico (`AF_PACKET` + `sock_filter`). Aggiunge il
  contesto di concorrenza softirq — distinto da IRQ/process/ISR — che i casi
  `linux-driver` esistenti non coprono. Buon complemento alla suite
  embedded-linux dopo OTA.

### Future directions — to investigate

- **Agentic capability evaluation**: investigate how to benchmark the agentic capabilities of
  models (multi-step tool use, self-correction, iterative debugging without human prompts).
  Understand what existing frameworks exist (SWE-bench, AgentBench, custom harness), whether
  embedeval can be extended to support agentic runs (e.g. model drives a compile-fix loop),
  and how to define a fair metric that accounts for token cost of agent iterations.

- **Bug-detection task type**: add cases where the prompt provides already-written embedded C code
  containing a deliberate bug (e.g. missing clock enable, wrong I2C address shift, unprotected
  ISR-shared variable, off-by-one in flash address arithmetic) and asks the model to identify it.
  Grading: static check verifies the model's output names the correct bug location/cause; a
  negatives check ensures it does not hallucinate additional non-existent bugs.
  Fits as a new `task_type: bug_detection` in `metadata.yaml`, parallel to refactoring/doxygen.
  Candidate first cases: missing `volatile` on ISR flag, wrong address bit-shift for I2C slave,
  clock gate enabled after peripheral init (ordering bug), buffer overflow in ring-buffer wrap.

- Hardware-in-the-loop (L5): flash code to real MCXC144 board, verify via serial output.
- Anti-hallucination trap prompts: ask for a peripheral that doesn't exist on MCXC144,
  verify the model refuses or flags the inconsistency instead of fabricating register addresses.
- Sensitivity analysis: run same case with 5 prompt variants, measure score variance.
- Contribute NXP cases upstream to embedeval via PR.
- NXP include pattern: llama-3.3-70b and gpt-oss-20b consistently use `board.h` instead
  of explicit `fsl_clock.h` / `fsl_port.h` — fails L0 on every case. Consider whether
  to relax the check (accept transitive includes) or keep it strict (explicit headers required).
- Fix retry delay for thinking models (Qwen3): `_parse_retry_after` does not handle the
  "350ms" format — add millisecond parsing.
- Investigate why `gpt-oss-20b` (63%) outscores `gpt-oss-120b` (45%) — the larger model
  may be more verbose and trigger negative checks (no_zephyr_apis, no_cross_platform_hallucination).
- Document in `docs/INCREMENTAL-EXECUTION.md` the non-determinism note from corpus.py docstring.
- **Quantized local model variants**: investigate how to benchmark the same base model across
  multiple quantization levels (e.g. Q4_K_M, Q5_K_M, Q8_0, F16) running locally via Ollama.
  Key questions: how to represent each variant as a distinct model slug in the leaderboard
  (e.g. `ollama/qwen2.5-coder:7b-q4_k_m` vs `ollama/qwen2.5-coder:7b-q8_0`); whether the
  cache key already handles this correctly (it keys on model string, so slug differences are
  enough); how to add a "quant" axis to the leaderboard/dashboard to compare accuracy vs
  inference speed trade-off across quantization levels for the same underlying model.

- **Long-context evaluation**: benchmark how models behave when the prompt includes a large
  surrounding codebase (e.g. entire driver module or SDK header dump) alongside the actual task.
  Goal: separate short-context capability from the ability to extract the relevant signal from
  noise. Key approaches to investigate:
  - *Needle-in-a-haystack*: embed a single critical detail (e.g. a custom register address or
    a non-standard API function signature) deep inside a large irrelevant C file; verify the
    model actually uses it rather than falling back to generic SDK patterns.
  - *Distraction injection*: pad the prompt with plausible-but-wrong code snippets from a
    different peripheral or platform; check that the model ignores them and produces correct output.
  - *Context window scaling*: run the same case at increasing context sizes (4k, 16k, 32k, 128k)
    to find where each model degrades — useful for deciding which models can handle
    real SpeakerMate driver files as context.
  Infrastructure notes: needs a `context_size_tokens` field in `metadata.yaml`; the generation
  cache key must include context payload hash to avoid collisions with the short-context variant.
