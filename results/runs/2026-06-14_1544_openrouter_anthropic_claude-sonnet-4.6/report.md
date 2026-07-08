# Benchmark Report: openrouter/anthropic/claude-sonnet-4.6

**Date:** 2026-06-14 15:44 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/anthropic/claude-sonnet-4.6 |
| Total Cases | 24 |
| Passed | 0 |
| Failed | 24 |
| pass@1 | 0.0% |

## Failed Cases (24)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | llm_call |
| `nxp-mcxc-flash-002` | storage | static_analysis | llm_call |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | llm_call |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | llm_call |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | llm_call |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | llm_call |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | llm_call |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | llm_call |
| `nxp-mcxc-timer-001` | timer | static_analysis | llm_call |
| `nxp-mcxc-uart-001` | uart | static_analysis | llm_call |
| `nxp-mcxc-uart-002` | uart | static_analysis | llm_call |
| `nxp-mcxc-watchdog-001` | watchdog | static_analysis | llm_call |
| `nxp-rt1170-audio-001` | audio | static_analysis | llm_call |
| `nxp-rt1170-dma-001` | dma | static_analysis | llm_call |
| `nxp-rt1170-gpio-001` | gpio-basic | static_analysis | llm_call |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | llm_call |
| `nxp-rt1170-gpt-001` | timer | static_analysis | llm_call |
| `nxp-rt1170-isr-001` | isr-concurrency | static_analysis | llm_call |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_analysis | llm_call |
| `nxp-rt1170-lpspi-001` | spi-i2c | static_analysis | llm_call |
| `nxp-rt1170-lpuart-001` | uart | static_analysis | llm_call |
| `nxp-rt1170-rtwdog-001` | watchdog | static_analysis | llm_call |
| `nxp-rt1170-sai-001` | audio | static_analysis | llm_call |
| `nxp-rt1170-sai-002` | audio | static_analysis | llm_call |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `llm_call` | 24 | nxp-mcxc-flash-001, nxp-mcxc-flash-002, nxp-mcxc-gpio-001, nxp-mcxc-gpio-002, nxp-mcxc-i2c-001 (+19 more) |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 0 |  |
| LLM format failure (prose) | 24 | nxp-mcxc-flash-001, nxp-mcxc-flash-002, nxp-mcxc-gpio-001, nxp-mcxc-gpio-002, nxp-mcxc-i2c-001, nxp-mcxc-i2c-002, nxp-mcxc-isr-001, nxp-mcxc-spi-001, nxp-mcxc-timer-001, nxp-mcxc-uart-001, nxp-mcxc-uart-002, nxp-mcxc-watchdog-001, nxp-rt1170-audio-001, nxp-rt1170-dma-001, nxp-rt1170-gpio-001, nxp-rt1170-gpio-002, nxp-rt1170-gpt-001, nxp-rt1170-isr-001, nxp-rt1170-lpi2c-001, nxp-rt1170-lpspi-001, nxp-rt1170-lpuart-001, nxp-rt1170-rtwdog-001, nxp-rt1170-sai-001, nxp-rt1170-sai-002 |


## TC Improvement Suggestions

