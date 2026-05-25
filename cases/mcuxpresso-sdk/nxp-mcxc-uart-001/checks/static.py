"""Static checks for nxp-mcxc-uart-001.

L0: pattern matching on generated source text, no compilation needed.
"""

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate MCXC144 UART TX blocking code structure."""
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

    has_init = scoped_contains(generated_code, "UART_Init", scope="stripped")
    details.append(CheckDetail(
        check_name="uart_init_called",
        passed=has_init,
        expected="UART_Init called",
        actual="present" if has_init else "missing",
        check_type="exact_match",
    ))

    has_write = scoped_contains(generated_code, "UART_WriteBlocking", scope="stripped")
    details.append(CheckDetail(
        check_name="uart_write_blocking_used",
        passed=has_write,
        expected="UART_WriteBlocking called",
        actual="present" if has_write else "missing",
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
