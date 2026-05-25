"""Behavioral checks for nxp-mcxc-i2c-002.

L3: verifies implicit domain knowledge — things the prompt does NOT mention.
"""

import re

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import has_clock_gate_before, has_pinmux_before_init
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit MCUXpresso SDK knowledge for I2C write+readback."""
    details: list[CheckDetail] = []

    # Clock gate before I2C_MasterInit
    clock_ok = has_clock_gate_before(generated_code, "I2C_MasterInit")
    has_clock = scoped_contains(generated_code, "CLOCK_EnableClock", scope="stripped")
    details.append(CheckDetail(
        check_name="clock_gate_before_i2c_init",
        passed=has_clock and clock_ok,
        expected="CLOCK_EnableClock called before I2C_MasterInit",
        actual="correct order" if (has_clock and clock_ok) else (
            "CLOCK_EnableClock missing" if not has_clock else "wrong order"
        ),
        check_type="constraint",
    ))

    # Pin mux before I2C_MasterInit
    pinmux_ok = has_pinmux_before_init(generated_code, "I2C_MasterInit")
    has_pinmux = bool(re.search(r"\bPORT_SetPin\w+\s*\(", generated_code))
    details.append(CheckDetail(
        check_name="pinmux_before_i2c_init",
        passed=has_pinmux and pinmux_ok,
        expected="PORT_SetPinMux called before I2C_MasterInit",
        actual="correct order" if (has_pinmux and pinmux_ok) else (
            "PORT_SetPinMux missing" if not has_pinmux else "wrong order"
        ),
        check_type="constraint",
    ))

    # Return values checked on both transfers
    status_check_count = len(re.findall(r"kStatus_Success", generated_code))
    details.append(CheckDetail(
        check_name="both_transfer_returns_checked",
        passed=status_check_count >= 2,
        expected="kStatus_Success checked at least twice (write + read)",
        actual=f"{status_check_count} check(s) found",
        check_type="constraint",
    ))

    # 7-bit address not pre-shifted
    has_preshifted = bool(re.search(r"\b0[xX][Dd]0\b", generated_code))
    has_shift_expr  = bool(re.search(r"\b0[xX]68\b\s*<<\s*1", generated_code))
    addr_ok = not has_preshifted and not has_shift_expr
    details.append(CheckDetail(
        check_name="i2c_address_not_preshifted",
        passed=addr_ok,
        expected="7-bit address 0x68 used (SDK shifts internally)",
        actual="correct" if addr_ok else (
            "shift expression 0x68 << 1 found" if has_shift_expr else "hardcoded 0xD0 found"
        ),
        check_type="constraint",
    ))

    return details
