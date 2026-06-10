"""Negative tests for nxp-rt1170-dma-001 (eDMA copy with cache coherency).

Reference: cases/mcuxpresso-sdk/nxp-rt1170-dma-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic Cortex-M7 DMA bug into the reference and
asserts the corresponding L0/L3 check detects it. The cache mutations are
the important ones: they are exactly the bugs that work on an M0+/M4
without cache and corrupt data on the M7.
"""


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


NEGATIVES = [
    {
        "name": "no_cache_clean",
        "description": "Source never cleaned to RAM — DMA reads stale memory, not the CPU-written pattern",
        "mutation": lambda code: (
            _remove_lines(
                _remove_lines(code, "SCB_CleanDCache_by_Addr"),
                "SCB_CleanInvalidateDCache_by_Addr",
            )
        ),
        "must_fail": ["dcache_clean_before_start"],
    },
    {
        "name": "no_invalidate_after",
        "description": "Destination not invalidated after DMA — CPU verifies stale cache lines",
        "mutation": lambda code: _remove_lines(code, "SCB_InvalidateDCache_by_Addr"),
        "must_fail": ["dcache_invalidate_after_transfer"],
    },
    {
        "name": "no_cache_handling_at_all",
        "description": "All cache maintenance removed — classic 'works on M4, fails on M7' bug",
        "mutation": lambda code: (
            _remove_lines(
                _remove_lines(
                    _remove_lines(code, "SCB_CleanDCache_by_Addr"),
                    "SCB_CleanInvalidateDCache_by_Addr",
                ),
                "SCB_InvalidateDCache_by_Addr",
            )
        ),
        "must_fail": [
            "dcache_coherency_handled",
            "dcache_clean_before_start",
            "dcache_invalidate_after_transfer",
        ],
    },
    {
        "name": "unaligned_buffers",
        "description": "Buffers not aligned to the 32-byte cache line — neighbours corrupted by maintenance ops",
        "mutation": lambda code: (
            code
            .replace(
                "SDK_ALIGN(static uint8_t s_src[BUF_SIZE], 32U);",
                "static uint8_t s_src[BUF_SIZE];",
            )
            .replace(
                "SDK_ALIGN(static uint8_t s_dst[BUF_SIZE], 32U);",
                "static uint8_t s_dst[BUF_SIZE];",
            )
        ),
        "must_fail": ["dma_buffers_cache_aligned"],
    },
    {
        "name": "nonvolatile_done_flag",
        "description": "volatile dropped from the completion flag — main may spin forever on a cached copy",
        "mutation": lambda code: code.replace(
            "static volatile bool s_transfer_done = false;",
            "static bool s_transfer_done = false;",
        ),
        "must_fail": ["done_flag_volatile"],
    },
    {
        "name": "missing_edma_init",
        "description": "EDMA_Init removed — module configuration never applied",
        "mutation": lambda code: _remove_lines(code, "EDMA_Init(DMA0"),
        "must_fail": ["edma_init_called"],
    },
    {
        "name": "missing_edma_header",
        "description": "fsl_edma.h include removed — relies on transitive includes",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_edma.h"'),
        "must_fail": ["header_fsl_edma_h"],
    },
    {
        "name": "stm32_hal_dma",
        "description": "STM32 HAL_DMA_Start used instead of MCUXpresso eDMA API",
        "mutation": lambda code: code.replace(
            "EDMA_StartTransfer(&s_dma_handle);",
            "HAL_DMA_Start(&hdma, (uint32_t)s_src, (uint32_t)s_dst, BUF_SIZE);",
        ),
        "must_fail": ["edma_transfer_started", "no_cross_platform_hallucination"],
    },
]
