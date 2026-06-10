"""Static checks for nxp-rt1170-gpt-001.

L0: pattern matching on generated source text, no compilation needed.
"""

import re

from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate RT1170 GPT tick code structure."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    has_header = scoped_contains(generated_code, "fsl_gpt.h", scope="code_only")
    details.append(CheckDetail(
        check_name="header_fsl_gpt_h",
        passed=has_header,
        expected="fsl_gpt.h included",
        actual="present" if has_header else "missing",
        check_type="exact_match",
    ))

    has_isr = bool(re.search(r"\bGPT\w*_IRQHandler\s*\(", stripped))
    details.append(CheckDetail(
        check_name="isr_handler_defined",
        passed=has_isr,
        expected="GPT*_IRQHandler defined (matches vector table entry)",
        actual="present" if has_isr else "missing",
        check_type="exact_match",
    ))

    has_clear = scoped_contains(
        generated_code, "GPT_ClearStatusFlags", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="interrupt_flag_cleared",
        passed=has_clear,
        expected="GPT_ClearStatusFlags called in the ISR",
        actual="present" if has_clear else "missing",
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
