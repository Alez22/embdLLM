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


def has_clock_gate_before(code: str, peripheral_init: str) -> bool:
    """Check that a CLOCK_EnableClock call appears before peripheral init.

    @brief Verifies the MCUXpresso SDK clock-gate-before-init invariant:
           CLOCK_EnableClock() must precede the first peripheral init call.
           This is implicit domain knowledge — prompts must not mention it.
    @param code             Raw C source string.
    @param peripheral_init  Function name to check ordering against,
                            e.g. "I2C_MasterInit", "SPI_MasterInit".
    @return True if CLOCK_EnableClock appears before peripheral_init,
            True if peripheral_init is absent (nothing to check),
            False if CLOCK_EnableClock is absent or appears after.
    """
    stripped = strip_comments(code)

    clock_match = re.search(r"\bCLOCK_EnableClock\s*\(", stripped)
    init_match = re.search(
        rf"\b{re.escape(peripheral_init)}\s*\(", stripped
    )

    # Nothing to check if the peripheral init is not present.
    if init_match is None:
        return True

    # Clock gate must be present and positioned before the init call.
    if clock_match is None:
        return False

    return clock_match.start() < init_match.start()


def has_iomuxc_before_init(code: str, peripheral_init: str) -> bool:
    """Check that an IOMUXC_*SetPinMux call appears before peripheral init.

    @brief RT1170 (i.MX RT) variant of the pin-mux-before-init invariant:
           pads are muxed via IOMUXC_SetPinMux / IOMUXC_LPSR_SetPinMux,
           not the Kinetis PORT_SetPinMux API.
    @param code             Raw C source string.
    @param peripheral_init  Function name to check ordering against,
                            e.g. "GPIO_PinInit", "LPI2C_MasterInit".
    @return True if IOMUXC mux appears before peripheral_init,
            True if peripheral_init is absent (nothing to check),
            False if IOMUXC mux is absent or appears after.
    """
    stripped = strip_comments(code)

    mux_match = re.search(r"\bIOMUXC\w*_SetPinMux\s*\(", stripped)
    init_match = re.search(
        rf"\b{re.escape(peripheral_init)}\s*\(", stripped
    )

    if init_match is None:
        return True

    if mux_match is None:
        return False

    return mux_match.start() < init_match.start()


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
           the first peripheral init call.
    @param code             Raw C source string.
    @param peripheral_init  Function name to check ordering against,
                            e.g. "I2C_MasterInit", "GPIO_PinInit".
    @return True if PORT_SetPin* appears before peripheral_init,
            True if peripheral_init is absent (nothing to check),
            False if PORT_SetPin* is absent or appears after.
    """
    stripped = strip_comments(code)

    pinmux_match = re.search(r"\bPORT_SetPin\w+\s*\(", stripped)
    init_match = re.search(
        rf"\b{re.escape(peripheral_init)}\s*\(", stripped
    )

    if init_match is None:
        return True

    if pinmux_match is None:
        return False

    return pinmux_match.start() < init_match.start()
