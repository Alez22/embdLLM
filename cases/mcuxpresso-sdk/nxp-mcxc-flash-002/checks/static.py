"""Static checks for nxp-mcxc-flash-002.

L0: pattern matching on generated source text, no compilation needed.
"""

import re

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate MCXC144 power-loss safe flash write code structure."""
    details: list[CheckDetail] = []

    has_header = scoped_contains(generated_code, "fsl_flash.h", scope="code_only")
    details.append(CheckDetail(
        check_name="header_fsl_flash_h",
        passed=has_header,
        expected="fsl_flash.h included",
        actual="present" if has_header else "missing",
        check_type="exact_match",
    ))

    # Magic constant present (optional U suffix)
    has_magic = bool(re.search(r"0[xX][Dd][Ee][Aa][Dd][Bb][Ee]{2}[Ff][Uu]?", generated_code))
    details.append(CheckDetail(
        check_name="magic_constant_defined",
        passed=has_magic,
        expected="0xDEADBEEF magic constant defined",
        actual="present" if has_magic else "missing",
        check_type="exact_match",
    ))

    # Two flash slot addresses defined (optional U suffix)
    has_slot_a = bool(re.search(r"0[xX]1[Ee]000[Uu]?", generated_code))
    has_slot_b = bool(re.search(r"0[xX]1[Ee]400[Uu]?", generated_code))
    details.append(CheckDetail(
        check_name="two_flash_slots_defined",
        passed=has_slot_a and has_slot_b,
        expected="Both slot addresses 0x1E000 and 0x1E400 defined",
        actual="both present" if (has_slot_a and has_slot_b) else
               "slot A missing" if not has_slot_a else "slot B missing",
        check_type="exact_match",
    ))

    # CRC calculation present
    has_crc = bool(re.search(r"\bcrc\w*\s*\(", generated_code, re.IGNORECASE))
    details.append(CheckDetail(
        check_name="crc_function_implemented",
        passed=has_crc,
        expected="CRC function implemented",
        actual="present" if has_crc else "missing",
        check_type="exact_match",
    ))

    has_erase = scoped_contains(generated_code, "FLASH_EraseSector", scope="stripped")
    has_program = scoped_contains(generated_code, "FLASH_Program", scope="stripped")
    has_verify = scoped_contains(generated_code, "FLASH_VerifyProgram", scope="stripped")
    details.append(CheckDetail(
        check_name="full_flash_sequence_present",
        passed=has_erase and has_program and has_verify,
        expected="FLASH_EraseSector + FLASH_Program + FLASH_VerifyProgram all present",
        actual="complete" if (has_erase and has_program and has_verify) else
               f"missing: {', '.join(x for x, ok in [('erase', has_erase), ('program', has_program), ('verify', has_verify)] if not ok)}",
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
