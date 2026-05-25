"""Static checks for nxp-mcxc-timer-001.

L0: pattern matching on generated source text, no compilation needed.
"""

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate MCXC144 PIT timer code structure."""
    details: list[CheckDetail] = []

    for header in ("fsl_pit.h", "fsl_clock.h"):
        present = scoped_contains(generated_code, header, scope="code_only")
        details.append(CheckDetail(
            check_name=f"header_{header.replace('.', '_')}",
            passed=present,
            expected=f"{header} included",
            actual="present" if present else "missing",
            check_type="exact_match",
        ))

    has_init = scoped_contains(generated_code, "PIT_Init", scope="stripped")
    details.append(CheckDetail(
        check_name="pit_init_called",
        passed=has_init,
        expected="PIT_Init called",
        actual="present" if has_init else "missing",
        check_type="exact_match",
    ))

    has_period = scoped_contains(generated_code, "PIT_SetTimerPeriod", scope="stripped")
    details.append(CheckDetail(
        check_name="pit_period_set",
        passed=has_period,
        expected="PIT_SetTimerPeriod called",
        actual="present" if has_period else "missing",
        check_type="exact_match",
    ))

    has_start = scoped_contains(generated_code, "PIT_StartTimer", scope="stripped")
    details.append(CheckDetail(
        check_name="pit_timer_started",
        passed=has_start,
        expected="PIT_StartTimer called",
        actual="present" if has_start else "missing",
        check_type="exact_match",
    ))

    import re
    has_isr = bool(re.search(r"\bPIT_IRQHandler\s*\(", generated_code))
    details.append(CheckDetail(
        check_name="pit_isr_defined",
        passed=has_isr,
        expected="PIT_IRQHandler defined",
        actual="present" if has_isr else "missing",
        check_type="exact_match",
    ))

    foreign = no_nxp_hallucination(generated_code)
    details.append(CheckDetail(
        check_name="no_cross_platform_hallucination",
        passed=len(foreign) == 0,
        expected="Only NXP MCUXpresso SDK APIs used",
        actual="clean" if not foreign else f"found: {foreign}",
        check_type="constraint",
    ))

    return details
