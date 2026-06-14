"""NXP MCUXpresso SDK check helpers.

Shared by all nxp-bare-metal case checks. Follows the same conventions
as check_utils.py: functions accept raw code strings and strip comments
internally. No external dependencies beyond check_utils.
"""

import re

from embedeval.check_utils import strip_comments

# ---------------------------------------------------------------------------
# SDK token lists — used by case checks to avoid hardcoding strings.
# ---------------------------------------------------------------------------

FSL_HEADERS: list[str] = [
    "fsl_clock.h",
    "fsl_port.h",
    "fsl_gpio.h",
    "fsl_i2c.h",
    "fsl_spi.h",
    "fsl_uart.h",
    "fsl_pit.h",
    "fsl_dma.h",
    "fsl_flash.h",
    "fsl_wdog.h",
]

CLOCK_APIS: list[str] = [
    "CLOCK_EnableClock",
    "CLOCK_SetIpSrc",
    "CLOCK_SetIpDiv",
]

PORT_APIS: list[str] = [
    "PORT_SetPinMux",
    "PORT_SetPinConfig",
    "PORT_SetMultiplePinsConfig",
]

GPIO_APIS: list[str] = [
    "GPIO_PinInit",
    "GPIO_PinWrite",
    "GPIO_PinRead",
    "GPIO_PortToggle",
    "GPIO_SetPinsOutput",
    "GPIO_ClearPinsOutput",
]

# ---------------------------------------------------------------------------
# Internal: foreign-platform patterns to detect hallucinations.
#
# Each entry is a regex matched against comment-stripped code.
# Patterns target function-call forms (identifier + open paren) to avoid
# false positives on comments, string literals, or include paths.
# ---------------------------------------------------------------------------

_FOREIGN_PLATFORM_PATTERNS: dict[str, list[str]] = {
    "STM32_HAL": [
        r"\bHAL_\w+\s*\(",       # HAL_GPIO_WritePin(, HAL_I2C_Init(, ...
        r"\bLL_\w+\s*\(",        # LL_GPIO_SetOutputPin(, ...
        r"\b__HAL_\w+\s*\(",     # __HAL_RCC_GPIOA_CLK_ENABLE(, ...
    ],
    "Zephyr": [
        r"\bk_\w+\s*\(",         # k_sleep(, k_sem_take(, ...
        r"\bDEVICE_DT_GET\s*\(", # Zephyr devicetree macro
        r"\bgpio_pin_configure\s*\(",
        r"\bi2c_write_read\s*\(",
    ],
    "Arduino": [
        r"\bdigitalWrite\s*\(",
        r"\bpinMode\s*\(",
        r"\banalogRead\s*\(",
        r"\bSerial\.",
    ],
    "FreeRTOS": [
        r"\bxTaskCreate\s*\(",
        r"\bvTaskDelay\s*\(",
        r"\bxQueueCreate\s*\(",
        r"\bxSemaphoreCreateBinary\s*\(",
    ],
    "ESP-IDF": [
        r"\besp_\w+\s*\(",       # esp_err_t, esp_log, ...
    ],
}


def no_nxp_hallucination(code: str) -> list[str]:
    """Return foreign-platform API tokens found in NXP bare-metal code.

    @brief Scans for STM32 HAL, Zephyr, Arduino, FreeRTOS, and ESP-IDF
           patterns that should never appear in MCUXpresso SDK code.
    @param code  Raw C source string (comments are stripped internally).
    @return      List of matched tokens. Empty list means no hallucination.
    """
    stripped = strip_comments(code)
    found: list[str] = []
    for platform, patterns in _FOREIGN_PLATFORM_PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, stripped)
            if match:
                # Report the matched token, not the full pattern.
                found.append(f"{match.group(0).strip()} [{platform}]")
    return found


