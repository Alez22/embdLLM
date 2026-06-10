"""Negative tests for nxp-rt1170-isr-001 (64-bit uptime counter).

Reference: cases/mcuxpresso-sdk/nxp-rt1170-isr-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic ISR-concurrency bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


NEGATIVES = [
    {
        "name": "torn_64bit_read",
        "description": "Critical section removed — ISR can fire between the two 32-bit halves of the read",
        "mutation": lambda code: (
            _remove_lines(code, "DisableGlobalIRQ")
            .replace("    EnableGlobalIRQ(primask);\n", "")
        ),
        "must_fail": ["critical_section_around_read"],
    },
    {
        "name": "irqs_never_restored",
        "description": "EnableGlobalIRQ dropped — first uptime read disables interrupts forever",
        "mutation": lambda code: code.replace(
            "    EnableGlobalIRQ(primask);\n", ""
        ),
        "must_fail": ["critical_section_around_read"],
    },
    {
        "name": "counter_not_volatile",
        "description": "volatile dropped from uptime counter — main may read a stale cached copy",
        "mutation": lambda code: code.replace(
            "static volatile uint64_t", "static uint64_t"
        ),
        "must_fail": ["volatile_uptime_counter"],
    },
    {
        "name": "missing_nvic_enable",
        "description": "EnableIRQ removed — GPT interrupt pends but NVIC never dispatches it",
        "mutation": lambda code: _remove_lines(code, "EnableIRQ(UPTIME_GPT_IRQ)"),
        "must_fail": ["nvic_irq_enabled"],
    },
    {
        "name": "timer_never_started",
        "description": "GPT_StartTimer removed — uptime stays at zero forever",
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
        "name": "isr_name_mismatch",
        "description": "Handler name does not match the vector table entry — default handler traps",
        "mutation": lambda code: code.replace(
            "GPT2_IRQHandler(void)", "Uptime_Handler(void)"
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
        "name": "zephyr_uptime",
        "description": "Zephyr k_uptime_get used instead of a bare-metal counter",
        "mutation": lambda code: code.replace(
            "uint64_t now = g_uptime_ms;",
            "uint64_t now = k_uptime_get();",
        ),
        "must_fail": ["no_cross_platform_hallucination"],
    },
]
