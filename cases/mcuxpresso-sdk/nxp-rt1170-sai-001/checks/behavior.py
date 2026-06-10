"""Behavioral checks for nxp-rt1170-sai-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded audio engineer targeting i.MX RT1170 must know.

Note: codec_configured_before_streaming compares the position of the first
LPI2C transfer against the first SAI write. With helper-function style the
helper definition naturally precedes main(), so this is a coarse textual
heuristic — it reliably catches a *missing* codec configuration, not a
reordered one.
"""

import re

from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.check_utils_nxp import has_iomuxc_before_init
from embedeval.models import CheckDetail

_SAI_WRITE_RE = re.compile(
    r"\b(SAI_WriteBlocking|SAI_TransferSendBlocking|"
    r"SAI_TransferSendNonBlocking|SAI_WriteNonBlocking)\s*\("
)


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit SAI/I2S + codec knowledge for RT1170 audio TX."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    # Pad mux before SAI init (implicit)
    mux_ordered = has_iomuxc_before_init(generated_code, "SAI_Init")
    has_mux = bool(re.search(r"\bIOMUXC\w*_SetPinMux\s*\(", stripped))
    mux_ok = has_mux and mux_ordered
    details.append(CheckDetail(
        check_name="iomuxc_before_sai_init",
        passed=mux_ok,
        expected="IOMUXC_SetPinMux called before SAI_Init",
        actual="correct order" if mux_ok else (
            "IOMUXC_SetPinMux missing" if not has_mux else "wrong order"
        ),
        check_type="constraint",
    ))

    # Clock root configured for the SAI (implicit: no BOARD_BootClockRUN here)
    has_clock_root = scoped_contains(
        generated_code, "CLOCK_SetRootClock", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="clock_root_configured",
        passed=has_clock_root,
        expected="CLOCK_SetRootClock called (SAI needs an audio-capable root)",
        actual="present" if has_clock_root else "missing",
        check_type="constraint",
    ))

    # SAI_Init before TX config (implicit ordering)
    init_pos = stripped.find("SAI_Init")
    cfg_match = re.search(r"\bSAI_TxSetConfig\s*\(", stripped)
    if cfg_match is None:
        init_order_ok = init_pos != -1   # alternative config path — init still required
        init_actual = "SAI_TxSetConfig not used" if init_pos != -1 else "SAI_Init missing"
    else:
        init_order_ok = init_pos != -1 and init_pos < cfg_match.start()
        init_actual = "correct order" if init_order_ok else "SAI_Init missing or after config"
    details.append(CheckDetail(
        check_name="sai_init_before_tx_config",
        passed=init_order_ok,
        expected="SAI_Init called before SAI_TxSetConfig",
        actual=init_actual,
        check_type="constraint",
    ))

    # Bit clock rate derived from sample rate (easy to forget: without it
    # the BCLK divider stays at reset value and the DAC receives no valid clock)
    has_bclk = scoped_contains(
        generated_code, "SAI_TxSetBitClockRate", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="bit_clock_rate_set",
        passed=has_bclk,
        expected="SAI_TxSetBitClockRate called for 48 kHz / 16-bit / stereo",
        actual="present" if has_bclk else "missing",
        check_type="constraint",
    ))

    # Codec configured before streaming starts (coarse: I2C transfer appears
    # before the first SAI write in the source)
    i2c_pos = stripped.find("LPI2C_MasterTransferBlocking")
    write_match = _SAI_WRITE_RE.search(stripped)
    codec_ok = (
        i2c_pos != -1 and write_match is not None and i2c_pos < write_match.start()
    )
    details.append(CheckDetail(
        check_name="codec_configured_before_streaming",
        passed=codec_ok,
        expected="codec register writes before SAI streaming starts",
        actual="correct order" if codec_ok else "codec config missing or after streaming",
        check_type="constraint",
    ))

    # Codec I2C writes checked for success (implicit)
    has_status_check = scoped_contains(
        generated_code, "kStatus_Success", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="codec_write_status_checked",
        passed=has_status_check,
        expected="kStatus_Success checked on codec register writes",
        actual="present" if has_status_check else "missing",
        check_type="constraint",
    ))

    # 7-bit codec address not pre-shifted
    has_shift_expr = bool(re.search(r"0[xX]18[Uu]?\s*<<\s*1", stripped))
    details.append(CheckDetail(
        check_name="codec_address_not_preshifted",
        passed=not has_shift_expr,
        expected="7-bit address 0x18 used (SDK shifts internally)",
        actual="correct" if not has_shift_expr else "shift expression 0x18 << 1 found",
        check_type="constraint",
    ))

    # No legacy Kinetis I2C API on RT1170
    has_legacy = bool(re.search(r"\bI2C_Master\w*\s*\(", stripped))
    details.append(CheckDetail(
        check_name="no_legacy_kinetis_i2c_api",
        passed=not has_legacy,
        expected="LPI2C_* API used, not Kinetis I2C_Master*",
        actual="clean" if not has_legacy else "Kinetis I2C_Master* API found",
        check_type="constraint",
    ))

    return details
