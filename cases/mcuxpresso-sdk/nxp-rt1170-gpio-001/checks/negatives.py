"""Negative tests for nxp-rt1170-gpio-001 (GPIO output LED blink).

Reference: cases/mcuxpresso-sdk/nxp-rt1170-gpio-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic RT1170 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""

import re


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


NEGATIVES = [
    {
        "name": "missing_iomuxc_mux",
        "description": "IOMUXC_SetPinMux removed — pad stays on default function, LED dead",
        "mutation": lambda code: _remove_lines(code, "IOMUXC_SetPinMux"),
        "must_fail": ["iomuxc_before_gpio_init"],
    },
    {
        "name": "iomuxc_after_init",
        "description": "Pad muxed after GPIO_PinInit — init writes while pad is unrouted",
        "mutation": lambda code: (
            code
            .replace("    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_04_GPIO9_IO03, 0U);\n", "")
            .replace(
                "GPIO_PinInit(LED_GPIO, LED_PIN, &led_config);",
                "GPIO_PinInit(LED_GPIO, LED_PIN, &led_config);\n"
                "    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_04_GPIO9_IO03, 0U);",
            )
        ),
        "must_fail": ["iomuxc_before_gpio_init"],
    },
    {
        "name": "missing_pad_config",
        "description": "IOMUXC_SetPinConfig removed — pad electrical settings left at reset defaults",
        "mutation": lambda code: _remove_lines(code, "IOMUXC_SetPinConfig"),
        "must_fail": ["pad_config_set"],
    },
    {
        "name": "input_direction",
        "description": "Pin configured as input — output driver disabled, toggle has no effect",
        "mutation": lambda code: code.replace("kGPIO_DigitalOutput", "kGPIO_DigitalInput"),
        "must_fail": ["output_direction_configured"],
    },
    {
        "name": "kinetis_port_mux",
        "description": "Kinetis PORT_SetPinMux used — wrong NXP family, does not exist on RT1170",
        # Replace any IOMUXC_SetPinMux(...) with the Kinetis PORT_SetPinMux the
        # check flags. RT1170 IOMUXC_SetPinMux takes model-variable tuple-macro
        # args, so the literal single-statement replace matched almost no model.
        "mutation": lambda code: re.sub(
            r"\bIOMUXC_SetPinMux\s*\([^;]*\);",
            "PORT_SetPinMux(PORTE, 3U, kPORT_MuxAsGpio);",
            code,
            count=1,
        ),
        "must_fail": ["no_kinetis_port_api"],
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
        "must_fail": ["header_fsl_gpio_h", "header_fsl_iomuxc_h"],
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
