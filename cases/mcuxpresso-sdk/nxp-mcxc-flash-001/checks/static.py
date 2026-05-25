"""Static checks for nxp-mcxc-flash-001.

L0: pattern matching on generated source text, no compilation needed.
"""

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate MCXC144 flash erase/write/verify code structure."""
    details: list[CheckDetail] = []

    has_header = scoped_contains(generated_code, "fsl_flash.h", scope="code_only")
    details.append(CheckDetail(
        check_name="header_fsl_flash_h",
        passed=has_header,
        expected="fsl_flash.h included",
        actual="present" if has_header else "missing",
        check_type="exact_match",
    ))

    has_init = scoped_contains(generated_code, "FLASH_Init", scope="stripped")
    details.append(CheckDetail(
        check_name="flash_init_called",
        passed=has_init,
        expected="FLASH_Init called",
        actual="present" if has_init else "missing",
        check_type="exact_match",
    ))

    has_erase = scoped_contains(generated_code, "FLASH_EraseSector", scope="stripped")
    details.append(CheckDetail(
        check_name="flash_erase_sector_called",
        passed=has_erase,
        expected="FLASH_EraseSector called before write",
        actual="present" if has_erase else "missing",
        check_type="exact_match",
    ))

    has_program = scoped_contains(generated_code, "FLASH_Program", scope="stripped")
    details.append(CheckDetail(
        check_name="flash_program_called",
        passed=has_program,
        expected="FLASH_Program called",
        actual="present" if has_program else "missing",
        check_type="exact_match",
    ))

    has_verify = scoped_contains(generated_code, "FLASH_VerifyProgram", scope="stripped")
    details.append(CheckDetail(
        check_name="flash_verify_program_called",
        passed=has_verify,
        expected="FLASH_VerifyProgram called after write",
        actual="present" if has_verify else "missing",
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
