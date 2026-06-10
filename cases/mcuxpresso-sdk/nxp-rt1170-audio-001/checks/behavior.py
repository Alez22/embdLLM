"""Behavioral checks for nxp-rt1170-audio-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded audio engineer targeting i.MX RT1170 must know. The core of
this case: when ADC and DAC share the clock lines, the SAI receiver must run
in sync mode so it borrows the transmitter's BCLK and frame sync.
"""

import re

from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.check_utils_nxp import has_iomuxc_before_init
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit full-duplex SAI knowledge for RT1170."""
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
    has_clock_root = scoped_contains(
        generated_code, "CLOCK_SetRootClock", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="clock_root_configured",
        passed=has_clock_root,
        expected="CLOCK_SetRootClock called (SAI needs an audio-capable root)",
        actual="present" if has_clock_root else "missing",
        check_type="constraint",
    ))

    # Bit clock rate derived from sample rate on the TX side (implicit)
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

    # RX must run in sync mode: shared clock wires mean the receiver borrows
    # the transmitter's BCLK/SYNC — two async dividers drift apart (implicit)
    has_sync_mode = scoped_contains(
        generated_code, "kSAI_ModeSync", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="rx_sync_mode",
        passed=has_sync_mode,
        expected="kSAI_ModeSync on the receiver (borrows TX clocks)",
        actual="present" if has_sync_mode else "missing",
        check_type="constraint",
    ))

    # Both directions must actually be enabled (easy to forget one)
    tx_on = bool(re.search(r"\bSAI_TxEnable\s*\(", stripped))
    rx_on = bool(re.search(r"\bSAI_RxEnable\s*\(", stripped))
    both_on = tx_on and rx_on
    details.append(CheckDetail(
        check_name="tx_and_rx_enabled",
        passed=both_on,
        expected="SAI_TxEnable and SAI_RxEnable both called",
        actual="both enabled" if both_on else (
            "TX not enabled" if not tx_on else "RX not enabled"
        ),
        check_type="constraint",
    ))

    return details
