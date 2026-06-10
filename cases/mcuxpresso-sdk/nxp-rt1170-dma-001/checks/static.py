"""Static checks for nxp-rt1170-dma-001.

L0: pattern matching on generated source text, no compilation needed.
"""

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate RT1170 eDMA memory-to-memory code structure."""
    details: list[CheckDetail] = []

    has_header = scoped_contains(generated_code, "fsl_edma.h", scope="code_only")
    details.append(CheckDetail(
        check_name="header_fsl_edma_h",
        passed=has_header,
        expected="fsl_edma.h included",
        actual="present" if has_header else "missing",
        check_type="exact_match",
    ))

    has_init = scoped_contains(generated_code, "EDMA_Init", scope="stripped")
    details.append(CheckDetail(
        check_name="edma_init_called",
        passed=has_init,
        expected="EDMA_Init called",
        actual="present" if has_init else "missing",
        check_type="exact_match",
    ))

    has_prepare = scoped_contains(
        generated_code, "EDMA_PrepareTransfer", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="edma_transfer_prepared",
        passed=has_prepare,
        expected="EDMA_PrepareTransfer called",
        actual="present" if has_prepare else "missing",
        check_type="exact_match",
    ))

    has_start = scoped_contains(generated_code, "EDMA_StartTransfer", scope="stripped")
    details.append(CheckDetail(
        check_name="edma_transfer_started",
        passed=has_start,
        expected="EDMA_StartTransfer called",
        actual="present" if has_start else "missing",
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
