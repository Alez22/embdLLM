"""Static checks for nxp-mcxc-watchdog-001.

L0: pattern matching on generated source text, no compilation needed.
"""

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate MCXC144 COP watchdog code structure."""
    details: list[CheckDetail] = []

    has_header = scoped_contains(generated_code, "fsl_cop.h", scope="code_only")
    details.append(CheckDetail(
        check_name="header_fsl_cop_h",
        passed=has_header,
        expected="fsl_cop.h included",
        actual="present" if has_header else "missing",
        check_type="exact_match",
    ))

    has_init = scoped_contains(generated_code, "COP_Init", scope="stripped")
    details.append(CheckDetail(
        check_name="cop_init_called",
        passed=has_init,
        expected="COP_Init called",
        actual="present" if has_init else "missing",
        check_type="exact_match",
    ))

    has_refresh = scoped_contains(generated_code, "COP_Refresh", scope="stripped")
    details.append(CheckDetail(
        check_name="cop_refresh_called",
        passed=has_refresh,
        expected="COP_Refresh called in main loop",
        actual="present" if has_refresh else "missing",
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
