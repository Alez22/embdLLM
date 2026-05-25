"""Behavioral checks for nxp-mcxc-flash-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention.
"""

import re

from embedeval.check_utils import scoped_contains
from embedeval.models import CheckDetail


def _pos(code: str, token: str) -> int:
    """Return position of first occurrence of token, or -1."""
    m = re.search(re.escape(token), code)
    return m.start() if m else -1


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit flash driver knowledge for MCXC144."""
    details: list[CheckDetail] = []

    # Erase must come before program — bits can only go 1→0
    erase_pos   = _pos(generated_code, "FLASH_EraseSector")
    program_pos = _pos(generated_code, "FLASH_Program")
    erase_before_write = (erase_pos != -1 and program_pos != -1
                          and erase_pos < program_pos)
    details.append(CheckDetail(
        check_name="erase_before_write",
        passed=erase_before_write,
        expected="FLASH_EraseSector called before FLASH_Program",
        actual="correct order" if erase_before_write else "wrong order or missing",
        check_type="constraint",
    ))

    # Verify after program
    verify_pos = _pos(generated_code, "FLASH_VerifyProgram")
    verify_after_write = (program_pos != -1 and verify_pos != -1
                          and verify_pos > program_pos)
    details.append(CheckDetail(
        check_name="verify_after_write",
        passed=verify_after_write,
        expected="FLASH_VerifyProgram called after FLASH_Program",
        actual="correct order" if verify_after_write else "wrong order or missing",
        check_type="constraint",
    ))

    # Return values checked — must not silently ignore errors
    has_status_check = scoped_contains(generated_code, "kStatus_Success", scope="stripped")
    details.append(CheckDetail(
        check_name="flash_return_value_checked",
        passed=has_status_check,
        expected="kStatus_Success checked after flash operations",
        actual="present" if has_status_check else "missing — errors silently ignored",
        check_type="constraint",
    ))

    # Erase key used (kFLASH_ApiEraseKey) — required by SDK security model
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
