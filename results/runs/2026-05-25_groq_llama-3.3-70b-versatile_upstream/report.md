# Benchmark Report: groq/llama-3.3-70b-versatile

**Date:** 2026-05-25 21:54 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/llama-3.3-70b-versatile |
| Total Cases | 11 |
| Passed | 4 |
| Failed | 7 |
| pass@1 | 36.4% |

## Failed Cases (7)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `esp-i2c-001` | spi-i2c | static_analysis | i2c_master_header, i2c_master_new_api, no_legacy_i2c_driver |
| `esp-spi-001` | spi-i2c | static_analysis | spi_master_header |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | header_fsl_port_h, header_fsl_clock_h, i2c_master_init_called |
| `stm32-gpio-001` | gpio-basic | static_heuristic | exti_callback_defined |
| `stm32-i2c-001` | spi-i2c | static_analysis | hal_i2c_mem_read_used, i2c_clock_enabled |
| `stm32-spi-001` | spi-i2c | static_analysis | spi_clock_enabled |
| `stm32-uart-001` | networking | static_analysis | uart_clock_enabled |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `i2c_master_header` | 1 | esp-i2c-001 |
| `i2c_master_new_api` | 1 | esp-i2c-001 |
| `no_legacy_i2c_driver` | 1 | esp-i2c-001 |
| `spi_master_header` | 1 | esp-spi-001 |
| `header_fsl_port_h` | 1 | nxp-mcxc-i2c-001 |
| `header_fsl_clock_h` | 1 | nxp-mcxc-i2c-001 |
| `i2c_master_init_called` | 1 | nxp-mcxc-i2c-001 |
| `exti_callback_defined` | 1 | stm32-gpio-001 |
| `hal_i2c_mem_read_used` | 1 | stm32-i2c-001 |
| `i2c_clock_enabled` | 1 | stm32-i2c-001 |
| `spi_clock_enabled` | 1 | stm32-spi-001 |
| `uart_clock_enabled` | 1 | stm32-uart-001 |

## TC Improvement Suggestions

