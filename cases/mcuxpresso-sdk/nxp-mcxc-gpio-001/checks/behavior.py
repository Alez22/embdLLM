"""Behavioral checks for nxp-mcxc-gpio-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded engineer targeting MCXC144 must know.
"""

import re

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import has_clock_gate_before, has_pinmux_before_init
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit MCUXpresso SDK knowledge for GPIO output."""
    details: list[CheckDetail] = []

    # Clock gate before GPIO_PinInit (implicit: prompt never mentions this)
    clock_ordered = has_clock_gate_before(generated_code, "GPIO_PinInit")
    has_clock = scoped_contains(generated_code, "CLOCK_EnableClock", scope="stripped")
    clock_ok = has_clock and clock_ordered
    details.append(CheckDetail(
        check_name="clock_gate_before_gpio_init",
        passed=clock_ok,
        expected="CLOCK_EnableClock called before GPIO_PinInit",
        actual="correct order" if clock_ok else (
            "CLOCK_EnableClock missing" if not has_clock else "wrong order"
        ),
        check_type="constraint",
    ))

    # Pin mux set to GPIO alternate function before GPIO_PinInit
    pinmux_ordered = has_pinmux_before_init(generated_code, "GPIO_PinInit")
    has_pinmux = bool(re.search(r"\bPORT_SetPin\w+\s*\(", generated_code))
    pinmux_ok = has_pinmux and pinmux_ordered
    details.append(CheckDetail(
        check_name="pinmux_as_gpio_before_init",
        passed=pinmux_ok,
        expected="PORT_SetPinMux with kPORT_MuxAsGpio before GPIO_PinInit",
        actual="correct order" if pinmux_ok else (
            "PORT_SetPinMux missing" if not has_pinmux else "wrong order"
        ),
        check_type="constraint",
    ))

    # Output direction configured (kGPIO_DigitalOutput)
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

    # kPORT_MuxAsGpio used for pin mux (not a numeric literal)
    has_gpio_mux = scoped_contains(generated_code, "kPORT_MuxAsGpio", scope="stripped")
    details.append(CheckDetail(
        check_name="gpio_mux_enum_used",
        passed=has_gpio_mux,
        expected="kPORT_MuxAsGpio used (not raw integer)",
        actual="present" if has_gpio_mux else "missing or raw integer",
        check_type="constraint",
    ))

    return details
