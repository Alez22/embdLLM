"""Negative tests for nxp-rt1170-lpuart-001 (LPUART echo).

Reference: cases/mcuxpresso-sdk/nxp-rt1170-lpuart-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic RT1170 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.

Mutations must match how a *model* writes the code, not only the exact
spelling in the reference. Literal string replaces silently no-op when the
candidate used a synonym (CLOCK_SetRootClockMux vs CLOCK_SetRootClock), a
different base (LPUART1 vs UART_BASE) or different spacing (115200 vs
115200U) — the mutation is then "skipped (code unchanged)" and the check is
never exercised. Prefer regex line-removal / regex replace that covers every
form the corresponding check accepts.
"""

import re


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


def _remove_matching(code: str, pattern: str) -> str:
    """Remove all lines matching the regex *pattern*."""
    rx = re.compile(pattern)
    return "\n".join(line for line in code.splitlines() if not rx.search(line))


NEGATIVES = [
    {
        "name": "missing_iomuxc_mux",
        "description": "IOMUXC_SetPinMux removed — TX/RX pads stay on default function, UART dead",
        "mutation": lambda code: _remove_lines(code, "IOMUXC_SetPinMux"),
        "must_fail": ["iomuxc_before_lpuart_init"],
    },
    {
        "name": "iomuxc_after_init",
        "description": "Pads muxed after LPUART_Init — init runs while pads are unrouted",
        "mutation": lambda code: (
            _remove_lines(code, "IOMUXC_SetPinMux")
            .replace(
                "    while (1) {\n        uint8_t ch;",
                "    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_24_LPUART1_TXD, 0U);\n"
                "    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_25_LPUART1_RXD, 0U);\n\n"
                "    while (1) {\n        uint8_t ch;",
            )
        ),
        "must_fail": ["iomuxc_before_lpuart_init"],
    },
    {
        "name": "missing_clock_root",
        "description": "CLOCK_SetRootClock removed — LPUART root left at reset state, wrong baud clock",
        # Remove every clock-root form clock_root_configured accepts (single
        # CLOCK_SetRootClock, split Mux/Div, low-level SetMux/SetDiv, board
        # wrappers) — not just the single-call spelling.
        "mutation": lambda code: _remove_matching(
            code,
            r"\bCLOCK_Set(?:RootClock(?:Mux|Div)?|Mux|Div)\s*\("
            r"|\bBOARD_(?:BootClockRUN|InitBootClocks)\w*\s*\(",
        ),
        "must_fail": ["clock_root_configured"],
    },
    {
        "name": "tx_rx_left_disabled",
        "description": "enableTx/enableRx not set — default config leaves the UART silent",
        # tx_rx_enabled accepts EITHER the config fields OR the LPUART_EnableTx/
        # Rx calls, so the mutation must strip both forms (any spacing) to
        # actually disable TX/RX.
        "mutation": lambda code: _remove_matching(
            code,
            r"\.enable(?:Tx|Rx)\s*=\s*true"
            r"|\bLPUART_Enable(?:Tx|Rx)\s*\(",
        ),
        "must_fail": ["tx_rx_enabled"],
    },
    {
        "name": "init_status_ignored",
        "description": "LPUART_Init return value discarded — unreachable baud rate goes unnoticed",
        # init_status_checked only looks for the token kStatus_Success, so the
        # mutation removes every line mentioning it (the status compare and any
        # status_t = LPUART_Init(...) assignment guarded by it). Independent of
        # the LPUART base name (UART_BASE vs LPUART1) or the exact if-shape.
        "mutation": lambda code: _remove_matching(code, r"\bkStatus_Success\b"),
        "must_fail": ["init_status_checked"],
    },
    {
        "name": "wrong_baud_rate",
        "description": "9600 baud configured instead of the requested 115200",
        # baud_rate_configured matches 115200 with an optional U/u suffix, so
        # replace the number regardless of suffix.
        "mutation": lambda code: re.sub(r"\b115200[Uu]?\b", "9600U", code),
        "must_fail": ["baud_rate_configured"],
    },
    {
        "name": "kinetis_uart_api",
        "description": "Kinetis UART_* API used — wrong NXP family, RT1170 has LPUART only",
        # Demote the LPUART read API (ReadBlocking or the register-level
        # ReadByte) to the legacy Kinetis UART_ReadBlocking spelling.
        # no_legacy_kinetis_uart_api only flags a fixed set of UART_* names
        # (ReadBlocking among them, but NOT ReadByte), so normalise any LPUART
        # read to UART_ReadBlocking.
        "mutation": lambda code: re.sub(
            r"\bLPUART_Read\w*\s*\(", "UART_ReadBlocking(", code
        ),
        "must_fail": ["no_legacy_kinetis_uart_api"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": ["header_fsl_lpuart_h", "header_fsl_iomuxc_h"],
    },
    {
        "name": "arduino_serial",
        "description": "Arduino Serial API used instead of MCUXpresso LPUART API",
        # Replace any LPUART write call (WriteBlocking or register-level
        # WriteByte) with the Arduino Serial API that
        # no_cross_platform_hallucination flags.
        "mutation": lambda code: re.sub(
            r"\bLPUART_Write\w*\s*\([^;]*\);", "Serial.write(ch);", code
        ),
        "must_fail": ["no_cross_platform_hallucination"],
    },
]
