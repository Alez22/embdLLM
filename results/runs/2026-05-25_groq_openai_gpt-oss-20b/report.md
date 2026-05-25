# Benchmark Report: groq/openai/gpt-oss-20b

**Date:** 2026-05-25 21:18 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/openai/gpt-oss-20b |
| Total Cases | 1 |
| Passed | 0 |
| Failed | 1 |
| pass@1 | 0.0% |

## Failed Cases (1)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | i2c_master_init_called, i2c_blocking_transfer_used |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `i2c_master_init_called` | 1 | nxp-mcxc-i2c-001 |
| `i2c_blocking_transfer_used` | 1 | nxp-mcxc-i2c-001 |

## TC Improvement Suggestions

