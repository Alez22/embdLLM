# Benchmark Report: openrouter/openai/gpt-oss-120b

**Date:** 2026-06-22 23:11 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/openai/gpt-oss-120b |
| Total Cases | 24 |
| Passed | 0 |
| Failed | 24 |
| pass@1 | 0.0% |

## Failed Cases (24)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-002` | storage | static_analysis | two_flash_slots_defined |
| `nxp-mcxc-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | pin_interrupt_configured, interrupt_flag_cleared |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-timer-001` | timer | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-audio-001` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | falling_edge_configured |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-rt1170-lpi2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpspi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `nxp_gcc` | 16 | nxp-mcxc-gpio-001, nxp-mcxc-i2c-001, nxp-mcxc-spi-001, nxp-mcxc-timer-001, nxp-mcxc-uart-001 (+11 more) |
| `flash_verify_program_called` | 1 | nxp-mcxc-flash-001 |
| `two_flash_slots_defined` | 1 | nxp-mcxc-flash-002 |
| `pin_interrupt_configured` | 1 | nxp-mcxc-gpio-002 |
| `interrupt_flag_cleared` | 1 | nxp-mcxc-gpio-002 |
| `header_fsl_port_h` | 1 | nxp-mcxc-i2c-002 |
| `pit_isr_defined` | 1 | nxp-mcxc-isr-001 |
| `uart_isr_handler_defined` | 1 | nxp-mcxc-uart-002 |
| `falling_edge_configured` | 1 | nxp-rt1170-gpio-002 |
| `sai_init_called` | 1 | nxp-rt1170-sai-001 |

## TC Improvement Suggestions

