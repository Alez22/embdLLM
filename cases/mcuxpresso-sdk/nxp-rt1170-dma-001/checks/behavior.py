"""Behavioral checks for nxp-rt1170-dma-001.

L3: verifies implicit Cortex-M7 domain knowledge — the prompt never mentions
the D-cache, alignment, or volatile. A model that gets these right knows the
i.MX RT platform; a model that misses them produces code that "works" on a
cacheless core and corrupts data on the M7.

Cache strategy: explicit clean/invalidate OR non-cacheable buffers are both
accepted (dcache_tokens_found). Ordering checks auto-pass for the
non-cacheable strategy, where no maintenance is needed.
"""

import re

from embedeval.check_utils import strip_comments
from embedeval.check_utils_nxp import (
    DCACHE_CLEAN_APIS,
    DCACHE_INVALIDATE_APIS,
    dcache_tokens_found,
)
from embedeval.models import CheckDetail


def _first_pos(code: str, tokens: list[str]) -> int:
    """Position of the earliest occurrence of any token, or -1."""
    positions = [code.find(t) for t in tokens if t in code]
    return min(positions) if positions else -1


def _last_pos(code: str, tokens: list[str]) -> int:
    """Position of the latest occurrence of any token, or -1."""
    positions = [code.rfind(t) for t in tokens if t in code]
    return max(positions) if positions else -1


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit M7 cache/DMA knowledge for eDMA memory copy."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)
    cache = dcache_tokens_found(generated_code)
    start_pos = stripped.find("EDMA_StartTransfer")

    # D-cache coherency handled at all: maintenance calls or non-cacheable
    coherent = cache["noncacheable"] or (cache["clean"] and cache["invalidate"])
    details.append(CheckDetail(
        check_name="dcache_coherency_handled",
        passed=coherent,
        expected="cache clean+invalidate or AT_NONCACHEABLE_SECTION buffers",
        actual="handled" if coherent else "no cache strategy found — data corruption on M7",
        check_type="constraint",
    ))

    # Source cleaned to RAM before the DMA engine reads it
    if cache["noncacheable"]:
        clean_ok = True
        clean_actual = "non-cacheable buffers — maintenance not needed"
    else:
        clean_pos = _first_pos(stripped, DCACHE_CLEAN_APIS)
        clean_ok = clean_pos != -1 and (start_pos == -1 or clean_pos < start_pos)
        clean_actual = "correct order" if clean_ok else (
            "clean missing" if clean_pos == -1 else "clean after transfer start"
        )
    details.append(CheckDetail(
        check_name="dcache_clean_before_start",
        passed=clean_ok,
        expected="D-cache clean of source before EDMA_StartTransfer",
        actual=clean_actual,
        check_type="constraint",
    ))

    # Destination invalidated after the transfer, before CPU verification
    if cache["noncacheable"]:
        inval_ok = True
        inval_actual = "non-cacheable buffers — maintenance not needed"
    else:
        inval_pos = _last_pos(stripped, DCACHE_INVALIDATE_APIS)
        inval_ok = inval_pos != -1 and (start_pos == -1 or inval_pos > start_pos)
        inval_actual = "correct order" if inval_ok else (
            "invalidate missing" if inval_pos == -1 else "invalidate before transfer start"
        )
    details.append(CheckDetail(
        check_name="dcache_invalidate_after_transfer",
        passed=inval_ok,
        expected="D-cache invalidate of destination after the transfer completes",
        actual=inval_actual,
        check_type="constraint",
    ))

    # Buffers aligned to the 32-byte cache line (or non-cacheable section)
    has_alignment = bool(re.search(
        r"(SDK_ALIGN|__ALIGNED\s*\(\s*32|aligned\s*\(\s*32|"
        r"AT_NONCACHEABLE_SECTION)",
        stripped,
    ))
    details.append(CheckDetail(
        check_name="dma_buffers_cache_aligned",
        passed=has_alignment,
        expected="DMA buffers 32-byte aligned (M7 cache line) or non-cacheable",
        actual="present" if has_alignment else "missing — partial-line corruption risk",
        check_type="constraint",
    ))

    # If a completion callback is used, the done flag must be volatile.
    # A polling implementation (EDMA_GetChannelStatusFlags) needs neither.
    uses_callback = "EDMA_SetCallback" in stripped
    has_volatile = bool(re.search(
        r"\bvolatile\b\s+(?:uint|int|bool|char)\w*", stripped
    ))
    flag_ok = (not uses_callback) or has_volatile
    details.append(CheckDetail(
        check_name="done_flag_volatile",
        passed=flag_ok,
        expected="volatile completion flag when using the DMA callback",
        actual="ok" if flag_ok else "callback used but no volatile flag declaration",
        check_type="constraint",
    ))

    return details
