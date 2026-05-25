"""Behavioral checks for nxp-mcxc-i2c-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded engineer targeting MCXC144 must know.
"""

import re

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import has_clock_gate_before, has_pinmux_before_init
from embedeval.models import CheckDetail

# Any I2C init call the model might use — correct or wrong API name.
# We check ordering against all of them so a wrong-name init still triggers
# the clock/pinmux ordering check instead of silently passing.
_I2C_INIT_CANDIDATES = [
    "I2C_MasterInit",
    "I2C_Init",
    "I2C_MasterGetDefaultConfig",
]


def _find_any_i2c_init(code: str) -> str | None:
    """Return the first I2C init function name found in code, or None."""
    for candidate in _I2C_INIT_CANDIDATES:
        if re.search(rf"\b{re.escape(candidate)}\s*\(", code):
            return candidate
    return None


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit MCUXpresso SDK knowledge for I2C master init."""
    details: list[CheckDetail] = []

    i2c_init = _find_any_i2c_init(generated_code) or "I2C_MasterInit"

    # Clock gate before I2C init (implicit: prompt never mentions this)
    clock_ordered = has_clock_gate_before(generated_code, i2c_init)
    # Also fail if CLOCK_EnableClock is simply absent
    has_clock = scoped_contains(generated_code, "CLOCK_EnableClock", scope="stripped")
    clock_ok = has_clock and clock_ordered
    details.append(CheckDetail(
        check_name="clock_gate_before_i2c_init",
        passed=clock_ok,
        expected="CLOCK_EnableClock called before I2C init",
        actual="correct order" if clock_ok else (
            "CLOCK_EnableClock missing" if not has_clock else "wrong order"
        ),
        check_type="constraint",
    ))

    # Pin mux before I2C init (implicit: prompt never mentions this)
    pinmux_ordered = has_pinmux_before_init(generated_code, i2c_init)
    has_pinmux = bool(re.search(r"\bPORT_SetPin\w+\s*\(", generated_code))
    pinmux_ok = has_pinmux and pinmux_ordered
    details.append(CheckDetail(
        check_name="pinmux_before_i2c_init",
        passed=pinmux_ok,
        expected="PORT_SetPinMux called before I2C init",
        actual="correct order" if pinmux_ok else (
            "PORT_SetPinMux missing" if not has_pinmux else "wrong order"
        ),
        check_type="constraint",
    ))

    # I2C address must be 7-bit (0x68), not pre-shifted.
    # MCUXpresso SDK handles the shift internally.
    # Wrong forms: 0xD0 hardcoded, or any expression like (0x68 << 1).
    has_preshifted_literal = bool(re.search(r"\b0[xX][Dd]0\b", generated_code))
    has_shift_expr = bool(re.search(r"\b0[xX]68\b\s*<<\s*1", generated_code))
    addr_ok = not has_preshifted_literal and not has_shift_expr
    details.append(CheckDetail(
        check_name="i2c_address_not_preshifted",
        passed=addr_ok,
        expected="7-bit address 0x68 used (SDK shifts internally)",
        actual="correct" if addr_ok else (
            "shift expression 0x68 << 1 found" if has_shift_expr else "hardcoded 0xD0 found"
        ),
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
