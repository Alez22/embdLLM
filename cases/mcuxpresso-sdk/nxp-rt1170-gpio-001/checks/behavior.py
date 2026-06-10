"""Behavioral checks for nxp-rt1170-gpio-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded engineer targeting i.MX RT1170 must know.
"""

import re

from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.check_utils_nxp import has_iomuxc_before_init
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit MCUXpresso SDK knowledge for RT1170 GPIO output."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    # Pad mux via IOMUXC before GPIO init (implicit: prompt never mentions this)
    mux_ordered = has_iomuxc_before_init(generated_code, "GPIO_PinInit")
    has_mux = bool(re.search(r"\bIOMUXC\w*_SetPinMux\s*\(", stripped))
    mux_ok = has_mux and mux_ordered
    details.append(CheckDetail(
        check_name="iomuxc_before_gpio_init",
        passed=mux_ok,
        expected="IOMUXC_SetPinMux called before GPIO_PinInit",
        actual="correct order" if mux_ok else (
            "IOMUXC_SetPinMux missing" if not has_mux else "wrong order"
        ),
        check_type="constraint",
    ))

    # Pad electrical config set (drive strength etc.) — implicit
    has_pad_cfg = bool(re.search(r"\bIOMUXC\w*_SetPinConfig\s*\(", stripped))
    details.append(CheckDetail(
        check_name="pad_config_set",
        passed=has_pad_cfg,
        expected="IOMUXC_SetPinConfig called for the LED pad",
        actual="present" if has_pad_cfg else "missing",
        check_type="constraint",
    ))

    # Output direction configured
    has_output_dir = scoped_contains(
        generated_code, "kGPIO_DigitalOutput", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="output_direction_configured",
        passed=has_output_dir,
        expected="kGPIO_DigitalOutput set in gpio_pin_config_t",
        actual="present" if has_output_dir else "missing",
        check_type="constraint",
    ))

    # No Kinetis PORT API — RT1170 routes pads via IOMUXC, PORT_SetPinMux
    # is a different NXP family (cross-family confusion)
    has_kinetis_port = bool(re.search(r"\bPORT_SetPin\w+\s*\(", stripped))
    details.append(CheckDetail(
        check_name="no_kinetis_port_api",
        passed=not has_kinetis_port,
        expected="No Kinetis PORT_SetPin* API on i.MX RT",
        actual="clean" if not has_kinetis_port else "Kinetis PORT API found",
        check_type="constraint",
    ))

    return details
