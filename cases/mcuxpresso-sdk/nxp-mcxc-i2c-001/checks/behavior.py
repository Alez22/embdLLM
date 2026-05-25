"""Behavioral checks for nxp-mcxc-i2c-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded engineer targeting MCXC144 must know.
"""

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import has_clock_gate_before, has_pinmux_before_init
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit MCUXpresso SDK knowledge for I2C master init."""
    details: list[CheckDetail] = []

    # Clock gate before I2C init (implicit: prompt never mentions this)
    clock_ordered = has_clock_gate_before(generated_code, "I2C_MasterInit")
    details.append(CheckDetail(
        check_name="clock_gate_before_i2c_init",
        passed=clock_ordered,
        expected="CLOCK_EnableClock called before I2C_MasterInit",
        actual="correct order" if clock_ordered else "missing or wrong order",
        check_type="constraint",
    ))

    # Pin mux before I2C init (implicit: prompt never mentions this)
    pinmux_ordered = has_pinmux_before_init(generated_code, "I2C_MasterInit")
    details.append(CheckDetail(
        check_name="pinmux_before_i2c_init",
        passed=pinmux_ordered,
        expected="PORT_SetPinMux called before I2C_MasterInit",
        actual="correct order" if pinmux_ordered else "missing or wrong order",
        check_type="constraint",
    ))

    # I2C address must be 7-bit (0x68), not pre-shifted to 8-bit
    # MCUXpresso SDK handles the shift internally — passing 0xD0 is wrong
    import re
    has_shifted_addr = bool(re.search(r"\b0[xX][Dd]0\b", generated_code))
    details.append(CheckDetail(
        check_name="i2c_address_not_preshifted",
        passed=not has_shifted_addr,
        expected="7-bit address 0x68 used (SDK shifts internally)",
        actual="correct" if not has_shifted_addr else "address pre-shifted to 0xD0 (wrong for MCUXpresso)",
        check_type="constraint",
    ))

    # Error return value checked after I2C_MasterTransferBlocking
    has_error_check = scoped_contains(generated_code, "kStatus_Success", scope="stripped")
    details.append(CheckDetail(
        check_name="transfer_return_value_checked",
        passed=has_error_check,
        expected="kStatus_Success checked after I2C_MasterTransferBlocking",
        actual="present" if has_error_check else "missing",
        check_type="constraint",
    ))

    # Default transfer flag used
    has_default_flag = scoped_contains(
        generated_code, "kI2C_TransferDefaultFlag", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="default_transfer_flag_set",
        passed=has_default_flag,
        expected="kI2C_TransferDefaultFlag set in transfer struct",
        actual="present" if has_default_flag else "missing",
        check_type="constraint",
    ))

    return details
