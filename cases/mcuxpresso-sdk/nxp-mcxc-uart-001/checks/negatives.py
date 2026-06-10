"""Negative tests for nxp-mcxc-uart-001 (UART TX blocking).

Reference: cases/mcuxpresso-sdk/nxp-mcxc-uart-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic MCXC144 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


NEGATIVES = [
    {
        "name": "missing_clock_gates",
        "description": "CLOCK_EnableClock removed — UART/PORT access bus-faults with gated clock",
        "mutation": lambda code: _remove_lines(code, "CLOCK_EnableClock"),
        "must_fail": ["clock_gate_before_uart_init"],
    },
    {
        "name": "missing_pinmux",
        "description": "PORT_SetPinMux removed — TX pin stays on default mux, no output",
        "mutation": lambda code: _remove_lines(code, "PORT_SetPinMux"),
        "must_fail": ["pinmux_before_uart_init"],
    },
    {
        "name": "tx_not_enabled",
        "description": "enableTx left at default false — UART_WriteBlocking hangs forever",
        "mutation": lambda code: _remove_lines(code, "config.enableTx"),
        "must_fail": ["uart_tx_enabled_in_config"],
    },
    {
        "name": "missing_uart_init",
        "description": "UART_Init removed — peripheral never configured",
        "mutation": lambda code: _remove_lines(code, "UART_Init(UART_BASE"),
        "must_fail": ["uart_init_called"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": ["header_fsl_uart_h", "header_fsl_port_h", "header_fsl_clock_h"],
    },
    {
        "name": "stm32_uart_transmit",
        "description": "STM32 HAL_UART_Transmit used instead of MCUXpresso write API",
        "mutation": lambda code: code.replace(
            "UART_WriteBlocking(UART_BASE, s_msg, strlen((const char *)s_msg));",
            "HAL_UART_Transmit(&huart0, s_msg, sizeof(s_msg) - 1U, 100);",
        ),
        "must_fail": ["uart_write_blocking_used", "no_cross_platform_hallucination"],
    },
]
