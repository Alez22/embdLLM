"""Static checks for nxp-rt1170-lpuart-001.

L0: pattern matching on generated source text, no compilation needed.
"""

import re

from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate RT1170 LPUART echo code structure."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    for header in ("fsl_lpuart.h", "fsl_iomuxc.h"):
        present = scoped_contains(generated_code, header, scope="code_only")
        details.append(CheckDetail(
            check_name=f"header_{header.replace('.', '_')}",
            passed=present,
            expected=f"{header} included",
            actual="present" if present else "missing",
            check_type="exact_match",
        ))

    # Stated requirement (prompt req. 2): 115200 baud
    has_baud = bool(re.search(r"\b115200[Uu]?\b", stripped))
    details.append(CheckDetail(
        check_name="baud_rate_configured",
        passed=has_baud,
        expected="115200 baud rate configured",
        actual="present" if has_baud else "missing",
        check_type="exact_match",
    ))

    # Stated requirement (prompt req. 3): byte-wise read and write back
    has_read = bool(re.search(r"\bLPUART_Read\w*\s*\(", stripped))
    has_write = bool(re.search(r"\bLPUART_Write\w*\s*\(", stripped))
    echo_ok = has_read and has_write
    details.append(CheckDetail(
        check_name="echo_read_write_api",
        passed=echo_ok,
        expected="LPUART_Read* and LPUART_Write* used for the echo loop",
        actual="present" if echo_ok else (
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
