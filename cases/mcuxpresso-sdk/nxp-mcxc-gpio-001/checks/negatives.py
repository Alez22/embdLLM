"""Negative tests for nxp-mcxc-gpio-001 (GPIO output init + toggle).

Reference: cases/mcuxpresso-sdk/nxp-mcxc-gpio-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic MCXC144 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""

import re


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


NEGATIVES = [
    {
        "name": "missing_clock_gate",
        "description": "CLOCK_EnableClock removed — PORT/GPIO access bus-faults with gated clock",
        "mutation": lambda code: _remove_lines(code, "CLOCK_EnableClock"),
        "must_fail": ["clock_gate_before_gpio_init"],
    },
    {
        "name": "clock_gate_after_init",
        "description": "Clock enabled after GPIO_PinInit — init writes to a gated peripheral",
        "mutation": lambda code: (
            code
            .replace("    CLOCK_EnableClock(kCLOCK_PortE);\n", "")
            .replace(
                "GPIO_PinInit(LED_GPIO, LED_PIN, &led_config);",
                "GPIO_PinInit(LED_GPIO, LED_PIN, &led_config);\n"
                "    CLOCK_EnableClock(kCLOCK_PortE);",
            )
        ),
        "must_fail": ["clock_gate_before_gpio_init"],
    },
    {
        "name": "missing_pinmux",
        "description": "PORT_SetPinMux removed — pin stays on default (disabled) mux, LED never driven",
        "mutation": lambda code: _remove_lines(code, "PORT_SetPinMux"),
        "must_fail": ["pinmux_as_gpio_before_init", "gpio_mux_enum_used"],
    },
    {
        "name": "raw_mux_integer",
        "description": "Magic number instead of kPORT_MuxAsGpio — unreadable and SDK-version fragile",
        "mutation": lambda code: code.replace("kPORT_MuxAsGpio", "1U"),
        "must_fail": ["gpio_mux_enum_used"],
    },
    {
        "name": "input_direction",
        "description": "Pin configured as input — output driver disabled, toggle has no effect",
        "mutation": lambda code: code.replace("kGPIO_DigitalOutput", "kGPIO_DigitalInput"),
        "must_fail": ["output_direction_configured"],
    },
    {
        "name": "missing_gpio_init",
        "description": "GPIO_PinInit removed — direction register never configured",
        "mutation": lambda code: _remove_lines(code, "GPIO_PinInit"),
        "must_fail": ["gpio_pin_init_called"],
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
        # Replace ALL toggle/write spellings gpio_toggle_called accepts
        # (GPIO_PortToggle / GPIO_PinWrite / GPIO_TogglePinsOutput) with the
        # Arduino call, regardless of arguments. Must cover every accepted form
        # or the check still sees a remaining accepted call and passes.
        "mutation": lambda code: re.sub(
            r"\bGPIO_(?:PortToggle|PinWrite|TogglePinsOutput)\s*\([^;]*\);",
            "digitalWrite(LED_PIN, !digitalRead(LED_PIN));",
            code,
        ),
        "must_fail": ["gpio_toggle_called", "no_cross_platform_hallucination"],
    },
]
