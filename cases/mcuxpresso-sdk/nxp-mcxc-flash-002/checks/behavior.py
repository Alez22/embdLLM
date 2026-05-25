"""Behavioral checks for nxp-mcxc-flash-002.

L3: verifies implicit domain knowledge about power-loss safe patterns.
"""

import re

from embedeval.check_utils import scoped_contains
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit knowledge for power-loss safe flash write."""
    details: list[CheckDetail] = []

    # Both slots must be written — detect either via two FLASH_EraseSector
    # calls or two separate flash write helper calls referencing both addresses.
    erase_calls = re.findall(r"FLASH_EraseSector\s*\(", generated_code)
    program_calls = re.findall(r"FLASH_Program\s*\(", generated_code)
    # Also accept a helper function called twice with different slot addresses
    slot_a_writes = len(re.findall(r"(SLOT_A|0[xX]1[Ee]000)", generated_code))
    slot_b_writes = len(re.findall(r"(SLOT_B|0[xX]1[Ee]400)", generated_code))
    two_slots_written = (
        len(erase_calls) >= 2
        or len(program_calls) >= 2
        or (slot_a_writes >= 1 and slot_b_writes >= 1)
    )
    details.append(CheckDetail(
        check_name="both_slots_written",
        passed=two_slots_written,
        expected="Both flash slots written (inactive first, then active)",
        actual="present" if two_slots_written else "only one slot written",
        check_type="constraint",
    ))

    # Verify after every program (not just once at the end)
    program_count = len(re.findall(r"\bFLASH_Program\s*\(", generated_code))
    verify_count  = len(re.findall(r"\bFLASH_VerifyProgram\s*\(", generated_code))
    details.append(CheckDetail(
        check_name="verify_after_each_write",
        passed=verify_count >= program_count and program_count > 0,
        expected="FLASH_VerifyProgram called at least once per FLASH_Program",
        actual=f"{verify_count} verify vs {program_count} program call(s)",
        check_type="constraint",
    ))

    # Corruption recovery: both slots invalid → assign magic and default data.
    # Look for an assignment to ->magic (or equivalent struct field) outside
    # the normal write path — indicates a "reset to defaults" branch.
    has_default = bool(re.search(
        r"(->magic|\.magic)\s*=(?!=)", generated_code
    )) and bool(re.search(
        r"(->data|\.data|->crc|\.crc)\s*=\s*[^=]", generated_code
    ))
    details.append(CheckDetail(
        check_name="corruption_recovery_handled",
        passed=has_default,
        expected="Handles both-slots-corrupt case: assigns magic and default data fields",
        actual="present" if has_default else "missing",
        check_type="constraint",
    ))

    # CRC covers magic+data but NOT the stored crc field (to avoid circular)
    # Look for offsetof or sizeof-based partial CRC calculation
    has_partial_crc = bool(re.search(
        r"(offsetof|sizeof\s*\(\s*\w+\s*\)\s*-\s*sizeof)", generated_code
    ))
    details.append(CheckDetail(
        check_name="crc_excludes_crc_field",
        passed=has_partial_crc,
        expected="CRC computed over magic+data only (offsetof or sizeof-N pattern)",
        actual="present" if has_partial_crc else "missing — CRC may cover itself (circular)",
        check_type="constraint",
    ))

    # Erase key used
    has_erase_key = scoped_contains(
        generated_code, "kFLASH_ApiEraseKey", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="flash_erase_key_used",
        passed=has_erase_key,
        expected="kFLASH_ApiEraseKey passed to FLASH_EraseSector",
        actual="present" if has_erase_key else "missing",
        check_type="constraint",
    ))

    return details
