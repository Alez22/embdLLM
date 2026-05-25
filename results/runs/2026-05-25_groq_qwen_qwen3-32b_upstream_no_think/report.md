# Benchmark Report: groq/qwen/qwen3-32b

**Date:** 2026-05-25 21:56 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/qwen/qwen3-32b |
| Total Cases | 11 |
| Passed | 4 |
| Failed | 7 |
| pass@1 | 36.4% |

## Failed Cases (7)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `esp-i2c-001` | spi-i2c | static_analysis | i2c_master_header, i2c_master_new_api, no_legacy_i2c_driver, no_zephyr_apis |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | header_fsl_clock_h |
| `stm32-freertos-001` | threading | static_analysis | stm32_hal_header_included |
| `stm32-gpio-001` | gpio-basic | static_analysis | nvic_configured |
| `stm32-i2c-001` | spi-i2c | static_analysis | hal_i2c_mem_read_used, i2c_clock_enabled |
| `stm32-spi-001` | spi-i2c | static_analysis | spi_clock_enabled |
| `stm32-uart-001` | networking | static_analysis | uart_clock_enabled |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `i2c_master_header` | 1 | esp-i2c-001 |
| `i2c_master_new_api` | 1 | esp-i2c-001 |
| `no_legacy_i2c_driver` | 1 | esp-i2c-001 |
| `no_zephyr_apis` | 1 | esp-i2c-001 |
| `stm32_hal_header_included` | 1 | stm32-freertos-001 |
| `header_fsl_clock_h` | 1 | nxp-mcxc-i2c-001 |
| `nvic_configured` | 1 | stm32-gpio-001 |
| `hal_i2c_mem_read_used` | 1 | stm32-i2c-001 |
| `i2c_clock_enabled` | 1 | stm32-i2c-001 |
| `spi_clock_enabled` | 1 | stm32-spi-001 |
| `uart_clock_enabled` | 1 | stm32-uart-001 |

## TC Improvement Suggestions

