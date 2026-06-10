"""Negative tests for nxp-mcxc-spi-001 (SPI master transfer, manual CS).

Reference: cases/mcuxpresso-sdk/nxp-mcxc-spi-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic MCXC144 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


NEGATIVES = [
    {
        "name": "missing_clock_gates",
        "description": "CLOCK_EnableClock removed — SPI/PORT access bus-faults with gated clock",
        "mutation": lambda code: _remove_lines(code, "CLOCK_EnableClock"),
        "must_fail": ["clock_gate_before_spi_init"],
    },
    {
        "name": "missing_pinmux",
        "description": "PORT_SetPinMux removed — SCK/MOSI/MISO stay on default mux",
        "mutation": lambda code: _remove_lines(code, "PORT_SetPinMux"),
        "must_fail": ["pinmux_before_spi_init"],
    },
    {
        "name": "no_cs_assert",
        "description": "CS never driven low before transfer — slave ignores the clocks",
        "mutation": lambda code: _remove_lines(code, "cs_assert();"),
        "must_fail": ["cs_asserted_before_transfer"],
    },
    {
        "name": "no_cs_deassert",
        "description": "CS never released after transfer — slave stays selected, bus blocked",
        "mutation": lambda code: _remove_lines(code, "cs_deassert"),
        "must_fail": ["cs_deasserted_after_transfer"],
    },
    {
        "name": "cs_idle_low",
        "description": "CS initialised low — slave selected (and possibly clocked) during init",
        "mutation": lambda code: code.replace(
            ".outputLogic  = 1U,   /* CS idle high */",
            ".outputLogic  = 0U,",
        ),
        "must_fail": ["cs_idle_high_initial_state"],
    },
    {
        "name": "missing_spi_init",
        "description": "SPI_MasterInit removed — peripheral never configured",
        "mutation": lambda code: _remove_lines(code, "SPI_MasterInit(SPI_BASE"),
        "must_fail": ["spi_master_init_called"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": [
            "header_fsl_spi_h",
            "header_fsl_gpio_h",
            "header_fsl_port_h",
            "header_fsl_clock_h",
        ],
    },
    {
        "name": "stm32_spi_transfer",
        "description": "STM32 HAL_SPI_TransmitReceive used instead of MCUXpresso transfer API",
        "mutation": lambda code: code.replace(
            "SPI_MasterTransferBlocking(SPI_BASE, &transfer);",
            "HAL_SPI_TransmitReceive(&hspi1, s_tx_buf, s_rx_buf, 2, 100);",
        ),
        "must_fail": ["spi_blocking_transfer_used", "no_cross_platform_hallucination"],
    },
]
