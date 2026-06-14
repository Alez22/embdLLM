"""Tests for the RT1170 helpers in check_utils_nxp."""

from embedeval.check_utils_nxp import (
    dcache_tokens_found,
    has_clock_gate_before,
    has_iomuxc_before_init,
    has_pinmux_before_init,
)


class TestHasIomuxcBeforeInit:
    def test_correct_order(self):
        code = (
            "IOMUXC_SetPinMux(IOMUXC_GPIO_AD_04_GPIO9_IO03, 0U);\n"
            "GPIO_PinInit(GPIO9, 3U, &cfg);\n"
        )
        assert has_iomuxc_before_init(code, "GPIO_PinInit") is True

    def test_wrong_order(self):
        code = (
            "GPIO_PinInit(GPIO9, 3U, &cfg);\n"
            "IOMUXC_SetPinMux(IOMUXC_GPIO_AD_04_GPIO9_IO03, 0U);\n"
        )
        assert has_iomuxc_before_init(code, "GPIO_PinInit") is False

    def test_mux_missing(self):
        code = "GPIO_PinInit(GPIO9, 3U, &cfg);\n"
        assert has_iomuxc_before_init(code, "GPIO_PinInit") is False

    def test_init_absent_passes(self):
        # Nothing to check when the peripheral init is not present.
        code = "int main(void) { return 0; }\n"
        assert has_iomuxc_before_init(code, "GPIO_PinInit") is True

    def test_lpsr_variant_matches(self):
        code = (
            "IOMUXC_LPSR_SetPinMux(IOMUXC_GPIO_LPSR_04_LPI2C5_SCL, 1U);\n"
            "LPI2C_MasterInit(LPI2C5, &cfg, freq);\n"
        )
        assert has_iomuxc_before_init(code, "LPI2C_MasterInit") is True

    def test_mux_in_comment_ignored(self):
        code = (
            "/* IOMUXC_SetPinMux would go here */\n"
            "GPIO_PinInit(GPIO9, 3U, &cfg);\n"
        )
        assert has_iomuxc_before_init(code, "GPIO_PinInit") is False


# Regression tests for the Class A fix (docs/NXP_CASE_AUDIT.md): ordering must
# be judged on CALL order, not on the textual position of a forward declaration
# or a function definition signature. SDK-idiomatic code structured into helper
# functions (BOARD_InitPins, a forward-declared wrapper) used to fail at 0%.

# A realistic, correct, SDK-style program mirroring actual model output
# (e.g. Sonnet 4.6 on nxp-mcxc-i2c-001): forward declarations up top, helper
# definitions (clock/pinmux) before the init wrapper, and the real SDK init
# call living inside the wrapper after the setup. The init function NAME first
# appears in the forward declaration — which must be ignored — while the real
# SDK init CALL comes after CLOCK_EnableClock / PORT_SetPinMux.
_STRUCTURED_CORRECT = """
static void BOARD_InitPins(void);       /* forward declarations */
static void BOARD_InitClock(void);
static status_t I2C_MasterInit(void);

static void BOARD_InitPins(void) {
    CLOCK_EnableClock(kCLOCK_PortC);
    PORT_SetPinMux(PORTC, 1U, kPORT_MuxAlt2);
}

static void BOARD_InitClock(void) {
    CLOCK_EnableClock(kCLOCK_I2c0);
}

static status_t I2C_MasterInit(void) {  /* definition signature */
    i2c_master_config_t cfg;
    I2C_MasterGetDefaultConfig(&cfg);
    I2C_MasterInit(I2C0, &cfg, freq);   /* real SDK init call, after setup */
    return kStatus_Success;
}

int main(void) {
    BOARD_InitClock();
    BOARD_InitPins();
    I2C_MasterInit();
    return 0;
}
"""

