"""Static checks for nxp-rt1170-lpi2c-001.

L0: pattern matching on generated source text, no compilation needed.
"""

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate RT1170 LPI2C master code structure."""
    details: list[CheckDetail] = []

    for header in ("fsl_lpi2c.h", "fsl_iomuxc.h", "fsl_clock.h"):
        present = scoped_contains(generated_code, header, scope="code_only")
        details.append(CheckDetail(
            check_name=f"header_{header.replace('.', '_')}",
            passed=present,
            expected=f"{header} included",
            actual="present" if present else "missing",
            check_type="exact_match",
        ))

    has_init = scoped_contains(generated_code, "LPI2C_MasterInit", scope="stripped")
    details.append(CheckDetail(
        check_name="lpi2c_master_init_called",
        passed=has_init,
        expected="LPI2C_MasterInit called",
        actual="present" if has_init else "missing",
        check_type="exact_match",
    ))

    has_transfer = scoped_contains(
        generated_code, "LPI2C_MasterTransferBlocking", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="lpi2c_blocking_transfer_used",
        passed=has_transfer,
        expected="LPI2C_MasterTransferBlocking called",
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
