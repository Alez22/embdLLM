"""Negative tests for nxp-mcxc-isr-001 (ISR-to-main data transfer).

Reference: cases/mcuxpresso-sdk/nxp-mcxc-isr-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic MCXC144 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.

Note on flag_cleared_after_consume: the ready_flag_cleared_before_consuming
regex also matches the variable *initializers* ("g_sample_ready = false;",
"g_sample_value = 0U;" followed by another shared-var name). The mutation
therefore strips the initializers as well — otherwise the declarations alone
satisfy the check regardless of the main-loop ordering. See review notes:
the check itself should be tightened.
"""

import re

_CONSUME_BLOCK = (
    "        if (g_sample_ready) {\n"
    "            /* Clear flag before reading value to avoid missing the next sample */\n"
    "            g_sample_ready = false;\n"
    "            if (g_sample_value) {\n"
    "                GPIO_PortToggle(LED_GPIO, 1U << LED_PIN);\n"
    "            }\n"
    "        }\n"
)

_CONSUME_BLOCK_REORDERED = (
    "        if (g_sample_ready) {\n"
    "            if (g_sample_value) {\n"
    "                GPIO_PortToggle(LED_GPIO, 1U << LED_PIN);\n"
    "            }\n"
    "            g_sample_ready = false;\n"
    "        }\n"
)


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


NEGATIVES = [
    {
        "name": "missing_clock_gates",
        "description": "CLOCK_EnableClock removed — PORT/GPIO/PIT access bus-faults",
        "mutation": lambda code: _remove_lines(code, "CLOCK_EnableClock"),
        "must_fail": ["clock_gate_before_gpio_init"],
    },
    {
        "name": "missing_nvic_enable",
        "description": "EnableIRQ removed — PIT interrupt pends but never fires",
        "mutation": lambda code: _remove_lines(code, "EnableIRQ"),
        "must_fail": ["nvic_pit_enabled"],
    },
    {
        "name": "pit_flag_not_cleared",
        "description": "PIT flag never cleared — ISR re-enters forever, main starves",
        "mutation": lambda code: _remove_lines(code, "PIT_ClearStatusFlags"),
        "must_fail": ["pit_flag_cleared_in_isr"],
    },
    {
        "name": "value_not_volatile",
        "description": "volatile dropped from shared value — main may read a stale register copy",
        # Drop volatile from a SINGLE shared declaration, leaving the other
        # volatile — distinct from no_volatile_at_all which strips both.
        # both_shared_vars_volatile requires >=2 volatile-typed decls; removing
        # one leaves <2. Match volatile only when immediately followed by a type
        # keyword (a declaration), so the word "volatile" in a comment is not
        # what gets stripped.
        "mutation": lambda code: re.sub(
            r"\bvolatile\s+(?=(?:unsigned\s+)?(?:uint|int|bool|char|float|double|struct)\w*)",
            "", code, count=1,
        ),
        "must_fail": ["both_shared_vars_volatile"],
    },
    {
        "name": "no_volatile_at_all",
        "description": "volatile dropped from both shared variables — main loop may never see updates",
        # Strip every 'volatile' qualifier regardless of the underlying type.
        # Literal replaces (e.g. "static volatile bool") missed models that
        # declared the flag with another type such as uint8_t, leaving a
        # residual 'volatile' that satisfied the generic volatile_shared_data
        # check and masked the mutation. The regex preserves 'static'.
        "mutation": lambda code: re.sub(r"\bvolatile\s+", "", code),
        "must_fail": ["both_shared_vars_volatile", "volatile_shared_data"],
    },
    {
        "name": "flag_cleared_after_consume",
        "description": "Ready flag cleared after reading value — sample arriving in between is lost",
        "mutation": lambda code: (
            code
            .replace(_CONSUME_BLOCK, _CONSUME_BLOCK_REORDERED)
            # Strip initializers: they alone satisfy the check regex (see
            # module docstring) and would mask the reordering bug.
            .replace(
                "static volatile bool     g_sample_ready = false;",
                "static volatile bool     g_sample_ready;",
            )
            .replace(
                "static volatile uint32_t g_sample_value = 0U;",
                "static volatile uint32_t g_sample_value;",
            )
        ),
        "must_fail": ["ready_flag_cleared_before_consuming"],
    },
    {
        "name": "hardcoded_input_value",
        "description": "GPIO_PinRead replaced with a constant — input never actually sampled",
        # Replace any GPIO_PinRead(...) with a constant; gpio_pin_read_in_code
        # flags the absence of GPIO_PinRead. The literal replace assumed the
        # exact args (INPUT_GPIO, INPUT_PIN).
        "mutation": lambda code: re.sub(
            r"\bGPIO_PinRead\s*\([^;)]*\)", "1U", code
        ),
        "must_fail": ["gpio_pin_read_in_code"],
    },
    {
        "name": "isr_not_vector_named",
        "description": "Handler renamed — no longer matches the vector table entry, never called",
        "mutation": lambda code: code.replace("PIT_IRQHandler", "pit_callback"),
        "must_fail": ["pit_isr_defined", "pit_flag_cleared_in_isr"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": ["header_fsl_pit_h", "header_fsl_gpio_h", "header_fsl_clock_h"],
    },
    {
        "name": "arduino_toggle",
        "description": "Arduino digitalWrite used instead of MCUXpresso GPIO API",
        # Inject an Arduino digitalWrite by replacing whichever GPIO output
        # toggle/write call the model used. If the solution drives no GPIO
        # output (this case centres on input sampling), there is nothing to
        # replace and the mutation legitimately no-ops.
        "mutation": lambda code: re.sub(
            r"\bGPIO_(?:PortToggle\w*|TogglePinsOutput|PinToggle|TogglePin|PinWrite)\s*\([^;]*\);",
            "digitalWrite(24, HIGH);",
            code,
            count=1,
        ),
        "must_fail": ["no_cross_platform_hallucination"],
    },
]
