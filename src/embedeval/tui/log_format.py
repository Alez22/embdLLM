"""Formatting/filtering of runner log lines for the TUI log panel."""
from __future__ import annotations

import re as _re

_CASE_RESULT_RE = _re.compile(
    r"Case (\S+) attempt (\d+): (PASS|FAIL@L(\S+)|FAIL)(?: \[src=(\S+)\])?"
)
_CASE_UNHANDLED_RE = _re.compile(r"Case (\S+) attempt (\d+): unhandled (\S+)")

# Human-readable provenance shown next to each result, derived from the
# EvalResult.cache_source tag the runner appends as "[src=...]".
_SRC_LABEL = {
    "llm": "fresh: LLM gen + graded",
    "grade-cache": "LLM gen, grade from cache",
    "gen-cache": "gen from cache, re-graded",
    "gen+grade-cache": "gen + grade from cache",
}


def _format_log_line(line: str) -> str | None:
    """Return a human-readable widget line, or None to suppress the line.

    The full raw output is always written to the log file; this function
    controls what appears in the TUI log panel.
    """
    # Launch and done markers.
    if line.startswith("[launch]") or line.startswith("[done]"):
        return line

    # Infrastructure error: unhandled exception in runner (API failure, timeout, etc.)
    u = _CASE_UNHANDLED_RE.search(line)
    if u:
        return f"[ERROR] {u.group(1)} #{u.group(2)}  ({u.group(3)})"

    # Per-attempt result: reformat into a compact, aligned line.
    m = _CASE_RESULT_RE.search(line)
    if m:
        case_id, attempt, status = m.group(1), m.group(2), m.group(3)
        src = m.group(5)
        src_note = f"  ({_SRC_LABEL.get(src, src)})" if src else ""
        if status == "PASS":
            return f"[ PASS ] {case_id} #{attempt}{src_note}"
        layer = m.group(4) or "?"
        return f"[ FAIL ] {case_id} #{attempt}  →  L{layer}{src_note}"

    # Rate-limit warnings worth surfacing.
    low = line.lower()
    if "rate limit" in low or "ratelimiterror" in low:
        return f"[warn ] rate limit — {line.strip()}"

    # Prose response warning: model returned text instead of code.
    if "returned prose" in low:
        # Strip log prefix (e.g. "WARNING:embedeval.llm_client:LLM ...")
        msg = _re.sub(r"^[A-Z]+:[^:]+:", "", line).strip()
        return f"[warn ] {msg}"

    return None
