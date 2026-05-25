"""Static checks for nxp-mcxc-i2c-002.

L0: pattern matching on generated source text, no compilation needed.
"""

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate MCXC144 I2C write + read-back code structure."""
    details: list[CheckDetail] = []

    for header in ("fsl_i2c.h", "fsl_port.h", "fsl_clock.h"):
        present = scoped_contains(generated_code, header, scope="code_only")
        details.append(CheckDetail(
            check_name=f"header_{header.replace('.', '_')}",
            passed=present,
            expected=f"{header} included",
            actual="present" if present else "missing",
            check_type="exact_match",
        ))

    has_init = scoped_contains(generated_code, "I2C_MasterInit", scope="stripped")
    details.append(CheckDetail(
        check_name="i2c_master_init_called",
        passed=has_init,
        expected="I2C_MasterInit called",
        actual="present" if has_init else "missing",
        check_type="exact_match",
    ))

    # Both a write transfer and a read transfer must be present
    has_write = scoped_contains(generated_code, "kI2C_Write", scope="stripped")
    has_read  = scoped_contains(generated_code, "kI2C_Read",  scope="stripped")
    details.append(CheckDetail(
        check_name="both_write_and_read_transfers",
        passed=has_write and has_read,
        expected="Both kI2C_Write and kI2C_Read transfers present",
        actual="both present" if (has_write and has_read) else
               "write missing" if not has_write else "read missing",
        check_type="exact_match",
    ))

    import re
    # Two calls to I2C_MasterTransferBlocking
    transfer_count = len(re.findall(r"\bI2C_MasterTransferBlocking\s*\(", generated_code))
    details.append(CheckDetail(
        check_name="two_separate_transfers",
        passed=transfer_count >= 2,
        expected="At least 2 I2C_MasterTransferBlocking calls (write + read)",
        actual=f"{transfer_count} call(s) found",
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
