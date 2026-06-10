"""Behavioral checks for nxp-rt1170-lpi2c-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded engineer targeting i.MX RT1170 must know.
"""

import re

from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.check_utils_nxp import has_iomuxc_before_init
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit MCUXpresso SDK knowledge for RT1170 LPI2C master."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    # Pad mux via IOMUXC before LPI2C init (implicit)
    mux_ordered = has_iomuxc_before_init(generated_code, "LPI2C_MasterInit")
    has_mux = bool(re.search(r"\bIOMUXC\w*_SetPinMux\s*\(", stripped))
    mux_ok = has_mux and mux_ordered
    details.append(CheckDetail(
        check_name="iomuxc_before_lpi2c_init",
        passed=mux_ok,
        expected="IOMUXC_SetPinMux called before LPI2C_MasterInit",
        actual="correct order" if mux_ok else (
            "IOMUXC_SetPinMux missing" if not has_mux else "wrong order"
        ),
        check_type="constraint",
    ))

    # Clock root configured — on RT1170 there is no BOARD_BootClockRUN in a
    # single-file program; the LPI2C root must be set explicitly (implicit)
    has_clock_root = scoped_contains(
        generated_code, "CLOCK_SetRootClock", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="clock_root_configured",
        passed=has_clock_root,
        expected="CLOCK_SetRootClock called for the LPI2C clock root",
        actual="present" if has_clock_root else "missing",
        check_type="constraint",
    ))

    # 7-bit address (0x68), not pre-shifted (0xD0 or 0x68 << 1)
    has_preshifted = bool(re.search(r"0[xX][Dd]0[Uu]?\b", stripped))
    has_shift_expr = bool(re.search(r"0[xX]68[Uu]?\s*<<\s*1", stripped))
    addr_ok = not has_preshifted and not has_shift_expr
    details.append(CheckDetail(
        check_name="i2c_address_not_preshifted",
        passed=addr_ok,
        expected="7-bit address 0x68 used (SDK shifts internally)",
        actual="correct" if addr_ok else (
            "shift expression 0x68 << 1 found" if has_shift_expr
            else "hardcoded 0xD0 found"
        ),
        check_type="constraint",
    ))

    # Transfer return value checked (implicit)
    has_status_check = scoped_contains(
        generated_code, "kStatus_Success", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="transfer_return_value_checked",
        passed=has_status_check,
        expected="kStatus_Success checked after LPI2C_MasterTransferBlocking",
        actual="present" if has_status_check else "missing",
        check_type="constraint",
    ))

    # Default transfer flag set
    has_flag = scoped_contains(
        generated_code, "kLPI2C_TransferDefaultFlag", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="default_transfer_flag_set",
        passed=has_flag,
        expected="kLPI2C_TransferDefaultFlag set in transfer struct",
        actual="present" if has_flag else "missing",
        check_type="constraint",
    ))

    # No legacy Kinetis I2C API — RT1170 has LPI2C only. \b stops a match
    # inside LPI2C_Master* (no word boundary between 'P' and 'I').
    has_legacy = bool(re.search(r"\bI2C_Master\w*\s*\(", stripped))
    details.append(CheckDetail(
        check_name="no_legacy_kinetis_i2c_api",
        passed=not has_legacy,
        expected="LPI2C_* API used, not Kinetis I2C_Master*",
        actual="clean" if not has_legacy else "Kinetis I2C_Master* API found",
        check_type="constraint",
    ))

    return details
