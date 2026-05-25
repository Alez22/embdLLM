"""Behavioral checks for nxp-mcxc-isr-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention.
"""

import re

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import has_clock_gate_before
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit knowledge for ISR-to-main atomic data transfer."""
    details: list[CheckDetail] = []

    # Clock gate before GPIO_PinInit
    clock_ok = has_clock_gate_before(generated_code, "GPIO_PinInit")
    has_clock = scoped_contains(generated_code, "CLOCK_EnableClock", scope="stripped")
    details.append(CheckDetail(
        check_name="clock_gate_before_gpio_init",
        passed=has_clock and clock_ok,
        expected="CLOCK_EnableClock called before GPIO_PinInit",
        actual="correct order" if (has_clock and clock_ok) else (
            "CLOCK_EnableClock missing" if not has_clock else "wrong order"
        ),
        check_type="constraint",
    ))

    # NVIC enabled for PIT
    has_nvic = bool(re.search(r"\bEnableIRQ\s*\(", generated_code))
    details.append(CheckDetail(
        check_name="nvic_pit_enabled",
        passed=has_nvic,
        expected="EnableIRQ called for PIT",
        actual="present" if has_nvic else "missing",
        check_type="constraint",
    ))

    # PIT flag cleared in ISR
    isr_match = re.search(
        r"\bPIT_IRQHandler\s*\([^)]*\)\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}",
        generated_code, re.DOTALL
    )
    flag_cleared = bool(isr_match and "PIT_ClearStatusFlags" in isr_match.group(1))
    details.append(CheckDetail(
        check_name="pit_flag_cleared_in_isr",
        passed=flag_cleared,
        expected="PIT_ClearStatusFlags inside PIT_IRQHandler",
        actual="present" if flag_cleared else "missing",
        check_type="constraint",
    ))

    # Ready flag cleared before consuming data (avoids missing next sample)
    # Look for pattern: clear flag, then read value
    flag_before_value = bool(re.search(
        r"(ready|flag|new_data|sample_ready)\s*=\s*(false|0)[^;]*;[^}]*"
        r"(sample|value|data|gpio|pin)",
        generated_code, re.IGNORECASE | re.DOTALL
    ))
    details.append(CheckDetail(
        check_name="ready_flag_cleared_before_consuming",
        passed=flag_before_value,
        expected="ready flag cleared before reading sample value in main",
        actual="correct order" if flag_before_value else "flag cleared after or not found",
        check_type="constraint",
    ))

    # Both shared variables volatile (flag AND value)
    volatile_count = len(re.findall(r"\bvolatile\b", generated_code))
    details.append(CheckDetail(
        check_name="both_shared_vars_volatile",
        passed=volatile_count >= 2,
        expected="at least 2 volatile declarations (flag and value)",
        actual=f"{volatile_count} volatile declaration(s) found",
        check_type="constraint",
    ))

    return details