# A function definition signature ("ret_type name(args) {") or a forward
# declaration ("ret_type name(args);") is NOT a call site. Models that write
# idiomatic, SDK-style code (helpers like BOARD_InitPins, a forward-declared
# wrapper such as I2C_MasterInit) would otherwise make the init function's name
# appear textually before the clock/pin-mux setup, even though at run time the
# setup is called first from main(). The official SDK examples are written the
# same way (clock gate lives in pin_mux.c::BOARD_InitPins). So ordering must be
# judged on CALL order, not on definition/declaration position.
#
# We blank out signatures and forward declarations before searching, leaving
# only call sites. Blanking (replacing with spaces) preserves byte offsets so
# the relative ordering of the surviving call sites is unchanged.
def _blank_function_signatures(stripped: str, name: str) -> str:
    """Replace forward declarations and the definition signature of ``name``
    with spaces, so a later position search only finds genuine call sites.

    @param stripped  Comment-stripped C source.
    @param name      Function name whose decl/def signature should be ignored.
    @return The source with ``name``'s signatures blanked (offsets preserved).
    """
    escaped = re.escape(name)
    # Matches a return-type token (one or more identifiers/pointers) directly
    # in front of "name(args)" followed by "{" (definition) or ";" (forward
    # declaration). A bare call "name(args);" has no return type in front of
    # it, so it is not matched here.
    signature_re = re.compile(
        rf"\b(?:[A-Za-z_]\w*[ \t\*\n]+)+{escaped}\s*\([^;{{}}]*\)\s*[;{{]"
    )

    def _blank(match: re.Match) -> str:
        return " " * (match.end() - match.start())

    return signature_re.sub(_blank, stripped)


def _first_call_pos(stripped: str, name: str) -> int | None:
    """Return the offset of the first genuine call to ``name``, or None.

    Forward declarations and the definition signature of ``name`` are ignored.
    """
    cleaned = _blank_function_signatures(stripped, name)
    match = re.search(rf"\b{re.escape(name)}\s*\(", cleaned)
    return match.start() if match else None


def has_clock_gate_before(code: str, peripheral_init: str) -> bool:
    """Check that a CLOCK_EnableClock call appears before peripheral init.

    @brief Verifies the MCUXpresso SDK clock-gate-before-init invariant:
           CLOCK_EnableClock() must precede the first peripheral init CALL.
           Ordering is judged on call sites, ignoring forward declarations and
           the wrapper's own definition signature (see _blank_function_signatures).
           This is implicit domain knowledge — prompts must not mention it.
    @param code             Raw C source string.
    @param peripheral_init  Function name to check ordering against,
                            e.g. "I2C_MasterInit", "SPI_MasterInit".
    @return True if CLOCK_EnableClock appears before the peripheral init call,
            True if the peripheral init is not called (nothing to check),
            False if CLOCK_EnableClock is absent or appears after.
    """
    stripped = strip_comments(code)

    clock_match = re.search(r"\bCLOCK_EnableClock\s*\(", stripped)
    init_pos = _first_call_pos(stripped, peripheral_init)

    # Nothing to check if the peripheral init is not called.
    if init_pos is None:
        return True

    # Clock gate must be present and positioned before the init call.
    if clock_match is None:
        return False

    return clock_match.start() < init_pos


def has_iomuxc_before_init(code: str, peripheral_init: str) -> bool:
    """Check that an IOMUXC_*SetPinMux call appears before peripheral init.

    @brief RT1170 (i.MX RT) variant of the pin-mux-before-init invariant:
           pads are muxed via IOMUXC_SetPinMux / IOMUXC_LPSR_SetPinMux,
           not the Kinetis PORT_SetPinMux API. Ordering is judged on the
           init CALL site, ignoring forward declarations / definition
           signatures (see _blank_function_signatures).
    @param code             Raw C source string.
    @param peripheral_init  Function name to check ordering against,
                            e.g. "GPIO_PinInit", "LPI2C_MasterInit".
    @return True if IOMUXC mux appears before peripheral_init,
            True if peripheral_init is absent (nothing to check),
            False if IOMUXC mux is absent or appears after.
    """
    stripped = strip_comments(code)

    mux_match = re.search(r"\bIOMUXC\w*_SetPinMux\s*\(", stripped)
    init_pos = _first_call_pos(stripped, peripheral_init)

    if init_pos is None:
        return True

    if mux_match is None:
        return False

    return mux_match.start() < init_pos


