"""Static checks for nxp-rt1170-audio-001.

L0: pattern matching on generated source text, no compilation needed.
"""

import re

from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate RT1170 full-duplex audio pass-through code structure."""
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

    # Stated requirement (prompt req. 3): read then write back
    has_read = bool(re.search(
        r"\bSAI_(?:ReadBlocking|TransferReceiveBlocking|ReadNonBlocking)\s*\(",
        stripped,
    ))
    has_write = bool(re.search(
        r"\bSAI_(?:WriteBlocking|TransferSendBlocking|WriteNonBlocking)\s*\(",
        stripped,
    ))
    duplex_ok = has_read and has_write
    details.append(CheckDetail(
        check_name="read_and_write_api_used",
        passed=duplex_ok,
        expected="SAI read and write APIs both used for the pass-through",
        actual="present" if duplex_ok else (
            "read missing" if not has_read else "write missing"
        ),
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
