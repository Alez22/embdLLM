"""Static checks for nxp-rt1170-sai-002.

L0: pattern matching on generated source text, no compilation needed.
"""

import re

from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate RT1170 interrupt-driven SAI playback code structure."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    for header in ("fsl_sai.h", "fsl_iomuxc.h"):
        present = scoped_contains(generated_code, header, scope="code_only")
        details.append(CheckDetail(
            check_name=f"header_{header.replace('.', '_')}",
            passed=present,
            expected=f"{header} included",
            actual="present" if present else "missing",
            check_type="exact_match",
        ))

    # Stated requirement (prompt req. 4): FIFO fed from the SAI interrupt
    has_isr = bool(re.search(r"\bSAI\w*_IRQHandler\s*\(", stripped))
    details.append(CheckDetail(
        check_name="isr_handler_defined",
        passed=has_isr,
        expected="SAI*_IRQHandler defined (matches vector table entry)",
        actual="present" if has_isr else "missing",
        check_type="exact_match",
    ))

    # Stated requirement (prompt req. 5): main loop does not stream.
    # A blocking SAI write in the source means the architecture was ignored.
    has_blocking = bool(re.search(
        r"\bSAI_(?:WriteBlocking|TransferSendBlocking)\s*\(", stripped
    ))
    details.append(CheckDetail(
        check_name="no_blocking_write",
        passed=not has_blocking,
        expected="No blocking SAI write — FIFO refilled from the ISR",
        actual="clean" if not has_blocking else "blocking SAI write found",
        check_type="constraint",
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
