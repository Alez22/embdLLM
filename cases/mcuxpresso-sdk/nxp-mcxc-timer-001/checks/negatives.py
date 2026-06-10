"""Negative tests for nxp-mcxc-timer-001 (periodic PIT interrupt).

Reference: cases/mcuxpresso-sdk/nxp-mcxc-timer-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic MCXC144 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""

_PERIOD_BLOCK = (
    "    PIT_SetTimerPeriod(PIT, PIT_CH,\n"
    "        USEC_TO_COUNT(PIT_PERIOD_MS * 1000U, BUS_CLK_HZ));\n"
)


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


NEGATIVES = [
    {
        "name": "missing_clock_gates",
        "description": "CLOCK_EnableClock removed — PIT/PORT/UART access bus-faults",
        "mutation": lambda code: _remove_lines(code, "CLOCK_EnableClock"),
        "must_fail": ["clock_gate_before_pit_init"],
    },
    {
        "name": "missing_nvic_enable",
        "description": "EnableIRQ removed — PIT interrupt pends but never fires",
        "mutation": lambda code: _remove_lines(code, "EnableIRQ"),
        "must_fail": ["nvic_pit_interrupt_enabled"],
    },
    {
        "name": "missing_pit_enable_interrupts",
        "description": "PIT_EnableInterrupts removed — timer counts but never interrupts",
        "mutation": lambda code: _remove_lines(code, "PIT_EnableInterrupts"),
        "must_fail": ["pit_interrupts_enabled"],
    },
    {
        "name": "nonvolatile_counter",
        "description": "volatile dropped from ISR-shared tick counter — main may spin on a stale copy",
        "mutation": lambda code: code.replace(
            "static volatile uint32_t g_tick_count",
            "static uint32_t g_tick_count",
        ),
        "must_fail": ["isr_counter_volatile"],
    },
    {
        "name": "pit_flag_not_cleared",
        "description": "PIT flag never cleared — ISR re-enters forever, main starves",
        "mutation": lambda code: _remove_lines(code, "PIT_ClearStatusFlags"),
        "must_fail": ["pit_flag_cleared_in_isr"],
    },
    {
        "name": "timer_never_started",
        "description": "PIT_StartTimer removed — timer configured but never runs",
        "mutation": lambda code: _remove_lines(code, "PIT_StartTimer"),
        "must_fail": ["pit_timer_started"],
    },
    {
        "name": "missing_period",
        "description": "PIT_SetTimerPeriod removed — timer runs with reset-default period",
        "mutation": lambda code: code.replace(_PERIOD_BLOCK, ""),
        "must_fail": ["pit_period_set"],
    },
    {
        "name": "isr_not_vector_named",
        "description": "Handler renamed — no longer matches the vector table entry, never called",
        "mutation": lambda code: code.replace("PIT_IRQHandler", "timer_tick_handler"),
        "must_fail": ["pit_isr_defined", "pit_flag_cleared_in_isr"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": ["header_fsl_pit_h", "header_fsl_clock_h"],
    },
    {
        "name": "stm32_timer_init",
        "description": "STM32 HAL_TIM_Base_Init used instead of MCUXpresso PIT API",
        "mutation": lambda code: code.replace(
            "PIT_Init(PIT, &pit_cfg);",
            "HAL_TIM_Base_Init(&htim2);",
        ),
        "must_fail": ["pit_init_called", "no_cross_platform_hallucination"],
    },
]
