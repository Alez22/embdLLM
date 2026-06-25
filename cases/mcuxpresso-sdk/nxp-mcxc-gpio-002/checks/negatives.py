"""Negative tests for nxp-mcxc-gpio-002 (GPIO input with edge IRQ).

Reference: cases/mcuxpresso-sdk/nxp-mcxc-gpio-002/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic MCXC144 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""

import re

# Exact ISR flag-clear block in the reference (comment + call + blank line).
_ISR_CLEAR_BLOCK = (
    "    /* Clear interrupt flag before any other action to avoid re-entry */\n"
    "    GPIO_PortClearInterruptFlags(BTN_GPIO, 1U << BTN_PIN);\n"
    "\n"
)


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


NEGATIVES = [
    {
        "name": "missing_clock_gates",
        "description": "CLOCK_EnableClock removed — PORT access bus-faults with gated clock",
        "mutation": lambda code: _remove_lines(code, "CLOCK_EnableClock"),
        "must_fail": ["clock_gate_before_gpio_init"],
    },
    {
        "name": "missing_nvic_enable",
        "description": "EnableIRQ removed — PORT interrupt pends but never fires",
        "mutation": lambda code: _remove_lines(code, "EnableIRQ"),
        "must_fail": ["nvic_interrupt_enabled"],
    },
    {
        "name": "nonvolatile_counter",
        "description": "volatile dropped from ISR-shared counter — compiler may cache it in a register",
        # NOTE: must_fail references 'isr_shared_variable_volatile', which this
        # case intentionally does NOT define (see behavior.py). This mutation is
        # therefore dangling and always reports as missed — flagged for review.
        # Mutation kept regex-based for consistency (strips all volatile).
        "mutation": lambda code: re.sub(r"\bvolatile\s+", "", code),
        "must_fail": ["isr_shared_variable_volatile"],
    },
    {
        "name": "rising_edge",
        "description": "Rising edge instead of falling — fires on release, not press",
        "mutation": lambda code: code.replace(
            "kPORT_InterruptFallingEdge", "kPORT_InterruptRisingEdge"
        ),
        "must_fail": ["falling_edge_interrupt_configured"],
    },
    {
        "name": "missing_pin_interrupt_config",
        "description": "PORT_SetPinInterruptConfig removed — pin never generates interrupts",
        "mutation": lambda code: _remove_lines(code, "PORT_SetPinInterruptConfig"),
        "must_fail": ["pin_interrupt_configured", "falling_edge_interrupt_configured"],
    },
    {
        "name": "flag_never_cleared",
        "description": "Interrupt flag never cleared — ISR re-enters forever, main starves",
        "mutation": lambda code: _remove_lines(code, "GPIO_PortClearInterruptFlags"),
        "must_fail": ["interrupt_flag_cleared", "flag_cleared_inside_isr"],
    },
    {
        "name": "flag_cleared_in_main",
        "description": "Flag cleared in main loop instead of ISR — ISR storms until main runs",
        "mutation": lambda code: (
            code
            .replace(_ISR_CLEAR_BLOCK, "")
            .replace(
                '        __asm volatile("wfi");',
                "        GPIO_PortClearInterruptFlags(BTN_GPIO, 1U << BTN_PIN);\n"
                '        __asm volatile("wfi");',
            )
        ),
        "must_fail": ["flag_cleared_inside_isr"],
    },
    {
        "name": "isr_not_vector_named",
        "description": "Handler renamed — no longer matches the vector table entry, never called",
        "mutation": lambda code: code.replace("PORTC_PORTD_IRQHandler", "button_callback"),
        "must_fail": ["isr_handler_defined", "flag_cleared_inside_isr"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": ["header_fsl_gpio_h", "header_fsl_port_h", "header_fsl_clock_h"],
    },
    {
        "name": "arduino_toggle",
        "description": "Arduino digitalWrite used instead of MCUXpresso GPIO API",
        # Inject an Arduino digitalWrite by replacing whichever GPIO output
        # toggle/write call the model used (PortToggle / TogglePinsOutput /
        # PinWrite / ...Output spellings). The literal replace only matched one
        # exact toggle statement and missed every other form.
        "mutation": lambda code: re.sub(
            r"\bGPIO_(?:PortToggle\w*|TogglePinsOutput|PinWrite)\s*\([^;]*\);",
            "digitalWrite(24, HIGH);",
            code,
            count=1,
        ),
        "must_fail": ["no_cross_platform_hallucination"],
    },
]
