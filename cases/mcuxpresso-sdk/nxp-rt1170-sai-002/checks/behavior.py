"""Behavioral checks for nxp-rt1170-sai-002.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded audio engineer targeting i.MX RT1170 must know.
"""

import re

from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.check_utils_nxp import has_iomuxc_before_init, has_rt1170_clock_root_config
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit SAI interrupt-streaming knowledge for RT1170."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    # Pad mux before SAI init (implicit)
    mux_ordered = has_iomuxc_before_init(generated_code, "SAI_Init")
    has_mux = bool(re.search(r"\bIOMUXC\w*_SetPinMux\s*\(", stripped))
    mux_ok = has_mux and mux_ordered
    details.append(CheckDetail(
        check_name="iomuxc_before_sai_init",
        passed=mux_ok,
        expected="IOMUXC_SetPinMux called before SAI_Init",
        actual="correct order" if mux_ok else (
            "IOMUXC_SetPinMux missing" if not has_mux else "wrong order"
        ),
        check_type="constraint",
    ))

    # Clock root configured (implicit: no BOARD_BootClockRUN here)
    has_clock_root = has_rt1170_clock_root_config(generated_code)
    details.append(CheckDetail(
        check_name="clock_root_configured",
        passed=has_clock_root,
        expected="CLOCK_SetRootClock called (SAI needs an audio-capable root)",
        actual="present" if has_clock_root else "missing",
        check_type="constraint",
    ))

    # Bit clock rate derived from sample rate (implicit)
    has_bclk = scoped_contains(
        generated_code, "SAI_TxSetBitClockRate", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="bit_clock_rate_set",
        passed=has_bclk,
        expected="SAI_TxSetBitClockRate called for 48 kHz / 16-bit / stereo",
        actual="present" if has_bclk else "missing",
        check_type="constraint",
    ))

    # FIFO request interrupt enabled at the peripheral (implicit)
    has_fifo_irq = scoped_contains(
        generated_code, "SAI_TxEnableInterrupts", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="fifo_interrupt_enabled",
        passed=has_fifo_irq,
        expected="SAI_TxEnableInterrupts enables the FIFO request interrupt",
        actual="present" if has_fifo_irq else "missing",
        check_type="constraint",
    ))

    # NVIC-level enable — without it the interrupt pends but never fires
    has_nvic = bool(re.search(r"\b(?:NVIC_)?EnableIRQ\s*\(", stripped))
    details.append(CheckDetail(
        check_name="nvic_irq_enabled",
        passed=has_nvic,
        expected="EnableIRQ called for the SAI IRQ line",
        actual="present" if has_nvic else "missing",
        check_type="constraint",
    ))

    # Transmitter must actually be enabled (easy to forget after config)
    has_tx_enable = bool(re.search(r"\bSAI_TxEnable\s*\(", stripped))
    details.append(CheckDetail(
        check_name="tx_enabled",
        passed=has_tx_enable,
        expected="SAI_TxEnable called to start the transmitter",
        actual="present" if has_tx_enable else "missing",
        check_type="constraint",
    ))

    # FIFO underrun handling: the error flag stops TX until cleared
    has_err_handling = bool(re.search(r"\bkSAI_FIFOErrorFlag\b", stripped))
    details.append(CheckDetail(
        check_name="fifo_underrun_handled",
        passed=has_err_handling,
        expected="kSAI_FIFOErrorFlag cleared on underrun",
        actual="present" if has_err_handling else "missing",
        check_type="constraint",
    ))

    # ISR state (sample index) must be volatile.
    # Match the qualifier on a data declaration only — a bare \bvolatile\b
    # would also match __asm volatile("wfi") and comments.
    has_volatile = bool(re.search(
        r"\bvolatile\b\s+(?:uint|int|unsigned|bool|char|size_t)\w*", stripped
    ))
    details.append(CheckDetail(
        check_name="volatile_sample_index",
        passed=has_volatile,
        expected="volatile qualifier on ISR streaming state",
        actual="present" if has_volatile else "missing",
        check_type="constraint",
    ))

    return details
