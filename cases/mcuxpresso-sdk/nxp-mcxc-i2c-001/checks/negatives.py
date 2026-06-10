"""Negative tests for nxp-mcxc-i2c-001 (I2C master WHO_AM_I read).

Reference: cases/mcuxpresso-sdk/nxp-mcxc-i2c-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic MCXC144 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""

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
        "mutation": lambda code: code.replace(
            "#define SENSOR_ADDR       0x68U",
            "#define SENSOR_ADDR       0xD0U",
        ),
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
        "mutation": lambda code: code.replace(
            "status = I2C_MasterTransferBlocking(I2C0, &transfer);",
            "status = HAL_I2C_Mem_Read(&hi2c1, SENSOR_ADDR, WHO_AM_I_REG,"
            " 1, &s_who_am_i, 1, 100);",
        ),
        "must_fail": ["i2c_blocking_transfer_used", "no_cross_platform_hallucination"],
    },
]
