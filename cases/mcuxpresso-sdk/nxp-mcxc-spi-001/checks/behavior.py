"""Behavioral checks for nxp-mcxc-spi-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention
but an embedded engineer targeting MCXC144 must know.
"""

import re

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import has_clock_gate_before, has_pinmux_before_init
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit MCUXpresso SDK knowledge for SPI master + manual CS."""
    details: list[CheckDetail] = []

    # Clock gate before SPI_MasterInit
    clock_ok = has_clock_gate_before(generated_code, "SPI_MasterInit")
    has_clock = scoped_contains(generated_code, "CLOCK_EnableClock", scope="stripped")
    details.append(CheckDetail(
        check_name="clock_gate_before_spi_init",
        passed=has_clock and clock_ok,
        expected="CLOCK_EnableClock called before SPI_MasterInit",
        actual="correct order" if (has_clock and clock_ok) else (
            "CLOCK_EnableClock missing" if not has_clock else "wrong order"
        ),
        check_type="constraint",
    ))

    # Pin mux configured before SPI init
    pinmux_ok = has_pinmux_before_init(generated_code, "SPI_MasterInit")
    has_pinmux = bool(re.search(r"\bPORT_SetPin\w+\s*\(", generated_code))
    details.append(CheckDetail(
        check_name="pinmux_before_spi_init",
        passed=has_pinmux and pinmux_ok,
        expected="PORT_SetPinMux called before SPI_MasterInit",
        actual="correct order" if (has_pinmux and pinmux_ok) else (
            "PORT_SetPinMux missing" if not has_pinmux else "wrong order"
        ),
        check_type="constraint",
    ))

    # CS asserted (low) before transfer — must be called in the transfer sequence,
    # not just defined as a helper. Anchor on SPI_MasterInit: the inline helper
    # definition (if any) appears before it, so search for the cs assert pattern
    # only in the code that follows SPI_MasterInit.
    spi_init_match = re.search(r"\bSPI_MasterInit\s*\(", generated_code)
    transfer_match = re.search(r"\bSPI_MasterTransferBlocking\s*\(", generated_code)
    if spi_init_match and transfer_match:
        between = generated_code[spi_init_match.end():transfer_match.start()]
        cs_assert_call = bool(re.search(
            r"(cs_assert\s*\(\s*\)|GPIO_PinWrite\s*\([^,]+,\s*\w+\s*,\s*0[Uu]?\s*\))",
            between
        ))
    else:
        cs_assert_call = False
    details.append(CheckDetail(
        check_name="cs_asserted_before_transfer",
        passed=cs_assert_call,
        expected="CS driven low (GPIO_PinWrite with 0 or cs_assert()) called before SPI transfer",
        actual="present" if cs_assert_call else "missing",
        check_type="constraint",
    ))

    # CS deasserted (high) after transfer
    cs_deassert_pattern = re.search(
        r"GPIO_PinWrite\s*\([^,]+,\s*\w+\s*,\s*1[Uu]?\s*\)", generated_code
    )
    details.append(CheckDetail(
        check_name="cs_deasserted_after_transfer",
        passed=bool(cs_deassert_pattern),
        expected="CS driven high (GPIO_PinWrite with 1) after SPI transfer",
        actual="present" if cs_deassert_pattern else "missing",
        check_type="constraint",
    ))

    # CS idle-high initial state (outputLogic = 1 in gpio_pin_config_t)
    cs_idle_high = bool(re.search(
        r"\.outputLogic\s*=\s*1[Uu]?", generated_code
    ))
    details.append(CheckDetail(
        check_name="cs_idle_high_initial_state",
        passed=cs_idle_high,
        expected="CS GPIO initialised high (outputLogic = 1)",
        actual="present" if cs_idle_high else "missing — CS may glitch low on init",
        check_type="constraint",
    ))

    return details
