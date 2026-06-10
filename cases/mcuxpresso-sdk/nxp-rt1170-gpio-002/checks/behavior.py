"""Behavioral checks for nxp-rt1170-gpio-002.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded engineer targeting i.MX RT1170 must know.
"""

import re

from embedeval.check_utils import strip_comments
from embedeval.check_utils_nxp import has_iomuxc_before_init
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit MCUXpresso SDK knowledge for RT1170 GPIO interrupt."""
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

    # Press counter is shared between ISR and main: must be volatile.
    # Match the qualifier on a data declaration only — a bare \bvolatile\b
    # would also match __asm volatile("wfi") and comments.
    has_volatile = bool(re.search(
        r"\bvolatile\b\s+(?:uint|int|unsigned|bool|char|size_t)\w*", stripped
    ))
    details.append(CheckDetail(
        check_name="volatile_press_counter",
        passed=has_volatile,
        expected="volatile qualifier on the ISR-shared press counter",
        actual="present" if has_volatile else "missing",
        check_type="constraint",
    ))

    # IGPIO quirk: interruptMode in gpio_pin_config_t selects the edge but
    # does NOT unmask the pin — an explicit enable call is required.
    has_pin_unmask = bool(re.search(
        r"\bGPIO_(?:Port)?EnableInterrupts\s*\(", stripped
    ))
    details.append(CheckDetail(
        check_name="gpio_port_interrupts_enabled",
        passed=has_pin_unmask,
        expected="GPIO_PortEnableInterrupts unmasks the button pin",
        actual="present" if has_pin_unmask else "missing",
        check_type="constraint",
    ))

    # NVIC-level enable — without it the interrupt pends but never fires
    has_nvic = bool(re.search(r"\b(?:NVIC_)?EnableIRQ\s*\(", stripped))
    details.append(CheckDetail(
        check_name="nvic_irq_enabled",
        passed=has_nvic,
        expected="EnableIRQ called for the GPIO IRQ line",
        actual="present" if has_nvic else "missing",
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
