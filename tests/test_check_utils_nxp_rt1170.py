"""Tests for the RT1170 helpers in check_utils_nxp."""

from embedeval.check_utils_nxp import dcache_tokens_found, has_iomuxc_before_init


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
