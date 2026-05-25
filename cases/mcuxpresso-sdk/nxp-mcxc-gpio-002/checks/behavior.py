"""Behavioral checks for nxp-mcxc-gpio-002.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded engineer targeting MCXC144 must know.
"""

import re

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import has_clock_gate_before, has_pinmux_before_init
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit MCUXpresso SDK knowledge for GPIO interrupt."""
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

    # NVIC enabled — implicit: prompt never mentions EnableIRQ
    has_nvic = bool(re.search(r"\bEnableIRQ\s*\(", generated_code))
    details.append(CheckDetail(
        check_name="nvic_interrupt_enabled",
        passed=has_nvic,
        expected="EnableIRQ called to enable PORT interrupt in NVIC",
        actual="present" if has_nvic else "missing",
        check_type="constraint",
    ))

    # volatile on ISR-shared variable — implicit: prompt never mentions this
    has_volatile = bool(re.search(r"\bvolatile\b", generated_code))
    details.append(CheckDetail(
        check_name="isr_shared_variable_volatile",
        passed=has_volatile,
        expected="volatile qualifier on ISR-shared variable",
        actual="present" if has_volatile else "missing",
        check_type="constraint",
    ))

    # Falling-edge interrupt configured (not just any interrupt)
    has_falling = scoped_contains(
        generated_code, "kPORT_InterruptFallingEdge", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="falling_edge_interrupt_configured",
        passed=has_falling,
        expected="kPORT_InterruptFallingEdge used",
        actual="present" if has_falling else "missing or wrong edge",
        check_type="constraint",
    ))

    # Interrupt flag cleared INSIDE the ISR (not in main)
    isr_match = re.search(r"\bPORT\w+_IRQHandler\s*\([^)]*\)\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}", generated_code, re.DOTALL)
    if isr_match:
        isr_body = isr_match.group(1)
        flag_cleared_in_isr = (
            "GPIO_PortClearInterruptFlags" in isr_body
            or "GPIO_ClearPinsInterruptFlags" in isr_body
        )
    else:
        flag_cleared_in_isr = False
    details.append(CheckDetail(
        check_name="flag_cleared_inside_isr",
        passed=flag_cleared_in_isr,
        expected="interrupt flag cleared inside IRQHandler body",
        actual="correct" if flag_cleared_in_isr else "missing or cleared outside ISR",
        check_type="constraint",
    ))

    return details
