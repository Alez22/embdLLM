"""Negative tests for nxp-rt1170-audio-001 (full-duplex audio pass-through).

Reference: cases/mcuxpresso-sdk/nxp-rt1170-audio-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic RT1170 audio bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""

import re


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


NEGATIVES = [
    {
        "name": "missing_iomuxc_mux",
        "description": "IOMUXC_SetPinMux removed — SAI pads stay on default function, no audio",
        "mutation": lambda code: _remove_lines(code, "IOMUXC_SetPinMux"),
        "must_fail": ["iomuxc_before_sai_init"],
    },
    {
        "name": "missing_clock_root",
        "description": "CLOCK_SetRootClock removed — SAI root left at reset state, wrong sample rate",
        "mutation": lambda code: _remove_lines(code, "CLOCK_SetRootClock("),
        "must_fail": ["clock_root_configured"],
    },
    {
        "name": "rx_async_mode",
        "description": "RX left async — its idle divider drifts against TX, channels slip within seconds",
        "mutation": lambda code: _remove_lines(code, "rx_config.syncMode"),
        "must_fail": ["rx_sync_mode"],
    },
    {
        "name": "missing_bit_clock_rate",
        "description": "SAI_TxSetBitClockRate removed — BCLK divider at reset value, no valid clock",
        "mutation": lambda code: code.replace(
            "    SAI_TxSetBitClockRate(SAI_BASE, SAI_CLOCK_FREQ, SAMPLE_RATE_HZ,\n"
            "                          BIT_WIDTH, 2U);\n",
            "",
        ),
        "must_fail": ["bit_clock_rate_set"],
    },
    {
        "name": "rx_never_enabled",
        "description": "SAI_RxEnable removed — receiver configured but never started, read blocks forever",
        "mutation": lambda code: _remove_lines(code, "SAI_RxEnable("),
        "must_fail": ["tx_and_rx_enabled"],
    },
    {
        "name": "tx_never_enabled",
        "description": "SAI_TxEnable removed — RX borrows clocks from a transmitter that never runs",
        "mutation": lambda code: _remove_lines(code, "SAI_TxEnable("),
        "must_fail": ["tx_and_rx_enabled"],
    },
    {
        "name": "write_only_no_read",
        "description": "Capture path dropped — pass-through plays back an uninitialised buffer",
        "mutation": lambda code: _remove_lines(code, "SAI_ReadBlocking"),
        "must_fail": ["read_and_write_api_used"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": ["header_fsl_sai_h", "header_fsl_iomuxc_h"],
    },
    {
        "name": "stm32_hal_i2s",
        "description": "STM32 HAL I2S calls used instead of MCUXpresso SAI API",
        # Inject the STM32 HAL I2S API by replacing any SAI read call
        # (ReadBlocking or register-level ReadData), regardless of base/args.
        "mutation": lambda code: re.sub(
            r"\bSAI_Read\w*\s*\([^;]*\);",
            "HAL_I2S_Receive(&hi2s1, (uint16_t *)s_chunk, FRAMES_PER_CHUNK * 2U, 100U);",
            code,
            count=1,
        ),
        "must_fail": ["no_cross_platform_hallucination"],
    },
]
