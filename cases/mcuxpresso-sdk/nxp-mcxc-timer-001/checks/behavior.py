"""Behavioral checks for nxp-mcxc-timer-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention.
"""

import re

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import has_clock_gate_before
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit MCUXpresso SDK knowledge for PIT interrupt."""
    details: list[CheckDetail] = []

    # Clock gate before PIT_Init
    clock_ok = has_clock_gate_before(generated_code, "PIT_Init")
    has_clock = scoped_contains(generated_code, "CLOCK_EnableClock", scope="stripped")
    details.append(CheckDetail(
        check_name="clock_gate_before_pit_init",
        passed=has_clock and clock_ok,
        expected="CLOCK_EnableClock called before PIT_Init",
        actual="correct order" if (has_clock and clock_ok) else (
            "CLOCK_EnableClock missing" if not has_clock else "wrong order"
        ),
        check_type="constraint",
    ))

    # NVIC enabled — implicit
    has_nvic = bool(re.search(r"\bEnableIRQ\s*\(", generated_code))
    details.append(CheckDetail(
        check_name="nvic_pit_interrupt_enabled",
        passed=has_nvic,
        expected="EnableIRQ called to enable PIT in NVIC",
        actual="present" if has_nvic else "missing",
        check_type="constraint",
    ))

    # PIT interrupt enabled before starting timer
    has_enable_int = scoped_contains(
        generated_code, "PIT_EnableInterrupts", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="pit_interrupts_enabled",
        passed=has_enable_int,
        expected="PIT_EnableInterrupts called",
        actual="present" if has_enable_int else "missing",
        check_type="constraint",
    ))

    # volatile on ISR-shared counter — match only variable declarations
    has_volatile = bool(re.search(
        r"\bvolatile\b\s+(?:uint|int|bool|char|float|double)\w*", generated_code
    ))
    details.append(CheckDetail(
        check_name="isr_counter_volatile",
        passed=has_volatile,
        expected="volatile qualifier on ISR-shared counter declaration",
        actual="present" if has_volatile else "missing",
        check_type="constraint",
    ))

    # Interrupt flag cleared inside ISR
    isr_match = re.search(
        r"\bPIT_IRQHandler\s*\([^)]*\)\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}",
        generated_code, re.DOTALL
    )
    flag_cleared = False
    if isr_match:
        flag_cleared = "PIT_ClearStatusFlags" in isr_match.group(1)
    details.append(CheckDetail(
        check_name="pit_flag_cleared_in_isr",
        passed=flag_cleared,
        expected="PIT_ClearStatusFlags called inside PIT_IRQHandler",
        actual="present" if flag_cleared else "missing",
        check_type="constraint",
    ))

    return details
