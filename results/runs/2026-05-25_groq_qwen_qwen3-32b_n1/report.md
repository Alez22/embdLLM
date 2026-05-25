# Benchmark Report: groq/qwen/qwen3-32b

**Date:** 2026-05-25 20:14 UTC

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
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | header_fsl_clock_h, i2c_blocking_transfer_used |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `header_fsl_clock_h` | 1 | nxp-mcxc-i2c-001 |
| `i2c_blocking_transfer_used` | 1 | nxp-mcxc-i2c-001 |

## TC Improvement Suggestions

