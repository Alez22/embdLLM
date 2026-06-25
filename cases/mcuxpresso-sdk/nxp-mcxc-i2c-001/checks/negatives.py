"""Negative tests for nxp-mcxc-i2c-001 (I2C master WHO_AM_I read).

Reference: cases/mcuxpresso-sdk/nxp-mcxc-i2c-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic MCXC144 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""

import re

_CLOCK_BLOCK = (
    "    CLOCK_EnableClock(kCLOCK_PortC);\n"
    "    CLOCK_EnableClock(kCLOCK_I2c0);\n"
)

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
        "name": "missing_clock_gates",
        "description": "CLOCK_EnableClock removed — I2C/PORT access bus-faults with gated clock",
        "mutation": lambda code: _remove_lines(code, "CLOCK_EnableClock"),
        "must_fail": ["clock_gate_before_i2c_init"],
    },
    {
        "name": "clock_gates_after_init",
        "description": "Clocks enabled after I2C_MasterInit — init writes to a gated peripheral",
        "mutation": lambda code: (
            code
            .replace(_CLOCK_BLOCK, "")
            .replace(
                "I2C_MasterInit(I2C0, &masterConfig, I2C0_CLK_FREQ);",
                "I2C_MasterInit(I2C0, &masterConfig, I2C0_CLK_FREQ);\n" + _CLOCK_BLOCK,
            )
        ),
        "must_fail": ["clock_gate_before_i2c_init"],
    },
    {
        "name": "missing_pinmux",
        "description": "PORT_SetPinMux removed — SCL/SDA stay on default mux, bus dead",
        "mutation": lambda code: _remove_lines(code, "PORT_SetPinMux"),
        "must_fail": ["pinmux_before_i2c_init"],
    },
    {
        "name": "preshifted_address",
        "description": "8-bit pre-shifted address 0xD0 — SDK shifts internally, device never ACKs",
        # Pre-shift the 7-bit address literal (0x68 -> 0xD0) wherever it appears
        # — in a #define under any macro name, or inline in the transfer.
        # i2c_address_not_preshifted flags the hardcoded 0xD0. The device regs
        # in this case are 0x75/0x1A, never 0x68, so replacing every 0x68 token
        # is safe. The literal whole-line replace missed nearly every model.
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
        "description": "kI2C_TransferDefaultFlag not set — transfer flags left at garbage/zero",
        "mutation": lambda code: _remove_lines(code, "kI2C_TransferDefaultFlag"),
        "must_fail": ["default_transfer_flag_set"],
    },
    {
        "name": "missing_master_init",
        "description": "I2C_MasterInit removed — peripheral never configured",
        "mutation": lambda code: _remove_lines(code, "I2C_MasterInit(I2C0"),
        "must_fail": ["i2c_master_init_called"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": ["header_fsl_i2c_h", "header_fsl_port_h", "header_fsl_clock_h"],
    },
    {
        "name": "stm32_mem_read",
        "description": "STM32 HAL_I2C_Mem_Read used instead of MCUXpresso transfer API",
        # Replace any I2C_MasterTransferBlocking(...) with the STM32 HAL call,
        # regardless of base/args: removes the NXP transfer (fails
        # i2c_blocking_transfer_used) and injects HAL_.
        "mutation": lambda code: re.sub(
            r"\bI2C_MasterTransferBlocking\s*\([^;]*\)",
            "HAL_I2C_Mem_Read(&hi2c1, SENSOR_ADDR, WHO_AM_I_REG,"
            " 1, &s_who_am_i, 1, 100)",
            code,
        ),
        "must_fail": ["i2c_blocking_transfer_used", "no_cross_platform_hallucination"],
    },
]
