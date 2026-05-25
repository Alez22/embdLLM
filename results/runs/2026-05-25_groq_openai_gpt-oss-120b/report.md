# Benchmark Report: groq/openai/gpt-oss-120b

**Date:** 2026-05-25 21:49 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/openai/gpt-oss-120b |
| Total Cases | 4 |
| Passed | 3 |
| Failed | 1 |
| pass@1 | 75.0% |

## Failed Cases (1)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `stm32-i2c-001` | spi-i2c | static_analysis | i2c_clock_enabled |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `i2c_clock_enabled` | 1 | stm32-i2c-001 |

## TC Improvement Suggestions

