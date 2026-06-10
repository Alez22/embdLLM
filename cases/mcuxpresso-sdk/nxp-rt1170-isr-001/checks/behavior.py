"""Behavioral checks for nxp-rt1170-isr-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded engineer must know. The core of this case: a 64-bit load on
a 32-bit Cortex-M core is two reads, so the accessor needs a critical
section, and the shared counter must be volatile.
"""

import re

from embedeval.check_utils import strip_comments
from embedeval.models import CheckDetail

_IRQ_DISABLE_RE = re.compile(
    r"\b(?:DisableGlobalIRQ|__disable_irq)\s*\("
)
_IRQ_RESTORE_RE = re.compile(
    r"\b(?:EnableGlobalIRQ|__enable_irq)\s*\("
)


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit ISR-concurrency knowledge for RT1170 uptime counter."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    # Uptime counter is shared between ISR and main: must be volatile.
    # Match the qualifier on a data declaration only — a bare \bvolatile\b
    # would also match __asm volatile("wfi") and comments.
    has_volatile = bool(re.search(
        r"\bvolatile\b\s+(?:uint|int|unsigned|bool|char|size_t)\w*", stripped
    ))
    details.append(CheckDetail(
        check_name="volatile_uptime_counter",
        passed=has_volatile,
        expected="volatile qualifier on the ISR-shared uptime counter",
        actual="present" if has_volatile else "missing",
        check_type="constraint",
    ))

    # 64-bit read tearing: the accessor must disable interrupts around the
    # read AND restore them afterwards (implicit — never stated in prompt)
    has_disable = bool(_IRQ_DISABLE_RE.search(stripped))
    has_restore = bool(_IRQ_RESTORE_RE.search(stripped))
    cs_ok = has_disable and has_restore
    details.append(CheckDetail(
        check_name="critical_section_around_read",
        passed=cs_ok,
        expected="interrupts disabled and restored around the 64-bit read",
        actual="present" if cs_ok else (
            "no IRQ disable" if not has_disable else "IRQs never re-enabled"
        ),
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
    has_start = bool(re.search(r"\bGPT_StartTimer\s*\(", stripped))
    details.append(CheckDetail(
        check_name="timer_started",
        passed=has_start,
        expected="GPT_StartTimer called",
        actual="present" if has_start else "missing",
        check_type="constraint",
    ))

    return details
