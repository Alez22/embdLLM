"""Static checks for nxp-rt1170-gpio-001.

L0: pattern matching on generated source text, no compilation needed.
"""

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate RT1170 GPIO output code structure."""
    details: list[CheckDetail] = []

    for header in ("fsl_gpio.h", "fsl_iomuxc.h"):
        present = scoped_contains(generated_code, header, scope="code_only")
        details.append(CheckDetail(
            check_name=f"header_{header.replace('.', '_')}",
            passed=present,
            expected=f"{header} included",
            actual="present" if present else "missing",
            check_type="exact_match",
        ))

    has_init = scoped_contains(generated_code, "GPIO_PinInit", scope="stripped")
    details.append(CheckDetail(
        check_name="gpio_pin_init_called",
        passed=has_init,
        expected="GPIO_PinInit called",
        actual="present" if has_init else "missing",
        check_type="exact_match",
    ))

    has_toggle = (
        scoped_contains(generated_code, "GPIO_PortToggle", scope="stripped")
        or scoped_contains(generated_code, "GPIO_PinWrite", scope="stripped")
        or scoped_contains(generated_code, "GPIO_TogglePinsOutput", scope="stripped")
    )
    details.append(CheckDetail(
        check_name="gpio_toggle_called",
        passed=has_toggle,
        expected="GPIO toggle/write API called in the loop",
        actual="present" if has_toggle else "missing",
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
