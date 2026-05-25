# Benchmark Report: groq/qwen/qwen3-32b

**Date:** 2026-05-25 21:02 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/qwen/qwen3-32b |
| Total Cases | 1 |
| Passed | 0 |
| Failed | 1 |
| pass@1 | 0.0% |

## Failed Cases (1)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | header_fsl_i2c_h, header_fsl_port_h, header_fsl_clock_h, i2c_master_init_called, i2c_blocking_transfer_used |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `header_fsl_i2c_h` | 1 | nxp-mcxc-i2c-001 |
| `header_fsl_port_h` | 1 | nxp-mcxc-i2c-001 |
| `header_fsl_clock_h` | 1 | nxp-mcxc-i2c-001 |
| `i2c_master_init_called` | 1 | nxp-mcxc-i2c-001 |
| `i2c_blocking_transfer_used` | 1 | nxp-mcxc-i2c-001 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 0 |  |
| LLM format failure (prose) | 1 | nxp-mcxc-i2c-001 |


## TC Improvement Suggestions

