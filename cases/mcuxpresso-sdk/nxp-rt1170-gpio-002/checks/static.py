"""Static checks for nxp-rt1170-gpio-002.

L0: pattern matching on generated source text, no compilation needed.
"""

import re

from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate RT1170 GPIO interrupt code structure."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    # Only the GPIO driver header is strictly required in a single-file answer.
    # The official SDK GPIO source (driver_examples/gpio/input_interrupt/
    # gpio_input_interrupt.c) includes fsl_gpio.h + fsl_port.h but NOT
    # fsl_iomuxc.h — pin muxing lives in a separate pin_mux.c. Requiring
    # fsl_iomuxc.h in the same file contradicts the SDK layout, so it is not
    # a hard requirement here (Class B fix, docs/NXP_CASE_AUDIT.md).
    has_gpio_header = scoped_contains(generated_code, "fsl_gpio.h", scope="code_only")
    details.append(CheckDetail(
        check_name="header_fsl_gpio_h",
        passed=has_gpio_header,
        expected="fsl_gpio.h included",
        actual="present" if has_gpio_header else "missing",
        check_type="exact_match",
    ))

    has_isr = bool(re.search(r"\bGPIO\w+_IRQHandler\s*\(", stripped))
    details.append(CheckDetail(
        check_name="isr_handler_defined",
        passed=has_isr,
        expected="GPIO*_IRQHandler defined (matches vector table entry)",
        actual="present" if has_isr else "missing",
        check_type="exact_match",
    ))

    has_clear = (
        scoped_contains(generated_code, "GPIO_PortClearInterruptFlags", scope="stripped")
        or scoped_contains(generated_code, "GPIO_ClearPinsInterruptFlags", scope="stripped")
    )
    details.append(CheckDetail(
        check_name="interrupt_flag_cleared",
        passed=has_clear,
        expected="GPIO interrupt flag clear API used",
        actual="present" if has_clear else "missing",
        check_type="exact_match",
    ))

    # Stated requirement (prompt req. 3): falling-edge interrupt.
    # Functional correctness check, NOT implicit knowledge — kept in L0.
    has_falling = scoped_contains(
        generated_code, "kGPIO_IntFallingEdge", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="falling_edge_configured",
        passed=has_falling,
        expected="kGPIO_IntFallingEdge interrupt mode",
        actual="present" if has_falling else "missing",
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
