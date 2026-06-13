"""Behavioral checks for nxp-mcxc-watchdog-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention.
"""

import re

from embedeval.check_utils import scoped_contains
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit COP watchdog knowledge for MCXC144."""
    details: list[CheckDetail] = []

    # LPO clock source — independent of core clock, reliable for WDT
    has_lpo = scoped_contains(generated_code, "kCOP_LpoClock", scope="stripped")
    details.append(CheckDetail(
        check_name="lpo_clock_source_used",
        passed=has_lpo,
        expected="kCOP_LpoClock used (LPO independent of core clock)",
        actual="present" if has_lpo else "missing — using core clock is less reliable",
        check_type="constraint",
    ))

    # Longest timeout configured
    has_long_timeout = bool(re.search(
        r"kCOP_Timeout_2Power1[68]\w*", generated_code
    ))
    details.append(CheckDetail(
        check_name="long_timeout_configured",
        passed=has_long_timeout,
        expected="kCOP_Timeout_2Power16LpoClock or 2Power18 (longest available)",
        actual="present" if has_long_timeout else "missing or short timeout",
        check_type="constraint",
    ))

    # Watchdog NOT disabled (no cop_cfg.enableCop = false)
    wdt_disabled = bool(re.search(
        r"\.enableCop\s*=\s*false", generated_code
    ))
    details.append(CheckDetail(
        check_name="watchdog_not_disabled",
        passed=not wdt_disabled,
        expected="Watchdog not disabled (prompt explicitly forbids this)",
        actual="ok" if not wdt_disabled else "watchdog disabled — defeats purpose",
        check_type="constraint",
    ))

    # COP_Refresh inside the main loop (not before the loop). Accept every
    # idiomatic infinite-loop form: while(1) / while(1U) / while(true) / for(;;).
    loop_match = re.search(
        r"\b(?:while\s*\(\s*(?:1[Uu]?|true)\s*\)|for\s*\(\s*;\s*;\s*\))\s*\{(.*)\}",
        generated_code,
        re.DOTALL,
    )
    refresh_in_loop = bool(loop_match and "COP_Refresh" in loop_match.group(1))
    details.append(CheckDetail(
        check_name="cop_refresh_inside_main_loop",
        passed=refresh_in_loop,
        expected="COP_Refresh called inside while(1) loop body",
        actual="correct" if refresh_in_loop else "COP_Refresh outside loop or loop not found",
        check_type="constraint",
    ))

    return details
