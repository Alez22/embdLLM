"""Static checks for nxp-mcxc-uart-002.

L0: pattern matching on generated source text, no compilation needed.
"""

import re

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate MCXC144 UART RX interrupt + ring buffer code structure."""
    details: list[CheckDetail] = []

    for header in ("fsl_uart.h", "fsl_port.h", "fsl_clock.h"):
        present = scoped_contains(generated_code, header, scope="code_only")
        details.append(CheckDetail(
            check_name=f"header_{header.replace('.', '_')}",
            passed=present,
            expected=f"{header} included",
            actual="present" if present else "missing",
            check_type="exact_match",
        ))

    has_enable_irq = scoped_contains(
        generated_code, "UART_EnableInterrupts", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="uart_rx_interrupt_enabled",
        passed=has_enable_irq,
        expected="UART_EnableInterrupts called",
        actual="present" if has_enable_irq else "missing",
        check_type="exact_match",
    ))

    has_isr = bool(re.search(r"\bUART0_IRQHandler\s*\(", generated_code))
    details.append(CheckDetail(
        check_name="uart_isr_handler_defined",
        passed=has_isr,
        expected="UART0_IRQHandler defined",
        actual="present" if has_isr else "missing",
        check_type="exact_match",
    ))

    # Ring buffer: must have a fixed-size array for RX accumulation
    has_ring_buf = bool(re.search(r"\buint8_t\b.*\[.*\]", generated_code))
    details.append(CheckDetail(
        check_name="ring_buffer_array_declared",
        passed=has_ring_buf,
        expected="uint8_t array declared for ring buffer",
        actual="present" if has_ring_buf else "missing",
        check_type="exact_match",
    ))

    foreign = no_nxp_hallucination(generated_code)
    details.append(CheckDetail(
        check_name="no_cross_platform_hallucination",
        passed=len(foreign) == 0,
        expected="Only NXP MCUXpresso SDK APIs used",
        actual="clean" if not foreign else f"found: {foreign}",
        check_type="constraint",
    ))

    return details
