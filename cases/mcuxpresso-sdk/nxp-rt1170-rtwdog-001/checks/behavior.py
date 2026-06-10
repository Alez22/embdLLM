"""Behavioral checks for nxp-rt1170-rtwdog-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded engineer targeting i.MX RT1170 must know.
"""

import re

from embedeval.check_utils import strip_comments
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit RTWDOG knowledge for RT1170."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    # Timeout explicitly configured — default config value is not 1 s
    has_timeout = bool(re.search(r"\btimeoutValue\s*=", stripped))
    details.append(CheckDetail(
        check_name="timeout_configured",
        passed=has_timeout,
        expected="timeoutValue set for a 1 s period",
        actual="present" if has_timeout else "missing",
        check_type="constraint",
    ))

    # Watchdog NOT disabled (prompt explicitly forbids this)
    wdt_disabled = bool(re.search(r"\benableRtwdog\s*=\s*false\b", stripped))
    details.append(CheckDetail(
        check_name="watchdog_not_disabled",
        passed=not wdt_disabled,
        expected="Watchdog left enabled",
        actual="ok" if not wdt_disabled else "watchdog disabled — defeats purpose",
        check_type="constraint",
    ))

    # RTWDOG_Refresh inside the main loop, not just once before it —
    # feeding outside the loop only delays the first reset
    loop_match = re.search(
        r"\bwhile\s*\(\s*1\s*\)\s*\{(.*)\}", stripped, re.DOTALL
    )
    refresh_in_loop = bool(loop_match and "RTWDOG_Refresh" in loop_match.group(1))
    details.append(CheckDetail(
        check_name="refresh_inside_main_loop",
        passed=refresh_in_loop,
        expected="RTWDOG_Refresh called inside the while(1) loop body",
        actual="correct" if refresh_in_loop else (
            "RTWDOG_Refresh outside loop or loop not found"
        ),
        check_type="constraint",
    ))

    # No Kinetis COP/WDOG API — RT1170 uses RTWDOG. \b stops a match inside
    # RTWDOG_* (no word boundary between 'T' and 'W').
    has_legacy = bool(re.search(r"\b(?:COP_|WDOG_)\w+\s*\(", stripped))
    details.append(CheckDetail(
        check_name="no_legacy_kinetis_wdog_api",
        passed=not has_legacy,
        expected="RTWDOG_* API used, not Kinetis COP_/WDOG_*",
        actual="clean" if not has_legacy else "Kinetis COP/WDOG API found",
        check_type="constraint",
    ))

    return details
