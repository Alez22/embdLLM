"""Static checks for nxp-mcxc-isr-001.

L0: pattern matching on generated source text, no compilation needed.
"""

import re

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate MCXC144 ISR-to-main data transfer code structure."""
    details: list[CheckDetail] = []

    for header in ("fsl_pit.h", "fsl_gpio.h", "fsl_clock.h"):
        present = scoped_contains(generated_code, header, scope="code_only")
        details.append(CheckDetail(
            check_name=f"header_{header.replace('.', '_')}",
            passed=present,
            expected=f"{header} included",
            actual="present" if present else "missing",
            check_type="exact_match",
        ))

    has_isr = bool(re.search(r"\bPIT_IRQHandler\s*\(", generated_code))
    details.append(CheckDetail(
        check_name="pit_isr_defined",
        passed=has_isr,
        expected="PIT_IRQHandler defined",
        actual="present" if has_isr else "missing",
        check_type="exact_match",
    ))

    # Shared flag or variable between ISR and main
    has_volatile = bool(re.search(r"\bvolatile\b", generated_code))
    details.append(CheckDetail(
        check_name="volatile_shared_data",
        passed=has_volatile,
        expected="volatile qualifier on ISR-shared variable(s)",
        actual="present" if has_volatile else "missing",
        check_type="exact_match",
    ))

    has_gpio_read = scoped_contains(generated_code, "GPIO_PinRead", scope="stripped")
    details.append(CheckDetail(
        check_name="gpio_pin_read_in_code",
        passed=has_gpio_read,
        expected="GPIO_PinRead called to sample input",
        actual="present" if has_gpio_read else "missing",
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
