# NXP Case Audit

**Date:** 2026-06-14
**Trigger:** Strong models (Claude Sonnet 4.6) underperform on the NXP cases.
Suspicion that the cases / checks are not well structured.
**Ground truth:** NXP MCUXpresso SDK `SDK_26_03_00_MIMXRT1170-EVKB`
(extracted under `sdk/`), including the official `driver_examples/`.

## Method

1. Cross-model evidence: aggregated `per_check_metrics.json` across 13 models.
   A check that fails at 0% on *every* model is suspect; one that some models
   pass is legitimate.
2. Ground-truth evidence: compared each suspect check's expected pattern
   against the real SDK driver / example code.
3. Inspected actual model output (Sonnet 4.6, deepseek-v4-flash) to separate
   model defects from check defects.

## Headline finding

**The cases are not well structured. The dominant problem is a systematic
check-design defect, not weak models.** Three classes of checks are broken
because they contradict how the official SDK is written. A strong model that
writes idiomatic, SDK-style code is *penalised*; a model that writes a
monolithic inline `main()` *passes*. This is backwards.

A secondary finding: many token-literal checks are sound — low scores on
those reflect genuine model weakness on implicit embedded practices.

---

## Class A — ordering checks (CONFIRMED BROKEN) — highest impact

**Affected helpers:** `has_clock_gate_before`, `has_pinmux_before_init`
(`src/embedeval/check_utils_nxp.py`), and every `*_before_*` check built on
them.

**Affected checks (17 cases):**
`clock_gate_before_i2c_init`, `pinmux_before_i2c_init`,
`clock_gate_before_pit_init`, `clock_gate_before_uart_init`,
`pinmux_before_uart_init`, `clock_gate_before_gpio_init`,
`pinmux_as_gpio_before_init`, `clock_gate_before_spi_init`,
`pinmux_before_spi_init`, `iomuxc_before_gpio_init`,
`iomuxc_before_lpi2c_init`, `iomuxc_before_lpspi_init`,
`iomuxc_before_lpuart_init`, `iomuxc_before_sai_init`, and the
`sai_init_before_tx_config` / `codec_configured_before_streaming` ordering
variants.

**Defect:** the helpers locate the **first textual occurrence** of the init
function name and require `CLOCK_EnableClock` / `PORT_SetPin*` to appear
textually *before* it. This breaks on any code organised into functions.

**Evidence — model output (Sonnet 4.6, `nxp-mcxc-i2c-001`):**
The code is correct and calls, in `main()` order, pin/clock setup before the
I2C transfer. But it contains:

```c
static status_t I2C_MasterInit(void);   /* forward declaration — FIRST hit */
...
static void BOARD_InitPins(void) {
    CLOCK_EnableClock(kCLOCK_PortC);    /* appears AFTER the forward decl */
    ...
}
```

The check sees `I2C_MasterInit` (the forward declaration) *before*
`CLOCK_EnableClock` → **FAIL at 0%**, despite correct runtime ordering.

**Evidence — SDK ground truth:** the official example structures it exactly
like Sonnet — separate files / functions, ordering enforced by call order in
`main`, not by definition order:

```
sdk/.../driver_examples/lpi2c/polling_b2b/slave/pin_mux.c
  void BOARD_InitPins(void) {
      CLOCK_EnableClock(kCLOCK_Iomuxc);   /* clock gate lives in pin_mux.c */
      ...
  }
```

The clock-enable and the peripheral init live in **separate files** in the
SDK. Our checks therefore contradict the SDK's own idiom.

**Impact:** ~15 of Sonnet's 30 zero-score checks are this class or derived
from it. This is the primary cause of the low score.

**Recommended fix:** rewrite `has_clock_gate_before` /
`has_pinmux_before_init` to evaluate **call order** (ignore forward
declarations and function-definition headers; check the order in which the
calls appear in execution context), or relax to "clock gate present anywhere"
where call-order parsing is impractical. Add regression tests using
function-structured code.

---

## Class B — multi-file header checks (CONFIRMED too strict)

**Affected:** `header_fsl_gpio_h` + `header_fsl_iomuxc_h` (`nxp-rt1170-gpio-002`),
and any check that requires multiple `fsl_*.h` headers in one file.

**Defect:** `nxp-rt1170-gpio-002/checks/static.py` requires BOTH `fsl_gpio.h`
AND `fsl_iomuxc.h` in the single generated file.

**Evidence — SDK ground truth:** the SDK splits these across files. The
official GPIO example's `pin_mux.c` includes **only** `fsl_iomuxc.h`
(not `fsl_gpio.h`); `fsl_gpio.h` is included by the main source. Requiring
both in one file contradicts the SDK layout for a single-file prompt.

