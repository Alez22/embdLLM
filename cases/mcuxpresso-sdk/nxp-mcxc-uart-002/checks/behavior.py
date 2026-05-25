"""Behavioral checks for nxp-mcxc-uart-002.

L3: verifies implicit domain knowledge — things the prompt does NOT mention.
"""

import re

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import has_clock_gate_before
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit MCUXpresso SDK knowledge for UART RX interrupt."""
    details: list[CheckDetail] = []

    # Clock gate before UART_Init
    clock_ok = has_clock_gate_before(generated_code, "UART_Init")
    has_clock = scoped_contains(generated_code, "CLOCK_EnableClock", scope="stripped")
    details.append(CheckDetail(
        check_name="clock_gate_before_uart_init",
        passed=has_clock and clock_ok,
        expected="CLOCK_EnableClock called before UART_Init",
        actual="correct order" if (has_clock and clock_ok) else (
            "CLOCK_EnableClock missing" if not has_clock else "wrong order"
        ),
        check_type="constraint",
    ))

    # NVIC enabled for UART0 — implicit: prompt never mentions EnableIRQ
    has_nvic = bool(re.search(r"\bEnableIRQ\s*\(", generated_code))
    details.append(CheckDetail(
        check_name="nvic_uart_interrupt_enabled",
        passed=has_nvic,
        expected="EnableIRQ called to enable UART0 in NVIC",
        actual="present" if has_nvic else "missing",
        check_type="constraint",
    ))

    # volatile on ring buffer — ISR and main share it
    has_volatile_buf = bool(re.search(
        r"\bvolatile\b[^;]*\buint8_t\b[^;]*\[", generated_code
    ))
    details.append(CheckDetail(
        check_name="ring_buffer_volatile",
        passed=has_volatile_buf,
        expected="ring buffer array declared volatile (ISR/main shared)",
        actual="present" if has_volatile_buf else "missing",
        check_type="constraint",
    ))

    # volatile on head/tail indices
    has_volatile_idx = bool(re.search(
        r"\bvolatile\b[^;]*(head|tail|write_idx|read_idx|wr_ptr|rd_ptr)", generated_code
    ))
    details.append(CheckDetail(
        check_name="ring_buffer_indices_volatile",
        passed=has_volatile_idx,
        expected="ring buffer head/tail indices declared volatile",
        actual="present" if has_volatile_idx else "missing",
        check_type="constraint",
    ))

    # RX status flag checked inside ISR before reading byte
    isr_match = re.search(
        r"\bUART0_IRQHandler\s*\([^)]*\)\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}",
        generated_code, re.DOTALL
    )
    if isr_match:
        isr_body = isr_match.group(1)
        flag_checked = (
            "kUART_RxDataRegFullFlag" in isr_body
            or "UART_GetStatusFlags" in isr_body
        )
    else:
        flag_checked = False
    details.append(CheckDetail(
        check_name="rx_flag_checked_in_isr",
        passed=flag_checked,
        expected="kUART_RxDataRegFullFlag checked before reading byte in ISR",
        actual="present" if flag_checked else "missing",
        check_type="constraint",
    ))

    return details
