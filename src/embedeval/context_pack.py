"""Context pack helpers for Context Quality Mode.

A "context pack" is a run-wide text payload (team's CLAUDE.md, expert pack,
or custom guidance) prepended to every LLM prompt. See
docs/CONTEXT-QUALITY-MODE.md for the full design.

This module owns three concerns:
- Resolving the user-supplied identifier to a real file path. The special
  value "expert" maps to the bundled pack at context_packs/expert.md.
- Hashing pack content so the tracker can refuse to mix incompatible runs.
  Hash uses raw bytes (not normalized text) so whitespace edits invalidate
  prior runs — that is intentional, a comma added to the pack is a different
  pack from the LLM's perspective.
- Length guard so accidentally pointing --context-pack at a multi-megabyte
  file fails loudly instead of silently exhausting the context window.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

# Soft limit. Above this we warn but proceed. The point is to catch the
# "user pointed --context-pack at the wrong file" case (e.g. a 2MB log),
# not to enforce token discipline — that's the user's call.
MAX_PACK_CHARS = 32_000

EXPERT_KEYWORD = "expert"

# Bundled packs addressable by keyword instead of a file path. The file lives
# next to this module under context_packs/. Add an entry to ship a new
# keyword-addressable pack.
_BUNDLED_PACKS = {
    "expert": "expert.md",
    "nxp": "nxp.md",
}


class ContextPackTooLargeError(ValueError):
    """Raised when a context pack exceeds MAX_PACK_CHARS."""


def bundled_expert_pack_path() -> Path:
    """Return the path to the bundled expert.md pack."""
    return Path(__file__).parent / "context_packs" / "expert.md"


def resolve_context_pack(identifier: str) -> Path:
    """Resolve a CLI --context-pack value to an actual file path.

    Args:
        identifier: Either a path to a context file, or a bundled-pack
            keyword ("expert", "nxp").

    Returns:
        Path to a readable .md/.txt file.

    Raises:
        FileNotFoundError: identifier is neither a known keyword nor an
            existing file.
    """
    if identifier in _BUNDLED_PACKS:
        path = Path(__file__).parent / "context_packs" / _BUNDLED_PACKS[identifier]
        if not path.is_file():
            raise FileNotFoundError(
                f"Bundled pack '{identifier}' missing at {path}. "
                f"Reinstall embedeval."
            )
        return path

    path = Path(identifier).expanduser()
    if not path.is_file():
        keywords = "', '".join(_BUNDLED_PACKS)
        raise FileNotFoundError(
            f"Context pack file not found: {path} "
            f"(or use a bundled keyword: '{keywords}')"
        )
    return path


def _hash_raw(content: str) -> str:
    """Compute the canonical 16-char SHA256 prefix without size checking.

    Single source of truth for the hash format. Called by hash_context_pack
    after the size guard, and directly by CLI when the size guard is
    intentionally bypassed (e.g. user accepted the oversized-pack warning).
    Keeping this in one place prevents the cli.py fallback from drifting
    out of sync with the canonical algorithm.
    """
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def hash_context_pack(content: str) -> str:
    """Return a 16-char SHA256 prefix of the pack content.

    16 chars (64 bits) is enough collision resistance for a tracker that
    holds at most a few dozen distinct packs across its lifetime, while
    staying short enough to read in tracker JSON.
    """
    if len(content) > MAX_PACK_CHARS:
        raise ContextPackTooLargeError(
            f"Context pack is {len(content)} chars, soft limit "
            f"{MAX_PACK_CHARS}. Excess content tends to dilute LLM attention."
        )
    return _hash_raw(content)