**Note — model anomaly on the same case:** Sonnet wrote a *bare-register*
implementation here (only `#include <stdint.h>`, redefining the GPIO register
map by hand). This is the ONLY case out of 24 where Sonnet ignored the SDK
(it used `fsl_*` headers in 23/24). So gpio-002 has *two* issues: a too-strict
check AND an unusually-prompted bare-register response. Worth reviewing the
prompt for gpio-002 specifically.

**Recommended fix:** require only the driver header strictly relevant to a
single-file answer; treat `fsl_iomuxc.h` as optional or check it separately
without failing the whole case.

---

## Class C — COP watchdog enum (CONFIRMED wrong API)

**Affected:** `long_timeout_configured` (`nxp-mcxc-watchdog-001`), the
`reference/main.c`, and `negatives.py` for that case.

**Defect:** the check requires `kCOP_Timeout_2Power1[68]\w*` and the reference
uses `kCOP_Timeout_2Power18LpoClock`. **This symbol does not exist in the SDK
header shipped in this package.**

**Evidence — SDK ground truth (`sdk/.../drivers/cop/fsl_cop.h`):**

```c
typedef enum _cop_timeout_cycles {
    kCOP_2Power5CyclesOr2Power13Cycles  = 1U,
    kCOP_2Power8CyclesOr2Power16Cycles  = 2U,
    kCOP_2Power10CyclesOr2Power18Cycles = 3U,   /* longest */
} cop_timeout_cycles_t;

typedef enum _cop_timeout_mode {
    kCOP_ShortTimeoutMode = 0U,
    kCOP_LongTimeoutMode  = 1U,
} cop_timeout_mode_t;

typedef struct _cop_config {
    cop_timeout_mode_t   timeoutMode;
    cop_clock_source_t   clockSource;     /* kCOP_LpoClock */
    cop_timeout_cycles_t timeoutCycles;
} cop_config_t;
```

The correct "longest timeout" expression in this SDK is
`timeoutCycles = kCOP_2Power10CyclesOr2Power18Cycles` (+ `timeoutMode =
kCOP_LongTimeoutMode`, `clockSource = kCOP_LpoClock`). Our reference and check
use a non-existent `kCOP_Timeout_2Power18LpoClock`.

qwen used `kCOP_LongTimeout` — closer to the real `kCOP_LongTimeoutMode` than
our reference — and still failed because of the wrong suffix.

**Caveat:** older MCXC SDK versions may expose a flat `kCOP_Timeout_2PowerN`
enum. The exact target SDK version for the MCXC144 cases must be confirmed.
But against the SDK present in this repo, the check matches an API that is not
there, so no model can pass it correctly.

**Recommended fix:** decide the target SDK version, then rewrite the reference
and the check to the enum that version actually ships
(`kCOP_2Power10CyclesOr2Power18Cycles` + `kCOP_LongTimeoutMode` for the SDK in
`sdk/`).

---

## Checks that are SOUND (do NOT relax)

Cross-model evidence shows these are legitimate; low scores reflect real model
weakness on implicit embedded practices.

- `transfer_status_checked` (`nxp-rt1170-lpspi-001`): 80% of models pass.
  deepseek fails because it genuinely discards the return value of
  `LPSPI_MasterTransferBlocking` (verified in its output). Sound check.
- `fifo_underrun_handled` (`nxp-rt1170-sai-002`): 50% pass. Sound.
- `flash_return_value_checked`, `init_status_checked`,
  `both_transfer_returns_checked`: token-literal but legitimate — they verify
  the model checks return codes, a real implicit-knowledge requirement.

**Cross-model sanity check:** zero checks fail at 0% on *all* 13 models →
no check is globally broken. The broken classes above fail because strong,
SDK-idiomatic code happens to dodge a fragile textual pattern, not because the
intent is wrong.

---

## Not a problem (ruled out)

- *"Models reimplement the SDK instead of using it."* False as a systematic
  cause: Sonnet used `fsl_*` headers in 23/24 cases. Only `nxp-rt1170-gpio-002`
  (Class B) saw a bare-register answer.
- *"All checks are broken."* False — see sound-checks section.

---

## Priority of fixes (when authorised)

1. **Class A (ordering)** — single shared-helper fix in
   `check_utils_nxp.py`; fixes 17 cases at once. Highest impact, lowest risk.
2. **Class C (COP enum)** — needs a target-SDK-version decision first; then
   fix reference + check for `nxp-mcxc-watchdog-001`.
3. **Class B (headers)** — relax `nxp-rt1170-gpio-002` header check; separately
   review its prompt (bare-register anomaly).

No check changes have been made. This document is the audit only.
