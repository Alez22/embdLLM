"""Negative tests for nxp-rt1170-lpuart-001 (LPUART echo).

Reference: cases/mcuxpresso-sdk/nxp-rt1170-lpuart-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic RT1170 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


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
        "mutation": lambda code: _remove_lines(code, "CLOCK_SetRootClock("),
        "must_fail": ["clock_root_configured"],
    },
    {
        "name": "tx_rx_left_disabled",
        "description": "enableTx/enableRx not set — default config leaves the UART silent",
        "mutation": lambda code: (
            _remove_lines(code, "config.enableTx")
            .replace("    config.enableRx = true;\n", "")
        ),
        "must_fail": ["tx_rx_enabled"],
    },
    {
        "name": "init_status_ignored",
        "description": "LPUART_Init return value discarded — unreachable baud rate goes unnoticed",
        "mutation": lambda code: code.replace(
            "    if (LPUART_Init(UART_BASE, &config, UART_CLOCK_FREQ) != kStatus_Success) {\n"
            "        /* Requested baud rate not achievable from this clock root */\n"
            "        while (1) {\n"
            "        }\n"
            "    }\n",
            "    LPUART_Init(UART_BASE, &config, UART_CLOCK_FREQ);\n",
        ),
        "must_fail": ["init_status_checked"],
    },
    {
        "name": "wrong_baud_rate",
        "description": "9600 baud configured instead of the requested 115200",
        "mutation": lambda code: code.replace("115200U", "9600U"),
        "must_fail": ["baud_rate_configured"],
    },
    {
        "name": "kinetis_uart_api",
        "description": "Kinetis UART_* API used — wrong NXP family, RT1170 has LPUART only",
        "mutation": lambda code: code.replace(
            "LPUART_ReadBlocking(UART_BASE, &ch, 1U);",
            "UART_ReadBlocking(UART_BASE, &ch, 1U);",
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
        "mutation": lambda code: code.replace(
            "LPUART_WriteBlocking(UART_BASE, &ch, 1U);",
            "Serial.write(ch);",
        ),
        "must_fail": ["no_cross_platform_hallucination"],
    },
]
