"""Behavioral checks for nxp-rt1170-lpuart-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded engineer targeting i.MX RT1170 must know.
"""

import re

from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.check_utils_nxp import has_iomuxc_before_init
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit MCUXpresso SDK knowledge for RT1170 LPUART echo."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    # Pad mux via IOMUXC before LPUART init (implicit)
    mux_ordered = has_iomuxc_before_init(generated_code, "LPUART_Init")
    has_mux = bool(re.search(r"\bIOMUXC\w*_SetPinMux\s*\(", stripped))
    mux_ok = has_mux and mux_ordered
    details.append(CheckDetail(
        check_name="iomuxc_before_lpuart_init",
        passed=mux_ok,
        expected="IOMUXC_SetPinMux called before LPUART_Init",
        actual="correct order" if mux_ok else (
            "IOMUXC_SetPinMux missing" if not has_mux else "wrong order"
        ),
        check_type="constraint",
    ))

    # Clock root configured — single-file program has no BOARD_BootClockRUN,
    # the LPUART root must be set explicitly (implicit)
    has_clock_root = scoped_contains(
        generated_code, "CLOCK_SetRootClock", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="clock_root_configured",
        passed=has_clock_root,
        expected="CLOCK_SetRootClock called for the LPUART clock root",
        actual="present" if has_clock_root else "missing",
        check_type="constraint",
    ))

    # MCUXpresso gotcha: LPUART_GetDefaultConfig leaves enableTx/enableRx
    # false — the UART stays silent unless both are enabled (implicit)
    tx_on = bool(
        re.search(r"\benableTx\s*=\s*true\b", stripped)
        or re.search(r"\bLPUART_EnableTx\s*\(", stripped)
    )
    rx_on = bool(
        re.search(r"\benableRx\s*=\s*true\b", stripped)
        or re.search(r"\bLPUART_EnableRx\s*\(", stripped)
    )
    tx_rx_ok = tx_on and rx_on
    details.append(CheckDetail(
        check_name="tx_rx_enabled",
        passed=tx_rx_ok,
        expected="enableTx and enableRx set (default config disables both)",
        actual="both enabled" if tx_rx_ok else (
            "TX not enabled" if not tx_on else "RX not enabled"
        ),
        check_type="constraint",
    ))

    # LPUART_Init returns status_t: unreachable baud rates must be caught
    has_status_check = scoped_contains(
        generated_code, "kStatus_Success", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="init_status_checked",
        passed=has_status_check,
        expected="kStatus_Success checked on LPUART_Init",
        actual="present" if has_status_check else "missing",
        check_type="constraint",
    ))

    # No legacy Kinetis UART API — RT1170 has LPUART only. \b stops a match
    # inside LPUART_* (no word boundary between 'P' and 'U'). Match known
    # API verbs only, so user macros like UART_CLOCK_FREQ(...) don't trip it.
    has_legacy = bool(re.search(
        r"\bUART_(?:Init|Deinit|GetDefaultConfig|ReadBlocking|WriteBlocking"
        r"|Enable\w*|TransferSendBlocking|TransferReceiveBlocking)\s*\(",
        stripped,
    ))
    details.append(CheckDetail(
        check_name="no_legacy_kinetis_uart_api",
        passed=not has_legacy,
        expected="LPUART_* API used, not Kinetis UART_*",
        actual="clean" if not has_legacy else "Kinetis UART_* API found",
        check_type="constraint",
    ))

    return details
