"""Negative tests for nxp-rt1170-gpt-001 (GPT millisecond tick).

Reference: cases/mcuxpresso-sdk/nxp-rt1170-gpt-001/reference/main.c
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
        "name": "missing_clock_root",
        "description": "CLOCK_SetRootClock removed — GPT root left at reset state, tick period wrong",
        "mutation": lambda code: _remove_lines(code, "CLOCK_SetRootClock("),
        "must_fail": ["clock_root_configured"],
    },
    {
        "name": "missing_compare_value",
        "description": "GPT_SetOutputCompareValue removed — timer free-runs, no periodic match",
        "mutation": lambda code: code.replace(
            "    GPT_SetOutputCompareValue(TICK_GPT, kGPT_OutputCompare_Channel1,\n"
            "                              (TICK_GPT_FREQ / 1000U) - 1U);\n",
            "",
        ),
        "must_fail": ["compare_value_set"],
    },
    {
        "name": "missing_peripheral_irq_enable",
        "description": "GPT_EnableInterrupts removed — compare matches but interrupt stays masked",
        "mutation": lambda code: _remove_lines(code, "GPT_EnableInterrupts("),
        "must_fail": ["peripheral_interrupt_enabled"],
    },
    {
        "name": "missing_nvic_enable",
        "description": "EnableIRQ removed — GPT interrupt pends but NVIC never dispatches it",
        "mutation": lambda code: _remove_lines(code, "EnableIRQ("),
        "must_fail": ["nvic_irq_enabled"],
    },
    {
        "name": "timer_never_started",
        "description": "GPT_StartTimer removed — timer fully configured but never counts",
        "mutation": lambda code: _remove_lines(code, "GPT_StartTimer("),
        "must_fail": ["timer_started"],
    },
    {
        "name": "missing_flag_clear",
        "description": "Compare flag never cleared in ISR — handler re-enters forever",
        "mutation": lambda code: _remove_lines(code, "GPT_ClearStatusFlags"),
        "must_fail": ["interrupt_flag_cleared"],
    },
    {
        "name": "counter_not_volatile",
        "description": "volatile dropped from tick counter — main may read a stale cached copy",
        # Strip every 'volatile' qualifier regardless of type. The literal
        # "static volatile uint32_t" missed models that used a different type;
        # volatile_tick_counter matches any 'volatile <type>'.
        "mutation": lambda code: re.sub(r"\bvolatile\s+", "", code),
        "must_fail": ["volatile_tick_counter"],
    },
    {
        "name": "isr_name_mismatch",
        "description": "Handler name does not match the vector table entry — default handler traps",
        "mutation": lambda code: code.replace(
            "GPT1_IRQHandler(void)", "Tick_Handler(void)"
        ),
        "must_fail": ["isr_handler_defined"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": ["header_fsl_gpt_h"],
    },
    {
        "name": "freertos_delay",
        "description": "FreeRTOS vTaskDelay used in a bare-metal main loop",
        # Inject FreeRTOS vTaskDelay in place of whichever wait-for-interrupt
        # idle the model used: __WFI() or an inline-asm wfi. Most models write
        # __WFI(), which the single literal replace missed.
        "mutation": lambda code: re.sub(
            r'\b__WFI\s*\(\s*\)\s*;|__asm\b[^;]*\bwfi\b[^;]*;',
            "vTaskDelay(1);",
            code,
            count=1,
        ),
        "must_fail": ["no_cross_platform_hallucination"],
    },
]
