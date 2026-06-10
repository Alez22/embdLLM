"""Negative tests for nxp-mcxc-watchdog-001 (COP watchdog init + feed).

Reference: cases/mcuxpresso-sdk/nxp-mcxc-watchdog-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic MCXC144 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""

_MAIN_LOOP = (
    "    while (1) {\n"
    "        do_work();\n"
    "\n"
    "        /* Feed watchdog — must be done within the timeout window */\n"
    "        COP_Refresh(SIM);\n"
    "    }\n"
)

_MAIN_LOOP_REFRESH_OUTSIDE = (
    "    COP_Refresh(SIM);\n"
    "\n"
    "    while (1) {\n"
    "        do_work();\n"
    "    }\n"
)


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


NEGATIVES = [
    {
        "name": "bus_clock_source",
        "description": "COP clocked from bus clock — dies with the core clock it should supervise",
        "mutation": lambda code: code.replace("kCOP_LpoClock", "kCOP_BusClock"),
        "must_fail": ["lpo_clock_source_used"],
    },
    {
        "name": "short_timeout",
        "description": "Short COP timeout — main loop work exceeds the window, spurious resets",
        "mutation": lambda code: code.replace(
            "kCOP_Timeout_2Power18LpoClock", "kCOP_Timeout_2Power5LpoClock"
        ),
        "must_fail": ["long_timeout_configured"],
    },
    {
        "name": "watchdog_disabled",
        "description": "enableCop = false — watchdog silently disabled, defeats the purpose",
        "mutation": lambda code: code.replace(
            "cop_cfg.enableCop      = true;",
            "cop_cfg.enableCop      = false;",
        ),
        "must_fail": ["watchdog_not_disabled"],
    },
    {
        "name": "refresh_outside_loop",
        "description": "COP_Refresh moved before the loop — fed once, then resets at first timeout",
        "mutation": lambda code: code.replace(_MAIN_LOOP, _MAIN_LOOP_REFRESH_OUTSIDE),
        "must_fail": ["cop_refresh_inside_main_loop"],
    },
    {
        "name": "refresh_missing",
        "description": "COP_Refresh removed entirely — device resets at every timeout",
        "mutation": lambda code: _remove_lines(code, "COP_Refresh"),
        "must_fail": ["cop_refresh_called", "cop_refresh_inside_main_loop"],
    },
    {
        "name": "missing_cop_header",
        "description": "fsl_cop.h include removed — relies on transitive includes",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_cop.h"'),
        "must_fail": ["header_fsl_cop_h"],
    },
    {
        "name": "stm32_iwdg",
        "description": "STM32 HAL_IWDG_Init used instead of MCUXpresso COP API",
        "mutation": lambda code: code.replace(
            "COP_Init(SIM, &cop_cfg);",
            "HAL_IWDG_Init(&hiwdg);",
        ),
        "must_fail": ["cop_init_called", "no_cross_platform_hallucination"],
    },
]
