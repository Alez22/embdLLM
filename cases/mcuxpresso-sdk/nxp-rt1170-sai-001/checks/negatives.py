"""Negative tests for nxp-rt1170-sai-001 (SAI I2S playback + codec setup).

Reference: cases/mcuxpresso-sdk/nxp-rt1170-sai-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic RT1170 audio bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""

# Codec power-up call in main, including its error check.
_CODEC_CALL_BLOCK = (
    "    /* Codec must be configured before streaming starts: it has to lock to\n"
    "       BCLK and be powered before the first valid frame. */\n"
    "    if (codec_power_up() != kStatus_Success) {\n"
    "        while (1);\n"
    "    }\n"
    "\n"
)


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


def _remove_codec_entirely(code: str) -> str:
    """Drop the codec helpers and their call site — codec never configured."""
    # Remove helper bodies by deleting every line between the helper
    # signatures and the streaming buffer build (helpers are contiguous).
    start = code.find("static status_t codec_write_reg")
    end = code.find("int main(void)")
    if start == -1 or end == -1:
        return code
    code = code[:start] + code[end:]
    return code.replace(_CODEC_CALL_BLOCK, "")


NEGATIVES = [
    {
        "name": "missing_iomuxc_mux",
        "description": "IOMUXC_SetPinMux removed — SAI/I2C pads unrouted, no clocks reach the DAC",
        "mutation": lambda code: _remove_lines(code, "IOMUXC_SetPinMux"),
        "must_fail": ["iomuxc_before_sai_init"],
    },
    {
        "name": "missing_clock_root",
        "description": "CLOCK_SetRootClock removed — SAI runs without an audio-capable clock root",
        "mutation": lambda code: _remove_lines(code, "CLOCK_SetRootClock"),
        "must_fail": ["clock_root_configured"],
    },
    {
        "name": "sai_config_before_init",
        "description": "SAI_TxSetConfig before SAI_Init — configures a module that was never enabled",
        "mutation": lambda code: (
            code
            .replace("    SAI_Init(SAI_BASE);\n", "")
            .replace(
                "    SAI_TxSetBitClockRate(",
                "    SAI_Init(SAI_BASE);\n    SAI_TxSetBitClockRate(",
            )
        ),
        "must_fail": ["sai_init_before_tx_config"],
    },
    {
        "name": "missing_bit_clock_rate",
        "description": "SAI_TxSetBitClockRate removed — BCLK divider stays at reset, DAC gets no valid clock",
        "mutation": lambda code: code.replace(
            "    SAI_TxSetBitClockRate(SAI_BASE, SAI_CLOCK_FREQ, SAMPLE_RATE_HZ,\n"
            "                          BIT_WIDTH, 2U);\n",
            "",
        ),
        "must_fail": ["bit_clock_rate_set"],
    },
    {
        "name": "codec_never_configured",
        "description": "Codec register writes removed — DAC stays powered down, silence on the output",
        "mutation": _remove_codec_entirely,
        "must_fail": [
            "codec_configured_before_streaming",
            "lpi2c_blocking_transfer_used",
        ],
    },
    {
        "name": "codec_status_ignored",
        "description": "Codec write return values ignored — a dead codec goes unnoticed",
        "mutation": lambda code: (
            code
            .replace(
                "    status = codec_write_reg(0x02U, 0x01U);   /* DAC power on */\n"
                "    if (status != kStatus_Success) { return status; }\n"
                "    status = codec_write_reg(0x04U, 0x00U);   /* I2S slave, 16-bit */\n"
                "    if (status != kStatus_Success) { return status; }\n"
                "    return codec_write_reg(0x06U, 0x3FU);     /* output volume */\n",
                "    codec_write_reg(0x02U, 0x01U);\n"
                "    codec_write_reg(0x04U, 0x00U);\n"
                "    codec_write_reg(0x06U, 0x3FU);\n"
                "    return 0;\n",
            )
            .replace(
                "    if (codec_power_up() != kStatus_Success) {\n"
                "        while (1);\n"
                "    }\n",
                "    codec_power_up();\n",
            )
        ),
        "must_fail": ["codec_write_status_checked"],
    },
    {
        "name": "preshifted_codec_address",
        "description": "Codec address pre-shifted (0x18 << 1) — SDK shifts internally, codec never ACKs",
        "mutation": lambda code: code.replace(
            "#define CODEC_ADDR        0x18U",
            "#define CODEC_ADDR        (0x18U << 1)",
        ),
        "must_fail": ["codec_address_not_preshifted"],
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
        "must_fail": ["no_legacy_kinetis_i2c_api", "lpi2c_blocking_transfer_used"],
    },
    {
        "name": "missing_sdk_headers",
        "description": "fsl_* includes removed — relies on transitive includes that may not exist",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_'),
        "must_fail": ["header_fsl_sai_h", "header_fsl_lpi2c_h", "header_fsl_iomuxc_h"],
    },
    {
        "name": "esp_i2s_api",
        "description": "ESP-IDF i2s_write used instead of MCUXpresso SAI API",
        "mutation": lambda code: code.replace(
            "        SAI_WriteBlocking(SAI_BASE, 0U, BIT_WIDTH,\n"
            "                          (uint8_t *)s_audio_buf, sizeof(s_audio_buf));",
            "        esp_i2s_write(I2S_NUM_0, s_audio_buf, sizeof(s_audio_buf),"
            " &written, portMAX_DELAY);",
        ),
        "must_fail": ["sai_write_api_used", "no_cross_platform_hallucination"],
    },
]
