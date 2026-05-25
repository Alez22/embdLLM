# Benchmark Report: groq/meta-llama/llama-4-scout-17b-16e-instruct

**Date:** 2026-05-25 21:55 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/meta-llama/llama-4-scout-17b-16e-instruct |
| Total Cases | 11 |
| Passed | 2 |
| Failed | 9 |
| pass@1 | 18.2% |

## Failed Cases (9)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `esp-gpio-001` | gpio-basic | static_heuristic | gpio_config_error_checked |
| `esp-i2c-001` | spi-i2c | static_analysis | i2c_master_header, i2c_master_new_api, no_legacy_i2c_driver |
| `esp-spi-001` | spi-i2c | static_heuristic | dma_channel_specified |
| `esp-wifi-001` | networking | static_analysis | event_handler_registered |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | header_fsl_port_h, header_fsl_clock_h, i2c_blocking_transfer_used |
| `stm32-freertos-001` | threading | static_analysis | stm32_hal_header_included |
| `stm32-i2c-001` | spi-i2c | static_analysis | hal_i2c_mem_read_used |
| `stm32-spi-001` | spi-i2c | static_analysis | software_nss_used, no_cross_platform_hallucination |
| `stm32-uart-001` | networking | static_heuristic | uart_clock_before_init |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `gpio_config_error_checked` | 1 | esp-gpio-001 |
| `i2c_master_header` | 1 | esp-i2c-001 |
| `i2c_master_new_api` | 1 | esp-i2c-001 |
| `no_legacy_i2c_driver` | 1 | esp-i2c-001 |
| `dma_channel_specified` | 1 | esp-spi-001 |
| `event_handler_registered` | 1 | esp-wifi-001 |
| `stm32_hal_header_included` | 1 | stm32-freertos-001 |
| `header_fsl_port_h` | 1 | nxp-mcxc-i2c-001 |
| `header_fsl_clock_h` | 1 | nxp-mcxc-i2c-001 |
| `i2c_blocking_transfer_used` | 1 | nxp-mcxc-i2c-001 |
| `hal_i2c_mem_read_used` | 1 | stm32-i2c-001 |
| `software_nss_used` | 1 | stm32-spi-001 |
| `no_cross_platform_hallucination` | 1 | stm32-spi-001 |
| `uart_clock_before_init` | 1 | stm32-uart-001 |

## TC Improvement Suggestions

