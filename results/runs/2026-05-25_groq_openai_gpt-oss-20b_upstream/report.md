# Benchmark Report: groq/openai/gpt-oss-20b

**Date:** 2026-05-25 21:58 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/openai/gpt-oss-20b |
| Total Cases | 11 |
| Passed | 7 |
| Failed | 4 |
| pass@1 | 63.6% |

## Failed Cases (4)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `esp-i2c-001` | spi-i2c | static_analysis | i2c_master_header, i2c_master_new_api, no_legacy_i2c_driver |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | header_fsl_i2c_h, header_fsl_port_h, header_fsl_clock_h, i2c_master_init_called, i2c_blocking_transfer_used |
| `stm32-i2c-001` | spi-i2c | static_analysis | i2c_clock_enabled |
| `stm32-uart-001` | networking | static_analysis | uart_clock_enabled |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `i2c_master_header` | 1 | esp-i2c-001 |
| `i2c_master_new_api` | 1 | esp-i2c-001 |
| `no_legacy_i2c_driver` | 1 | esp-i2c-001 |
| `header_fsl_i2c_h` | 1 | nxp-mcxc-i2c-001 |
| `header_fsl_port_h` | 1 | nxp-mcxc-i2c-001 |
| `header_fsl_clock_h` | 1 | nxp-mcxc-i2c-001 |
| `i2c_master_init_called` | 1 | nxp-mcxc-i2c-001 |
| `i2c_blocking_transfer_used` | 1 | nxp-mcxc-i2c-001 |
| `i2c_clock_enabled` | 1 | stm32-i2c-001 |
| `uart_clock_enabled` | 1 | stm32-uart-001 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 3 | esp-i2c-001, stm32-i2c-001, stm32-uart-001 |
| LLM format failure (prose) | 1 | nxp-mcxc-i2c-001 |

*Adjusted pass@1 (excluding format failures): 70.0% (7/10)*


## TC Improvement Suggestions