# Genuinely wrong: the init helper (with the real SDK init call) is defined
# before any clock/pinmux setup, so the first init CALL precedes the setup.
_STRUCTURED_WRONG = """
static status_t I2C_MasterInit(void);
static void BOARD_InitPins(void);

static status_t I2C_MasterInit(void) {
    i2c_master_config_t cfg;
    I2C_MasterInit(I2C0, &cfg, freq);   /* init call before any setup */
    return kStatus_Success;
}

static void BOARD_InitPins(void) {
    CLOCK_EnableClock(kCLOCK_PortC);
    PORT_SetPinMux(PORTC, 1U, kPORT_MuxAlt2);
}

int main(void) {
    I2C_MasterInit();
    BOARD_InitPins();
    return 0;
}
"""


class TestClassAOrderingFix:
    """Forward declarations and definition signatures must not count as calls."""

    def test_clock_gate_structured_correct(self):
        # CLOCK_EnableClock (in BOARD_InitPins) is called before the init
        # wrapper in main(), even though I2C_MasterInit's name appears earlier.
        assert has_clock_gate_before(_STRUCTURED_CORRECT, "I2C_MasterInit") is True

    def test_pinmux_structured_correct(self):
        assert has_pinmux_before_init(_STRUCTURED_CORRECT, "I2C_MasterInit") is True

    def test_clock_gate_structured_wrong(self):
        assert has_clock_gate_before(_STRUCTURED_WRONG, "I2C_MasterInit") is False

    def test_pinmux_structured_wrong(self):
        assert has_pinmux_before_init(_STRUCTURED_WRONG, "I2C_MasterInit") is False

    def test_forward_decl_only_is_not_a_call(self):
        # Only a forward declaration, no actual call → nothing to check → True.
        code = (
            "static status_t LPI2C_MasterInit(void);\n"
            "int main(void) { return 0; }\n"
        )
        assert has_clock_gate_before(code, "LPI2C_MasterInit") is True

    def test_iomuxc_structured_correct(self):
        code = """
static void GPIO_PinInit_wrapper(void);

static void BOARD_InitPins(void) {
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_04_GPIO9_IO03, 0U);
}

void GPIO_PinInit(GPIO_Type *base, uint32_t pin, const gpio_pin_config_t *c) {
    /* real driver call lives here */
    GPIO_PinInit(base, pin, c);
}

int main(void) {
    BOARD_InitPins();
    GPIO_PinInit(GPIO9, 3U, &cfg);
    return 0;
}
"""
        assert has_iomuxc_before_init(code, "GPIO_PinInit") is True

    def test_inline_main_still_works(self):
        # The simple inline form (no helper functions) must keep working.
        code = (
            "int main(void) {\n"
            "    CLOCK_EnableClock(kCLOCK_PortC);\n"
            "    PORT_SetPinMux(PORTC, 1U, kPORT_MuxAlt2);\n"
            "    I2C_MasterInit(I2C0, &cfg, freq);\n"
            "    return 0;\n"
            "}\n"
        )
        assert has_clock_gate_before(code, "I2C_MasterInit") is True
        assert has_pinmux_before_init(code, "I2C_MasterInit") is True


class TestDcacheTokensFound:
    def test_clean_and_invalidate(self):
        code = (
            "SCB_CleanDCache_by_Addr((uint32_t *)src, 512);\n"
            "SCB_InvalidateDCache_by_Addr((uint32_t *)dst, 512);\n"
        )
        found = dcache_tokens_found(code)
        assert found["clean"] is True
        assert found["invalidate"] is True
        assert found["noncacheable"] is False

    def test_clean_invalidate_counts_as_both(self):
        code = "SCB_CleanInvalidateDCache_by_Addr((uint32_t *)buf, 512);\n"
        found = dcache_tokens_found(code)
        assert found["clean"] is True
        assert found["invalidate"] is True

    def test_noncacheable_section(self):
        code = "AT_NONCACHEABLE_SECTION_ALIGN(static uint8_t buf[512], 32U);\n"
        assert dcache_tokens_found(code)["noncacheable"] is True

    def test_tokens_in_comments_ignored(self):
        code = "/* remember: SCB_CleanDCache_by_Addr before DMA */\nint x;\n"
        found = dcache_tokens_found(code)
        assert found["clean"] is False
        assert found["invalidate"] is False

    def test_nothing_found(self):
        code = "int main(void) { return 0; }\n"
        found = dcache_tokens_found(code)
        assert not any(found.values())
