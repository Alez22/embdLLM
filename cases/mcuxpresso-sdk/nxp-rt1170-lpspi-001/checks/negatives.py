"""Negative tests for nxp-rt1170-lpspi-001 (SPI flash JEDEC ID read).

Reference: cases/mcuxpresso-sdk/nxp-rt1170-lpspi-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic RT1170 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


NEGATIVES = [
    {
        "name": "missing_iomuxc_mux",
        "description": "IOMUXC_SetPinMux removed — SPI pads stay on default function, bus dead",
        "mutation": lambda code: _remove_lines(code, "IOMUXC_SetPinMux"),
        "must_fail": ["iomuxc_before_lpspi_init"],
    },
    {
        "name": "iomuxc_after_init",
        "description": "Pads muxed after LPSPI_MasterInit — init runs while pads are unrouted",
        "mutation": lambda code: (
            _remove_lines(code, "IOMUXC_SetPinMux")
            .replace(
                "    memset(&xfer, 0, sizeof(xfer));",
                "    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_28_LPSPI1_SCK, 0U);\n\n"
                "    memset(&xfer, 0, sizeof(xfer));",
            )
        ),
        "must_fail": ["iomuxc_before_lpspi_init"],
    },
    {
        "name": "missing_clock_root",
        "description": "CLOCK_SetRootClock removed — LPSPI root left at reset state, wrong SCK rate",
        "mutation": lambda code: _remove_lines(code, "CLOCK_SetRootClock("),
        "must_fail": ["clock_root_configured"],
    },
    {
        "name": "pcs_toggle_per_word",
        "description": "PCS continuous flag dropped — flash deselected after the opcode, ID reads 0xFF",
        "mutation": lambda code: code.replace(
            "kLPSPI_MasterPcs0 | kLPSPI_MasterPcsContinuous",
            "kLPSPI_MasterPcs0",
        ),
        "must_fail": ["pcs_continuous_set"],
    },
    {
        "name": "transfer_status_ignored",
        "description": "Transfer return value discarded — bus error yields a bogus ID",
        "mutation": lambda code: code.replace(
            "    if (LPSPI_MasterTransferBlocking(FLASH_SPI, &xfer) != kStatus_Success) {\n"
            "        /* Bus error: stop here rather than report a bogus ID */\n"
            "        while (1) {\n"
            "        }\n"
            "    }\n",
            "    LPSPI_MasterTransferBlocking(FLASH_SPI, &xfer);\n",
        ),
        "must_fail": ["transfer_status_checked"],
    },
    {
        "name": "wrong_command",
        "description": "Read command 0x03 sent instead of JEDEC ID 0x9F",
        "mutation": lambda code: code.replace("0x9FU", "0x03U"),
        "must_fail": ["jedec_command_used"],
    },
    {
        "name": "kinetis_dspi_api",
        "description": "Kinetis DSPI API used — wrong NXP family, RT1170 has LPSPI only",
        "mutation": lambda code: code.replace(
            "LPSPI_MasterTransferBlocking(FLASH_SPI, &xfer)",
            "DSPI_MasterTransferBlocking(FLASH_SPI, &xfer)",
        ),
        "must_fail": ["no_legacy_kinetis_spi_api"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": ["header_fsl_lpspi_h", "header_fsl_iomuxc_h"],
    },
    {
        "name": "stm32_hal_spi",
        "description": "STM32 HAL SPI call used instead of MCUXpresso LPSPI API",
        "mutation": lambda code: code.replace(
            "LPSPI_MasterTransferBlocking(FLASH_SPI, &xfer)",
            "HAL_SPI_TransmitReceive(&hspi1, tx_buf, rx_buf, 4U, 100U)",
        ),
        "must_fail": ["no_cross_platform_hallucination"],
    },
]
