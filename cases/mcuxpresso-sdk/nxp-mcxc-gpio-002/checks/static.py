"""Static checks for nxp-mcxc-gpio-002.

L0: pattern matching on generated source text, no compilation needed.
"""

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate MCXC144 GPIO interrupt code structure."""
    details: list[CheckDetail] = []

    for header in ("fsl_gpio.h", "fsl_port.h", "fsl_clock.h"):
        present = scoped_contains(generated_code, header, scope="code_only")
        details.append(CheckDetail(
            check_name=f"header_{header.replace('.', '_')}",
            passed=present,
            expected=f"{header} included",
            actual="present" if present else "missing",
            check_type="exact_match",
        ))

    has_irq_config = scoped_contains(
        generated_code, "PORT_SetPinInterruptConfig", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="pin_interrupt_configured",
        passed=has_irq_config,
        expected="PORT_SetPinInterruptConfig called",
        actual="present" if has_irq_config else "missing",
        check_type="exact_match",
    ))

    has_clear_flags = (
        scoped_contains(generated_code, "GPIO_PortClearInterruptFlags", scope="stripped")
        or scoped_contains(generated_code, "GPIO_ClearPinsInterruptFlags", scope="stripped")
    )
    details.append(CheckDetail(
        check_name="interrupt_flag_cleared",
        passed=has_clear_flags,
        expected="interrupt flag cleared in ISR",
        actual="present" if has_clear_flags else "missing",
        check_type="exact_match",
    ))

    # ISR handler must follow PORTC_PORTD_IRQHandler naming convention
    import re
    has_isr = bool(re.search(r"\bPORT\w+_IRQHandler\s*\(", generated_code))
    details.append(CheckDetail(
        check_name="isr_handler_defined",
        passed=has_isr,
        expected="PORT*_IRQHandler function defined",
        actual="present" if has_isr else "missing",
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
