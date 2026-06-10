"""Static checks for nxp-rt1170-lpspi-001.

L0: pattern matching on generated source text, no compilation needed.
"""

import re

from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate RT1170 LPSPI JEDEC ID read code structure."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    for header in ("fsl_lpspi.h", "fsl_iomuxc.h"):
        present = scoped_contains(generated_code, header, scope="code_only")
        details.append(CheckDetail(
            check_name=f"header_{header.replace('.', '_')}",
            passed=present,
            expected=f"{header} included",
            actual="present" if present else "missing",
            check_type="exact_match",
        ))

    # Stated requirement (prompt req. 3): JEDEC ID command 0x9F
    has_cmd = bool(re.search(r"0[xX]9[Ff][Uu]?\b", stripped))
    details.append(CheckDetail(
        check_name="jedec_command_used",
        passed=has_cmd,
        expected="JEDEC ID command 0x9F sent",
        actual="present" if has_cmd else "missing",
        check_type="exact_match",
    ))

    has_transfer = bool(re.search(r"\bLPSPI_MasterTransfer\w*\s*\(", stripped))
    details.append(CheckDetail(
        check_name="lpspi_transfer_used",
        passed=has_transfer,
        expected="LPSPI_MasterTransfer* API used",
        actual="present" if has_transfer else "missing",
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
