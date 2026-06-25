"""Negative tests for nxp-rt1170-sai-002 (interrupt-driven sine playback).

Reference: cases/mcuxpresso-sdk/nxp-rt1170-sai-002/reference/main.c
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
        "name": "missing_bit_clock_rate",
        "description": "SAI_TxSetBitClockRate removed — BCLK divider at reset value, DAC gets no valid clock",
        "mutation": lambda code: code.replace(
            "    SAI_TxSetBitClockRate(SAI_BASE, SAI_CLOCK_FREQ, SAMPLE_RATE_HZ,\n"
            "                          BIT_WIDTH, 2U);\n",
            "",
        ),
        "must_fail": ["bit_clock_rate_set"],
    },
    {
        "name": "fifo_irq_not_enabled",
        "description": "SAI_TxEnableInterrupts removed — FIFO drains once and the ISR never fires",
        "mutation": lambda code: code.replace(
            "    SAI_TxEnableInterrupts(SAI_BASE, kSAI_FIFORequestInterruptEnable |\n"
            "                                     kSAI_FIFOErrorInterruptEnable);\n",
            "",
        ),
        "must_fail": ["fifo_interrupt_enabled"],
    },
    {
        "name": "missing_nvic_enable",
        "description": "EnableIRQ removed — SAI interrupt pends but NVIC never dispatches it",
        "mutation": lambda code: _remove_lines(code, "EnableIRQ("),
        "must_fail": ["nvic_irq_enabled"],
    },
    {
        "name": "tx_never_enabled",
        "description": "SAI_TxEnable removed — transmitter configured but never started",
        "mutation": lambda code: _remove_lines(code, "SAI_TxEnable(SAI_BASE, true)"),
        "must_fail": ["tx_enabled"],
    },
    {
        "name": "underrun_not_handled",
        "description": "FIFO error flag never cleared — first underrun stops the tone permanently",
        "mutation": lambda code: code.replace(
            "    if ((SAI_BASE->TCSR & (uint32_t)kSAI_FIFOErrorFlag) != 0U) {\n"
            "        SAI_TxClearStatusFlags(SAI_BASE, kSAI_FIFOErrorFlag);\n"
            "    }\n\n",
            "",
        ).replace(" |\n                                     kSAI_FIFOErrorInterruptEnable", ""),
        "must_fail": ["fifo_underrun_handled"],
    },
    {
        "name": "index_not_volatile",
        "description": "volatile dropped from the sample index — optimiser may cache ISR state",
        "mutation": lambda code: code.replace(
            "static volatile uint32_t", "static uint32_t"
        ),
        "must_fail": ["volatile_sample_index"],
    },
    {
        "name": "blocking_write_in_main",
        "description": "Streaming moved to a blocking write in main — ignores the required architecture",
        "mutation": lambda code: code.replace(
            '        __asm volatile("wfi");',
            "        SAI_WriteBlocking(SAI_BASE, 0U, BIT_WIDTH,\n"
            "                          (uint8_t *)s_sine_table, sizeof(s_sine_table));",
        ),
        "must_fail": ["no_blocking_write"],
    },
    {
        "name": "isr_name_mismatch",
        "description": "Handler name does not match the vector table entry — default handler traps",
        "mutation": lambda code: code.replace(
            "SAI1_IRQHandler(void)", "Audio_Handler(void)"
        ),
        "must_fail": ["isr_handler_defined"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": ["header_fsl_sai_h", "header_fsl_iomuxc_h"],
    },
    {
        "name": "stm32_hal_i2s",
        "description": "STM32 HAL I2S call used instead of MCUXpresso SAI API",
        # Inject the STM32 HAL I2S API by replacing any SAI write call
        # (WriteData or WriteBlocking), regardless of base/args.
        "mutation": lambda code: re.sub(
            r"\bSAI_Write\w*\s*\([^;]*\);",
            "HAL_I2S_Transmit_IT(&hi2s1, (uint16_t *)&sample, 2U);",
            code,
            count=1,
        ),
        "must_fail": ["no_cross_platform_hallucination"],
    },
]
