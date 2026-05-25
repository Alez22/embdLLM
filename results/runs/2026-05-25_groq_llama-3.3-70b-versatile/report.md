# Benchmark Report: groq/llama-3.3-70b-versatile

**Date:** 2026-05-25 19:41 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/llama-3.3-70b-versatile |
| Total Cases | 3 |
| Passed | 0 |
| Failed | 3 |
| pass@1 | 0.0% |

## Failed Cases (3)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | header_fsl_port_h, header_fsl_clock_h, i2c_blocking_transfer_used |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | header_fsl_clock_h, i2c_master_init_called |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | header_fsl_port_h, header_fsl_clock_h, i2c_master_init_called, i2c_blocking_transfer_used |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `header_fsl_clock_h` | 3 | nxp-mcxc-i2c-001, nxp-mcxc-i2c-001, nxp-mcxc-i2c-001 |
| `header_fsl_port_h` | 2 | nxp-mcxc-i2c-001, nxp-mcxc-i2c-001 |
| `i2c_blocking_transfer_used` | 2 | nxp-mcxc-i2c-001, nxp-mcxc-i2c-001 |
| `i2c_master_init_called` | 2 | nxp-mcxc-i2c-001, nxp-mcxc-i2c-001 |

## TC Improvement Suggestions

