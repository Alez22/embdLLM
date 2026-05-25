"""Behavioral checks for nxp-mcxc-uart-001.

L3: verifies implicit domain knowledge — things the prompt does NOT mention.
"""

import re

from embedeval.check_utils import scoped_contains
from embedeval.check_utils_nxp import has_clock_gate_before, has_pinmux_before_init
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate implicit MCUXpresso SDK knowledge for UART TX."""
    details: list[CheckDetail] = []

    # Clock gate before UART_Init
    clock_ok = has_clock_gate_before(generated_code, "UART_Init")
    has_clock = scoped_contains(generated_code, "CLOCK_EnableClock", scope="stripped")
    details.append(CheckDetail(
        check_name="clock_gate_before_uart_init",
        passed=has_clock and clock_ok,
        expected="CLOCK_EnableClock called before UART_Init",
        actual="correct order" if (has_clock and clock_ok) else (
            "CLOCK_EnableClock missing" if not has_clock else "wrong order"
        ),
        check_type="constraint",
    ))

    # Pin mux before UART_Init
    pinmux_ok = has_pinmux_before_init(generated_code, "UART_Init")
    has_pinmux = bool(re.search(r"\bPORT_SetPin\w+\s*\(", generated_code))
    details.append(CheckDetail(
        check_name="pinmux_before_uart_init",
        passed=has_pinmux and pinmux_ok,
        expected="PORT_SetPinMux called before UART_Init",
        actual="correct order" if (has_pinmux and pinmux_ok) else (
            "PORT_SetPinMux missing" if not has_pinmux else "wrong order"
        ),
        check_type="constraint",
    ))

    # TX explicitly enabled in config
    has_tx_enabled = bool(re.search(
        r"\.enableTx\s*=\s*true", generated_code
    ))
    details.append(CheckDetail(
        check_name="uart_tx_enabled_in_config",
        passed=has_tx_enabled,
        expected="enableTx = true set in uart_config_t",
        actual="present" if has_tx_enabled else "missing",
        check_type="constraint",
    ))

    return details
