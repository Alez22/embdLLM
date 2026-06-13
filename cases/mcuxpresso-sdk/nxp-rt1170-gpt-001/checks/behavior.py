"""Behavioral checks for nxp-rt1170-gpt-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded engineer targeting i.MX RT1170 must know.
"""

import re

from embedeval.check_utils_nxp import has_rt1170_clock_root_config
from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit MCUXpresso SDK knowledge for RT1170 GPT tick."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    # Clock root configured — single-file program has no BOARD_BootClockRUN,
    # the GPT root must be set explicitly (implicit)
    has_clock_root = has_rt1170_clock_root_config(generated_code)
    details.append(CheckDetail(
        check_name="clock_root_configured",
        passed=has_clock_root,
        expected="CLOCK_SetRootClock called for the GPT clock root",
        actual="present" if has_clock_root else "missing",
        check_type="constraint",
    ))

    # Period must come from a compare value — without it the timer free-runs
    has_compare = scoped_contains(
        generated_code, "GPT_SetOutputCompareValue", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="compare_value_set",
        passed=has_compare,
        expected="GPT_SetOutputCompareValue sets the 1 ms period",
        actual="present" if has_compare else "missing",
        check_type="constraint",
    ))

    # Interrupt enable at the peripheral (compare channel) — implicit
    has_periph_irq = scoped_contains(
        generated_code, "GPT_EnableInterrupts", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="peripheral_interrupt_enabled",
        passed=has_periph_irq,
        expected="GPT_EnableInterrupts unmasks the compare interrupt",
        actual="present" if has_periph_irq else "missing",
        check_type="constraint",
    ))

    # NVIC-level enable — without it the interrupt pends but never fires
    has_nvic = bool(re.search(r"\b(?:NVIC_)?EnableIRQ\s*\(", stripped))
    details.append(CheckDetail(
        check_name="nvic_irq_enabled",
        passed=has_nvic,
        expected="EnableIRQ called for the GPT IRQ line",
        actual="present" if has_nvic else "missing",
        check_type="constraint",
    ))

    # Timer must actually be started (easy to forget after configuring)
    has_start = scoped_contains(
        generated_code, "GPT_StartTimer", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="timer_started",
        passed=has_start,
        expected="GPT_StartTimer called",
        actual="present" if has_start else "missing",
        check_type="constraint",
    ))

    # Tick counter is shared between ISR and main: must be volatile.
    # Match the qualifier on a data declaration only — a bare \bvolatile\b
    # would also match __asm volatile("wfi") and comments.
    has_volatile = bool(re.search(
        r"\bvolatile\b\s+(?:uint|int|unsigned|bool|char|size_t)\w*", stripped
    ))
    details.append(CheckDetail(
        check_name="volatile_tick_counter",
        passed=has_volatile,
        expected="volatile qualifier on the ISR-shared tick counter",
        actual="present" if has_volatile else "missing",
        check_type="constraint",
    ))

    return details
