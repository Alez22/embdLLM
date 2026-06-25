"""Negative tests for nxp-mcxc-uart-002 (UART RX interrupt + ring buffer).

Reference: cases/mcuxpresso-sdk/nxp-mcxc-uart-002/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic MCXC144 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""

import re

_ISR_FLAG_CHECK_BLOCK = (
    "    if (UART_GetStatusFlags(UART_BASE) & kUART_RxDataRegFullFlag) {\n"
    "        ring_push(UART_ReadByte(UART_BASE));\n"
    "    }\n"
)


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
        "name": "missing_nvic_enable",
        "description": "EnableIRQ removed — UART RX interrupt pends but never fires",
        "mutation": lambda code: _remove_lines(code, "EnableIRQ"),
        "must_fail": ["nvic_uart_interrupt_enabled"],
    },
    {
        "name": "missing_uart_enable_interrupts",
        "description": "UART_EnableInterrupts removed — RX flag never generates an interrupt",
        "mutation": lambda code: _remove_lines(code, "UART_EnableInterrupts"),
        "must_fail": ["uart_rx_interrupt_enabled"],
    },
    {
        "name": "buffer_not_volatile",
        "description": "volatile dropped from ring buffer array shared between ISR and main",
        # Strip every 'volatile' qualifier regardless of type/name/spacing. The
        # literal replace assumed the exact declaration (type + buffer name +
        # double space) and missed nearly every model. ring_buffer_volatile
        # matches a volatile uint8_t array.
        "mutation": lambda code: re.sub(r"\bvolatile\s+", "", code),
        "must_fail": ["ring_buffer_volatile"],
    },
    {
        "name": "tail_not_volatile",
        "description": "volatile dropped from tail index — main may spin on a stale copy",
        # Strip every 'volatile' qualifier so fewer than 2 volatile indices
        # remain. The literal replace assumed the exact name s_rx_tail and
        # missed models using head/tail/write_idx/etc. spellings.
        "mutation": lambda code: re.sub(r"\bvolatile\s+", "", code),
        "must_fail": ["ring_buffer_indices_volatile"],
    },
    {
        "name": "unconditional_read_in_isr",
        "description": "RX flag not checked in ISR — reads garbage when another flag triggered the IRQ",
        "mutation": lambda code: code.replace(
            _ISR_FLAG_CHECK_BLOCK,
            "    ring_push(UART_ReadByte(UART_BASE));\n",
        ),
        "must_fail": ["rx_flag_checked_in_isr"],
    },
    {
        "name": "isr_not_vector_named",
        "description": "Handler renamed — no longer matches the vector table entry, never called",
        "mutation": lambda code: code.replace("UART2_FLEXIO_IRQHandler", "uart_rx_callback"),
        "must_fail": ["uart_isr_handler_defined", "rx_flag_checked_in_isr"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": ["header_fsl_uart_h", "header_fsl_port_h", "header_fsl_clock_h"],
    },
    {
        "name": "zephyr_msgq",
        "description": "Zephyr k_msgq API used instead of bare-metal ring buffer drain",
        # Inject the Zephyr k_msgq API by replacing any UART write call,
        # regardless of base/args.
        "mutation": lambda code: re.sub(
            r"\bUART_Write\w*\s*\([^;]*\);",
            "k_msgq_put(&uart_msgq, line_buf, K_NO_WAIT);",
            code,
            count=1,
        ),
        "must_fail": ["no_cross_platform_hallucination"],
    },
]
