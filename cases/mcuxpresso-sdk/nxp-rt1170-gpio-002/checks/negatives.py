"""Negative tests for nxp-rt1170-gpio-002 (button interrupt toggles LED).

Reference: cases/mcuxpresso-sdk/nxp-rt1170-gpio-002/reference/main.c
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
        "description": "IOMUXC_SetPinMux removed — pads stay on default function, button and LED dead",
        "mutation": lambda code: _remove_lines(code, "IOMUXC_SetPinMux"),
        "must_fail": ["iomuxc_before_gpio_init"],
    },
    {
        "name": "iomuxc_after_init",
        "description": "Pads muxed after GPIO_PinInit — init writes while pads are unrouted",
        "mutation": lambda code: (
            _remove_lines(code, "IOMUXC_SetPinMux")
            .replace(
                "GPIO_PinInit(LED_GPIO, LED_PIN, &led_config);",
                "GPIO_PinInit(LED_GPIO, LED_PIN, &led_config);\n"
                "    IOMUXC_SetPinMux(IOMUXC_WAKEUP_DIG_GPIO13_IO00, 0U);\n"
                "    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_04_GPIO9_IO03, 0U);",
            )
        ),
        "must_fail": ["iomuxc_before_gpio_init"],
    },
    {
        "name": "counter_not_volatile",
        "description": "volatile dropped from press counter — main may read a stale cached copy",
        "mutation": lambda code: code.replace(
            "static volatile uint32_t", "static uint32_t"
        ),
        "must_fail": ["volatile_press_counter"],
    },
    {
        "name": "missing_pin_unmask",
        "description": "GPIO_PortEnableInterrupts removed — edge configured but pin stays masked, ISR never fires",
        "mutation": lambda code: _remove_lines(code, "GPIO_PortEnableInterrupts("),
        "must_fail": ["gpio_port_interrupts_enabled"],
    },
    {
        "name": "missing_nvic_enable",
        "description": "EnableIRQ removed — GPIO interrupt pends but NVIC never dispatches it",
        "mutation": lambda code: _remove_lines(code, "EnableIRQ("),
        "must_fail": ["nvic_irq_enabled"],
    },
    {
        "name": "missing_flag_clear",
        "description": "Interrupt flag never cleared in ISR — handler re-enters forever",
        "mutation": lambda code: _remove_lines(code, "GPIO_PortClearInterruptFlags"),
        "must_fail": ["interrupt_flag_cleared"],
    },
    {
        "name": "wrong_edge",
        "description": "Rising edge configured — toggles on release instead of press",
        "mutation": lambda code: code.replace(
            "kGPIO_IntFallingEdge", "kGPIO_IntRisingEdge"
        ),
        "must_fail": ["falling_edge_configured"],
    },
    {
        "name": "isr_name_mismatch",
        "description": "Handler name does not match the vector table entry — default handler traps",
        "mutation": lambda code: code.replace(
            "GPIO13_Combined_0_31_IRQHandler(void)", "Button_Handler(void)"
        ),
        "must_fail": ["isr_handler_defined"],
    },
    {
        "name": "kinetis_port_mux",
        "description": "Kinetis PORT_SetPinMux used — wrong NXP family, does not exist on RT1170",
        "mutation": lambda code: code.replace(
            "IOMUXC_SetPinMux(IOMUXC_WAKEUP_DIG_GPIO13_IO00, 0U);",
            "PORT_SetPinMux(PORTA, 0U, kPORT_MuxAsGpio);",
        ),
        "must_fail": ["no_kinetis_port_api"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": ["header_fsl_gpio_h"],
    },
    {
        "name": "arduino_toggle",
        "description": "Arduino digitalWrite used instead of MCUXpresso GPIO API",
        "mutation": lambda code: code.replace(
            "GPIO_PortToggle(LED_GPIO, 1U << LED_PIN);",
            "digitalWrite(LED_PIN, !digitalRead(LED_PIN));",
        ),
        "must_fail": ["no_cross_platform_hallucination"],
    },
]
