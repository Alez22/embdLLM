"""Behavioral checks for nxp-rt1170-lpspi-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded engineer targeting i.MX RT1170 must know.
"""

import re

from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.check_utils_nxp import has_iomuxc_before_init, has_rt1170_clock_root_config
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit MCUXpresso SDK knowledge for RT1170 LPSPI master."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    # Pad mux via IOMUXC before LPSPI init (implicit)
    mux_ordered = has_iomuxc_before_init(generated_code, "LPSPI_MasterInit")
    has_mux = bool(re.search(r"\bIOMUXC\w*_SetPinMux\s*\(", stripped))
    mux_ok = has_mux and mux_ordered
    details.append(CheckDetail(
        check_name="iomuxc_before_lpspi_init",
        passed=mux_ok,
        expected="IOMUXC_SetPinMux called before LPSPI_MasterInit",
        actual="correct order" if mux_ok else (
            "IOMUXC_SetPinMux missing" if not has_mux else "wrong order"
        ),
        check_type="constraint",
    ))

    # Clock root configured — single-file program has no BOARD_BootClockRUN,
    # the LPSPI root must be set explicitly (implicit)
    has_clock_root = has_rt1170_clock_root_config(generated_code)
    details.append(CheckDetail(
        check_name="clock_root_configured",
        passed=has_clock_root,
        expected="CLOCK_SetRootClock called for the LPSPI clock root",
        actual="present" if has_clock_root else "missing",
        check_type="constraint",
    ))

    # PCS must stay asserted across command + response: without the
    # continuous flag the flash sees a deselect after the opcode and the
    # ID bytes read back as 0xFF (implicit — never stated in prompt)
    has_pcs_cont = scoped_contains(
        generated_code, "kLPSPI_MasterPcsContinuous", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="pcs_continuous_set",
        passed=has_pcs_cont,
        expected="kLPSPI_MasterPcsContinuous keeps PCS asserted for the whole frame",
        actual="present" if has_pcs_cont else "missing",
        check_type="constraint",
    ))

    # Transfer return value checked (implicit)
    has_status_check = scoped_contains(
        generated_code, "kStatus_Success", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="transfer_status_checked",
        passed=has_status_check,
        expected="kStatus_Success checked after LPSPI_MasterTransferBlocking",
        actual="present" if has_status_check else "missing",
        check_type="constraint",
    ))

    # No legacy Kinetis SPI/DSPI API — RT1170 has LPSPI only. \b stops a
    # match inside LPSPI_Master* (no word boundary between 'P' and 'S').
    has_legacy = bool(re.search(r"\bD?SPI_Master\w*\s*\(", stripped))
    details.append(CheckDetail(
        check_name="no_legacy_kinetis_spi_api",
        passed=not has_legacy,
        expected="LPSPI_* API used, not Kinetis SPI_/DSPI_Master*",
        actual="clean" if not has_legacy else "Kinetis SPI/DSPI API found",
        check_type="constraint",
    ))

    return details
