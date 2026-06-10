"""Negative tests for nxp-mcxc-i2c-002 (I2C write + read-back verify).

Reference: cases/mcuxpresso-sdk/nxp-mcxc-i2c-002/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic MCXC144 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""

_STATUS_CHECK_BLOCK = (
    "    if (status != kStatus_Success) {\n"
    "        while (1);\n"
    "    }\n"
)

# Entire read-back helper — removing it kills both kI2C_Read and the
# second I2C_MasterTransferBlocking occurrence.
_READ_HELPER = (
    "static status_t i2c_read_reg(uint8_t reg, uint8_t *out)\n"
    "{\n"
    "    i2c_master_transfer_t xfer;\n"
    "\n"
    "    memset(&xfer, 0, sizeof(xfer));\n"
    "    xfer.slaveAddress   = SENSOR_ADDR;\n"
    "    xfer.direction      = kI2C_Read;\n"
    "    xfer.subaddress     = reg;\n"
    "    xfer.subaddressSize = 1U;\n"
    "    xfer.data           = out;\n"
    "    xfer.dataSize       = 1U;\n"
    "    xfer.flags          = kI2C_TransferDefaultFlag;\n"
    "    return I2C_MasterTransferBlocking(I2C0, &xfer);\n"
    "}\n"
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
        "name": "missing_pinmux",
        "description": "PORT_SetPinMux removed — SCL/SDA stay on default mux, bus dead",
        "mutation": lambda code: _remove_lines(code, "PORT_SetPinMux"),
        "must_fail": ["pinmux_before_i2c_init"],
    },
    {
        "name": "preshifted_address",
        "description": "8-bit pre-shifted address 0xD0 — SDK shifts internally, device never ACKs",
        "mutation": lambda code: code.replace(
            "#define SENSOR_ADDR     0x68U",
            "#define SENSOR_ADDR     0xD0U",
        ),
        "must_fail": ["i2c_address_not_preshifted"],
    },
    {
        "name": "single_status_check",
        "description": "Only one of two transfer return values checked — read-back error swallowed",
        "mutation": lambda code: code.replace(_STATUS_CHECK_BLOCK, "", 1),
        "must_fail": ["both_transfer_returns_checked"],
    },
    {
        "name": "write_without_readback",
        "description": "Read-back helper removed — write never verified",
        "mutation": lambda code: code.replace(_READ_HELPER, ""),
        "must_fail": ["both_write_and_read_transfers", "two_separate_transfers"],
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
        "name": "zephyr_i2c_api",
        "description": "Zephyr i2c_write_read used instead of MCUXpresso transfer API",
        "mutation": lambda code: code.replace(
            "I2C_MasterTransferBlocking", "i2c_write_read"
        ),
        "must_fail": ["no_cross_platform_hallucination", "two_separate_transfers"],
    },
]
