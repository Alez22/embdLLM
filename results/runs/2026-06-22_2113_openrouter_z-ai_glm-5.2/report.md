# Benchmark Report: openrouter/z-ai/glm-5.2

**Date:** 2026-06-22 21:13 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/z-ai/glm-5.2 |
| Total Cases | 24 |
| Passed | 2 |
| Failed | 22 |
| pass@1 | 8.3% |

## Failed Cases (22)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-timer-001` | timer | static_analysis | pit_isr_defined |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-audio-001` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_heuristic | clock_root_configured |
| `nxp-rt1170-lpspi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, lpi2c_blocking_transfer_used |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `nxp_gcc` | 16 | nxp-mcxc-flash-002, nxp-mcxc-i2c-001, nxp-mcxc-i2c-002, nxp-mcxc-isr-001, nxp-mcxc-spi-001 (+11 more) |
| `flash_verify_program_called` | 1 | nxp-mcxc-flash-001 |
| `interrupt_flag_cleared` | 1 | nxp-mcxc-gpio-002 |
| `pit_isr_defined` | 1 | nxp-mcxc-timer-001 |
| `uart_isr_handler_defined` | 1 | nxp-mcxc-uart-002 |
| `clock_root_configured` | 1 | nxp-rt1170-lpi2c-001 |
| `sai_init_called` | 1 | nxp-rt1170-sai-001 |
| `lpi2c_blocking_transfer_used` | 1 | nxp-rt1170-sai-001 |

## TC Improvement Suggestions

