# Benchmark Report: groq/qwen/qwen3-32b

**Date:** 2026-05-25 20:14 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/qwen/qwen3-32b |
| Total Cases | 3 |
| Passed | 0 |
| Failed | 3 |
| pass@1 | 0.0% |

## Failed Cases (3)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | header_fsl_clock_h, i2c_master_init_called, i2c_blocking_transfer_used |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | header_fsl_port_h, header_fsl_clock_h, i2c_master_init_called |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | llm_call |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `header_fsl_clock_h` | 2 | nxp-mcxc-i2c-001, nxp-mcxc-i2c-001 |
| `i2c_master_init_called` | 2 | nxp-mcxc-i2c-001, nxp-mcxc-i2c-001 |
| `i2c_blocking_transfer_used` | 1 | nxp-mcxc-i2c-001 |
| `header_fsl_port_h` | 1 | nxp-mcxc-i2c-001 |
| `llm_call` | 1 | nxp-mcxc-i2c-001 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 1 | nxp-mcxc-i2c-001 |
| LLM format failure (prose) | 2 | nxp-mcxc-i2c-001, nxp-mcxc-i2c-001 |

*Adjusted pass@1 (excluding format failures): 0.0% (0/1)*


## TC Improvement Suggestions

