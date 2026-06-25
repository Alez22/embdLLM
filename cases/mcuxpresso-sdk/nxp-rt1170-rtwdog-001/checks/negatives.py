"""Negative tests for nxp-rt1170-rtwdog-001 (RTWDOG setup and feed).

Reference: cases/mcuxpresso-sdk/nxp-rt1170-rtwdog-001/reference/main.c
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
        "name": "refresh_before_loop_only",
        "description": "Watchdog fed once before the loop — first timeout resets the device anyway",
        "mutation": lambda code: code.replace(
            "    while (1) {\n"
            "        work_counter++;\n"
            "        /* Feed last, after the work: a stall anywhere above starves it */\n"
            "        RTWDOG_Refresh(WDT_BASE);\n"
            "    }\n",
            "    RTWDOG_Refresh(WDT_BASE);\n\n"
            "    while (1) {\n"
            "        work_counter++;\n"
            "    }\n",
        ),
        "must_fail": ["refresh_inside_main_loop"],
    },
    {
        "name": "refresh_missing",
        "description": "RTWDOG_Refresh removed entirely — device resets every second",
        "mutation": lambda code: _remove_lines(code, "RTWDOG_Refresh"),
        "must_fail": ["rtwdog_refresh_used", "refresh_inside_main_loop"],
    },
    {
        "name": "watchdog_disabled",
        "description": "enableRtwdog forced false — watchdog never armed, prompt forbids this",
        # Force the config's enableRtwdog field false right after
        # RTWDOG_GetDefaultConfig(&<cfg>), capturing whatever name the model
        # gave the config struct (config / rtwdogConfig / wdogConfig / cfg /...).
        # watchdog_not_disabled flags 'enableRtwdog = false'. The literal replace
        # assumed a 'config.timeoutValue = ...' line spelled exactly.
        "mutation": lambda code: re.sub(
            r"(RTWDOG\d*_GetDefaultConfig\s*\(\s*&\s*(\w+)\s*\)\s*;)",
            r"\1\n    \2.enableRtwdog = false;",
            code,
            count=1,
        ),
        "must_fail": ["watchdog_not_disabled"],
    },
    {
        "name": "timeout_left_default",
        "description": "timeoutValue not set — default period, not the requested 1 s",
        "mutation": lambda code: _remove_lines(code, "config.timeoutValue"),
        "must_fail": ["timeout_configured"],
    },
    {
        "name": "kinetis_wdog_api",
        "description": "Kinetis WDOG API used — wrong NXP family, RT1170 has RTWDOG",
        # Demote any RTWDOG_Refresh(...) to the Kinetis WDOG_Refresh spelling,
        # regardless of base/args.
        "mutation": lambda code: re.sub(
            r"\bRTWDOG_Refresh\s*\([^;]*\);", "WDOG_Refresh(WDOG);", code
        ),
        "must_fail": ["no_legacy_kinetis_wdog_api"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": ["header_fsl_rtwdog_h"],
    },
    {
        "name": "stm32_iwdg",
        "description": "STM32 HAL IWDG call used instead of MCUXpresso RTWDOG API",
        # Replace any RTWDOG_Refresh(...) with the STM32 HAL refresh, regardless
        # of base/args.
        "mutation": lambda code: re.sub(
            r"\bRTWDOG_Refresh\s*\([^;]*\);", "HAL_IWDG_Refresh(&hiwdg);", code
        ),
        "must_fail": ["no_cross_platform_hallucination"],
    },
]
