# Benchmark Report: groq/openai/gpt-oss-120b

**Date:** 2026-05-25 21:53 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/openai/gpt-oss-120b |
| Total Cases | 11 |
| Passed | 5 |
| Failed | 6 |
| pass@1 | 45.5% |

## Failed Cases (6)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `esp-gpio-001` | gpio-basic | static_analysis | gpio_config_used |
| `esp-i2c-001` | spi-i2c | static_analysis | i2c_master_header, i2c_master_new_api, no_legacy_i2c_driver, no_zephyr_apis |
| `esp-wifi-001` | networking | static_analysis | event_handler_registered |
| `stm32-freertos-001` | threading | static_heuristic | different_task_priorities |
| `stm32-i2c-001` | spi-i2c | static_analysis | i2c_clock_enabled |
| `stm32-spi-001` | spi-i2c | static_analysis | spi_clock_enabled |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `gpio_config_used` | 1 | esp-gpio-001 |
| `i2c_master_header` | 1 | esp-i2c-001 |
| `i2c_master_new_api` | 1 | esp-i2c-001 |
| `no_legacy_i2c_driver` | 1 | esp-i2c-001 |
| `no_zephyr_apis` | 1 | esp-i2c-001 |
| `event_handler_registered` | 1 | esp-wifi-001 |
| `different_task_priorities` | 1 | stm32-freertos-001 |
| `i2c_clock_enabled` | 1 | stm32-i2c-001 |
| `spi_clock_enabled` | 1 | stm32-spi-001 |

## TC Improvement Suggestions

