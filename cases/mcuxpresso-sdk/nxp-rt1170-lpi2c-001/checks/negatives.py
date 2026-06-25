"""Negative tests for nxp-rt1170-lpi2c-001 (LPI2C master WHO_AM_I read).

Reference: cases/mcuxpresso-sdk/nxp-rt1170-lpi2c-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic RT1170 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""

import re

_STATUS_CHECK_BLOCK = (
    "    if (status != kStatus_Success) {\n"
    "        /* Communication error — halt */\n"
    "        while (1);\n"
    "    }\n"
)


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


NEGATIVES = [
    {
        "name": "missing_iomuxc_mux",
        "description": "IOMUXC_SetPinMux removed — SCL/SDA pads unrouted, bus dead",
        "mutation": lambda code: _remove_lines(code, "IOMUXC_SetPinMux"),
        "must_fail": ["iomuxc_before_lpi2c_init"],
    },
    {
        "name": "missing_clock_root",
        "description": "CLOCK_SetRootClock removed — LPI2C functional clock not configured",
        "mutation": lambda code: _remove_lines(code, "CLOCK_SetRootClock"),
        "must_fail": ["clock_root_configured"],
    },
    {
        "name": "preshifted_address",
        "description": "8-bit pre-shifted address 0xD0 — SDK shifts internally, device never ACKs",
        # Pre-shift the 7-bit address literal (0x68 -> 0xD0) wherever it appears
        # — in a #define under any macro name, or inline. The device regs here
        # are 0x75/..., never 0x68, so replacing every 0x68 token is safe.
        "mutation": lambda code: re.sub(r"\b0x68[Uu]?\b", "0xD0U", code),
        "must_fail": ["i2c_address_not_preshifted"],
    },
    {
        "name": "status_ignored",
        "description": "Transfer return value ignored — NAK/arbitration loss silently swallowed",
        "mutation": lambda code: code.replace(_STATUS_CHECK_BLOCK, ""),
        "must_fail": ["transfer_return_value_checked"],
    },
    {
        "name": "missing_default_flag",
        "description": "kLPI2C_TransferDefaultFlag not set — transfer flags left at garbage/zero",
        "mutation": lambda code: _remove_lines(code, "kLPI2C_TransferDefaultFlag"),
        "must_fail": ["default_transfer_flag_set"],
    },
    {
        "name": "legacy_kinetis_i2c",
        "description": "Kinetis I2C_Master* API used — wrong NXP family, does not exist on RT1170",
        "mutation": lambda code: (
            code
            .replace("LPI2C_MasterGetDefaultConfig", "I2C_MasterGetDefaultConfig")
            .replace("LPI2C_MasterInit", "I2C_MasterInit")
            .replace("LPI2C_MasterTransferBlocking", "I2C_MasterTransferBlocking")
        ),
        "must_fail": [
            "no_legacy_kinetis_i2c_api",
            "lpi2c_master_init_called",
            "lpi2c_blocking_transfer_used",
        ],
    },
    {
        "name": "missing_master_init",
        "description": "LPI2C_MasterInit removed — peripheral never configured",
        "mutation": lambda code: _remove_lines(code, "LPI2C_MasterInit(LPI2C_BASE"),
        "must_fail": ["lpi2c_master_init_called"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": ["header_fsl_lpi2c_h", "header_fsl_iomuxc_h", "header_fsl_clock_h"],
    },
    {
        "name": "stm32_mem_read",
        "description": "STM32 HAL_I2C_Mem_Read used instead of MCUXpresso transfer API",
        # Replace any LPI2C_MasterTransferBlocking(...) with the STM32 HAL call,
        # regardless of base/args.
        "mutation": lambda code: re.sub(
            r"\bLPI2C_MasterTransferBlocking\s*\([^;]*\)",
            "HAL_I2C_Mem_Read(&hi2c1, SENSOR_ADDR, WHO_AM_I_REG,"
            " 1, &s_who_am_i, 1, 100)",
            code,
        ),
        "must_fail": ["lpi2c_blocking_transfer_used", "no_cross_platform_hallucination"],
    },
]
