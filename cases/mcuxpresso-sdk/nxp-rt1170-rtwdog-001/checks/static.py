"""Static checks for nxp-rt1170-rtwdog-001.

L0: pattern matching on generated source text, no compilation needed.
"""

import re

from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate RT1170 RTWDOG code structure."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    has_header = scoped_contains(generated_code, "fsl_rtwdog.h", scope="code_only")
    details.append(CheckDetail(
        check_name="header_fsl_rtwdog_h",
        passed=has_header,
        expected="fsl_rtwdog.h included",
        actual="present" if has_header else "missing",
        check_type="exact_match",
    ))

    has_init = bool(re.search(r"\bRTWDOG_Init\s*\(", stripped))
    details.append(CheckDetail(
        check_name="rtwdog_init_called",
        passed=has_init,
        expected="RTWDOG_Init called",
        actual="present" if has_init else "missing",
        check_type="exact_match",
    ))

    has_refresh = bool(re.search(r"\bRTWDOG_Refresh\s*\(", stripped))
    details.append(CheckDetail(
        check_name="rtwdog_refresh_used",
        passed=has_refresh,
        expected="RTWDOG_Refresh called to feed the watchdog",
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
