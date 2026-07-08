# Benchmark Report: openrouter/anthropic/claude-sonnet-4.6

**Date:** 2026-06-17 19:08 UTC

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
| `nxp-mcxc-flash-001` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-timer-001` | timer | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | static_heuristic | critical_section_around_read |
| `nxp-rt1170-lpi2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpspi-001` | spi-i2c | static_heuristic | clock_root_configured |
| `nxp-rt1170-lpuart-001` | uart | static_heuristic | init_status_checked |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_write_api_used |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `nxp_gcc` | 17 | nxp-mcxc-flash-001, nxp-mcxc-flash-002, nxp-mcxc-gpio-001, nxp-mcxc-i2c-001, nxp-mcxc-i2c-002 (+12 more) |
| `interrupt_flag_cleared` | 1 | nxp-mcxc-gpio-002 |
| `uart_isr_handler_defined` | 1 | nxp-mcxc-uart-002 |
| `read_and_write_api_used` | 1 | nxp-rt1170-audio-001 |
| `critical_section_around_read` | 1 | nxp-rt1170-isr-001 |
| `clock_root_configured` | 1 | nxp-rt1170-lpspi-001 |
| `init_status_checked` | 1 | nxp-rt1170-lpuart-001 |
| `sai_init_called` | 1 | nxp-rt1170-sai-001 |
| `sai_write_api_used` | 1 | nxp-rt1170-sai-001 |

## TC Improvement Suggestions