def has_rt1170_clock_root_config(code: str) -> bool:
    """Check that an RT1170 peripheral clock root is configured.

    @brief The i.MX RT1170 SDK offers several valid ways to set a peripheral
           clock root; this accepts any of them instead of forcing one literal
           API. Requiring only ``CLOCK_SetRootClock`` produced false negatives
           for correct solutions using the split mux/div form or a board clock
           init wrapper.
    @param code  Raw C source string (comments stripped internally).
    @return True if any recognised clock-root configuration call is present.

    Accepted forms:
      - CLOCK_SetRootClock(root, &config)        (single-call form)
      - CLOCK_SetRootClockMux / CLOCK_SetRootClockDiv  (split form)
      - CLOCK_SetMux / CLOCK_SetDiv               (low-level form)
      - BOARD_BootClockRUN() / BOARD_InitBootClocks()  (board wrapper)
    """
    stripped = strip_comments(code)
    return bool(re.search(
        r"\bCLOCK_Set(?:RootClock(?:Mux|Div)?|Mux|Div)\s*\("
        r"|\bBOARD_(?:BootClockRUN|InitBootClocks)\w*\s*\(",
        stripped,
    ))


# ---------------------------------------------------------------------------
# Cortex-M7 (RT1170) D-cache coherency tokens.
#
# DMA on a cached core requires either explicit cache maintenance or
# buffers placed in a non-cacheable section. Case checks accept any of
# these strategies via dcache_tokens_found().
# ---------------------------------------------------------------------------

DCACHE_CLEAN_APIS: list[str] = [
    "SCB_CleanDCache_by_Addr",
    "SCB_CleanInvalidateDCache_by_Addr",
    "L1CACHE_CleanDCacheByRange",
    "DCACHE_CleanByRange",
]

DCACHE_INVALIDATE_APIS: list[str] = [
    "SCB_InvalidateDCache_by_Addr",
    "SCB_CleanInvalidateDCache_by_Addr",
    "L1CACHE_InvalidateDCacheByRange",
    "DCACHE_InvalidateByRange",
]

NONCACHEABLE_MACROS: list[str] = [
    "AT_NONCACHEABLE_SECTION",
]


def dcache_tokens_found(code: str) -> dict[str, bool]:
    """Report which D-cache coherency strategies appear in the code.

    @brief Scans comment-stripped code for cache clean / invalidate calls
           and non-cacheable section macros.
    @param code  Raw C source string.
    @return dict with keys "clean", "invalidate", "noncacheable".
    """
    stripped = strip_comments(code)
    return {
        "clean": any(api in stripped for api in DCACHE_CLEAN_APIS),
        "invalidate": any(api in stripped for api in DCACHE_INVALIDATE_APIS),
        "noncacheable": any(m in stripped for m in NONCACHEABLE_MACROS),
    }


def has_pinmux_before_init(code: str, peripheral_init: str) -> bool:
    """Check that a PORT_SetPin* call appears before peripheral init.

    @brief Verifies the MCUXpresso SDK pin-mux-before-init invariant:
           PORT_SetPinMux() (or any PORT_SetPin* variant) must precede
           the first peripheral init CALL. Ordering ignores forward
           declarations / definition signatures (see _blank_function_signatures).
    @param code             Raw C source string.
    @param peripheral_init  Function name to check ordering against,
                            e.g. "I2C_MasterInit", "GPIO_PinInit".
    @return True if PORT_SetPin* appears before peripheral_init,
            True if peripheral_init is absent (nothing to check),
            False if PORT_SetPin* is absent or appears after.
    """
    stripped = strip_comments(code)

    pinmux_match = re.search(r"\bPORT_SetPin\w+\s*\(", stripped)
    init_pos = _first_call_pos(stripped, peripheral_init)

    if init_pos is None:
        return True

    if pinmux_match is None:
        return False

    return pinmux_match.start() < init_pos
