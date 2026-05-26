# embedeval-nxp

Extension of [EmbedEval](https://github.com/Ecro/embedeval) with new firmware cases,
new task types (refactoring, documentation, test generation), and a human-in-the-loop review workflow.

## Project Goal

Benchmark local LLMs for embedded firmware development at Powersoft (audio amplification).
Privacy requirement: production code must not leave local infrastructure.
Strategy: benchmark candidate models now via cloud APIs (Groq/OpenRouter) to decide which
model to deploy locally (Ollama) once dedicated hardware is available.

## Repository Layout

```
embedeval-nxp/
├── CLAUDE.md               # This file
├── README.md
├── TODO.md
├── cases/
│   ├── nxp-bare-metal/     # New: NXP MCUXpresso SDK cases (bare-metal, no RTOS)
│   │   ├── nxp-i2c-001/
│   │   │   ├── metadata.yaml
│   │   │   ├── prompt.md
│   │   │   ├── reference/main.c
│   │   │   └── checks/
│   │   │       ├── static.py
│   │   │       ├── behavior.py
│   │   │       └── negatives.py   # optional, L4 mutation
│   │   └── ...
│   └── (upstream cases from embedeval fork)
├── src/embedeval/
│   ├── check_utils_nxp.py  # New: NXP SDK pattern helpers
│   ├── review.py           # New: human-in-the-loop review workflow
│   └── (upstream modules)
├── docs/
│   └── NXP-CONSIDERATIONS.md
└── results/
```

## Target Platform Context

- **MCU family:** NXP Kinetis / MCX (MCXC144, ARM Cortex-M0+)
- **SDK:** MCUXpresso SDK (SDK2_x_xxx naming convention)
- **Toolchain:** arm-none-eabi-gcc
- **RTOS:** None — bare-metal only
- **Project:** SpeakerMate — speaker device configuration + flash memory management
- **Key domain:** power-loss safe flash (WAL, scratch areas, metadata validation, recovery)

## Case Format

Every case follows the embedeval format exactly. No exceptions.

### metadata.yaml fields
```yaml
id: nxp-i2c-001
category: spi-i2c
difficulty: medium          # easy | medium | hard
title: NXP I2C Peripheral Init
description: One-sentence description
tags: [nxp, bare-metal, i2c, mcuxpresso]
platform: nxp_bare_metal
sdk: mcuxpresso-sdk
estimated_tokens: 400
visibility: public
created_date: 'YYYY-MM-DD'
tier: core
reasoning_types:
  - system_reasoning         # must infer from domain knowledge, not prompt
  - api_recall
  - rule_application
```

### prompt.md rules — CRITICAL
- State **what** to build, never **how** to make it safe.
- Do NOT mention: volatile, memory barriers, cache flush, __DSB/__ISB, critical sections,
  clock enable order, error return checks. The model must know these from domain knowledge.
- End with: `Output ONLY the complete C source file.`
- If the task is refactoring: provide the existing code inline in a fenced block.
- If the task is documentation: provide the undocumented code inline.

### checks/static.py pattern
```python
"""Static checks for <case-id>.

L0: pattern matching on generated source text, no compilation needed.
"""
from embedeval.models import CheckDetail
from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import no_nxp_hallucination


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate NXP bare-metal code structure."""
    details: list[CheckDetail] = []

    # --- required includes ---
    has_sdk_header = scoped_contains(generated_code, 'fsl_i2c.h', scope='code_only')
    details.append(CheckDetail(
        check_name="fsl_i2c_header_included",
        passed=has_sdk_header,
        expected="fsl_i2c.h included",
        actual="present" if has_sdk_header else "missing",
        check_type="exact_match",
    ))

    # --- anti-hallucination: no STM32/Zephyr/Arduino APIs ---
    cross_plat = no_nxp_hallucination(generated_code)
    details.append(CheckDetail(
        check_name="no_cross_platform_hallucination",
        passed=len(cross_plat) == 0,
        expected="Only NXP MCUXpresso SDK APIs used",
        actual="clean" if not cross_plat else f"found: {cross_plat}",
        check_type="constraint",
    ))

    return details
```

### checks/behavior.py — ordering and implicit knowledge
Focus on checks that verify the model applied domain knowledge WITHOUT being told:
- Clock enable before peripheral init
- Pin mux configured before peripheral use
- Error return values checked
- volatile on ISR-shared variables
- Correct address bit-shifting for I2C
- Timeout set in blocking transfers

### checks/review.py (new task type — human review)
Used only for subjective task types (refactoring, Doxygen, explanation, architecture).
```python
"""Human review rubric for <case-id>."""

RUBRIC = [
    {
        "criterion": "correctness",
        "description": "Code is functionally correct and would work on target hardware",
        "weight": 3,
    },
    {
        "criterion": "doxygen_completeness",
        "description": "All public functions have @brief, @param, @return",
        "weight": 2,
    },
]
```

## Coding Conventions

- **Language:** C for embedded code, Python for tooling
- **Comments:** always in English
- **Function headers:** Doxygen format (`@brief`, `@param`, `@retval`)
- **Style:** short functions, single responsibility, early returns over deep nesting
- **Naming:** explicit and descriptive — no abbreviations unless standard (e.g. ISR, DMA, IRQ)
- **Memory:** static allocation only in embedded code — no malloc, no dynamic containers
- **Complexity:** keep cyclomatic complexity low; if a function needs scrolling, split it
- **No over-engineering:** write the simplest thing that passes the checks

## NXP MCUXpresso SDK Patterns

Key patterns the model should know without being prompted:

```c
/* Clock gate: always before peripheral init */
CLOCK_EnableClock(kCLOCK_I2c0);

/* Pin mux: before peripheral init */
PORT_SetPinMux(PORTA, 3U, kPORT_MuxAlt2);

/* I2C init sequence */
I2C_MasterGetDefaultConfig(&masterConfig);
masterConfig.baudRate_Bps = 100000U;
I2C_MasterInit(I2C0, &masterConfig, I2C0_CLK_FREQ);

/* ISR-shared flag: must be volatile */
static volatile bool g_transfer_complete = false;

/* DMA: cache flush before transfer (Cortex-M7 only — not needed on M0+) */
```

## Commands

```bash
# Install
uv sync

# Run NXP cases only (L0+L3, no Docker)
uv run embedeval run --model mock --cases cases/nxp-bare-metal/

# Run with Groq (open-weight models via API)
GROQ_API_KEY=... uv run embedeval run \
  --model groq/llama-3.3-70b-versatile \
  --cases cases/nxp-bare-metal/ \
  --attempts 3

# Run human review workflow
uv run embedeval review --cases cases/nxp-bare-metal/ --reviewer-model anthropic/claude-opus-4-20250514

# Validate all reference solutions pass checks
uv run embedeval validate --cases cases/nxp-bare-metal/

# Lint and test
uv run ruff check src/ tests/
uv run pytest tests/
```

## What NOT to Do

- Do not add `malloc` or dynamic allocation to embedded reference solutions.
- Do not mention safety requirements in the prompt — the whole point is implicit knowledge.
- Do not add RTOS primitives (FreeRTOS, Zephyr k_sem, etc.) to NXP bare-metal cases.
- Do not create a refactoring case without providing the original code in the prompt.
- Do not implement additional features or optimizations without explicit request.
- Do not skip the anti-hallucination check in static.py.

## Caching architecture — non-obvious invariants

Two-tier cache in `src/embedeval/corpus.py`. Get these wrong and the
benchmark numbers silently become invalid.

### Generation cache
- Key: `(prompt_hash, model, temperature, generation_params, attempt)`.
- Layout: `results/corpus/generations/<model_slug>/<case_id>/<attempt>.json`.
- Per-model directory: a model never reads another model's cells.

### Grading cache (`GradeCell`)
- Key: `(generated_code_hash, checks_hash)` — **NOT** model or attempt.
- **Stores ONLY pure-function-of-(code,checks) fields**: `layers`,
  `passed`, `failed_at_layer`, `total_score`. Nothing else.
- Per-call metadata (model, attempt, token_usage, cost_usd,
  duration_seconds, used_thinking, temperature, generation_params) must
  come from the *current* call site via `_build_result_from_grade`.
- Rationale: two different models that happen to emit identical code
  (common with temperature=0) share the cache key — leaking the first
  model's metadata into the second would falsify per-model results.

### Feedback rounds do NOT use the grade cache
- The cache key cannot distinguish a base generation from a feedback-round
  output, so caching them together would poison cross-context lookups.
- Feedback rounds always call `evaluate()` afresh. Accept the cost.

### When adding fields to `EvalResult`
- If the new field depends only on `(generated_code, checks)`, add it to
  `GradeCell` too.
- If it depends on the call site (model, params, timing), pass it via
  `_build_result_from_grade` arguments. Do NOT add it to `GradeCell`.

### `--force` semantics
- Bypasses both caches. Generates NEW samples, does NOT reproduce old
  ones — most providers expose no seed. A specific past sample cannot be
  recovered after `--force`.

## Retry policy (LLM client)

- `_call_litellm` uses exponential backoff with full jitter:
  `min(base * 2^(attempt-1), cap) + uniform(0, 1)`.
  Defaults: `base=5s` (`rate_limit_delay`), `cap=120s` (`max_retry_delay`),
  `max_retries=6`.
- On `RateLimitError`: `delay = max(provider_delay, backoff)` — the
  provider-supplied wait time is always respected. Parsed from HTTP
  `Retry-After` header first, then from the message body
  ("try again in X.XXs" / "350ms").
- Other transient errors (`ServiceUnavailableError`, `Timeout`,
  `ConnectionError`) use pure backoff.
- Anything else propagates as `RuntimeError(f"Non-retryable error...")` —
  caller turns it into FAIL@L0 via `_make_error_result`.
