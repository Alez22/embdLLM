# Benchmark Report: openrouter/deepseek/deepseek-v4-pro

**Date:** 2026-06-24 16:24 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/deepseek/deepseek-v4-pro |
| Total Cases | 24 |
| Passed | 1 |
| Failed | 23 |
| pass@1 | 4.2% |

## Failed Cases (23)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-002` | storage | static_analysis | two_flash_slots_defined |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_port_h |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | i2c_blocking_transfer_used |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-timer-001` | timer | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-dma-001` | dma | static_analysis | edma_transfer_started |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpt-001` | timer | static_analysis | isr_handler_defined |
| `nxp-rt1170-lpi2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpspi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_write_api_used |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `nxp_gcc` | 13 | nxp-mcxc-i2c-002, nxp-mcxc-isr-001, nxp-mcxc-spi-001, nxp-mcxc-timer-001, nxp-mcxc-uart-001 (+8 more) |
| `flash_verify_program_called` | 1 | nxp-mcxc-flash-001 |
| `two_flash_slots_defined` | 1 | nxp-mcxc-flash-002 |
| `header_fsl_port_h` | 1 | nxp-mcxc-gpio-001 |
| `interrupt_flag_cleared` | 1 | nxp-mcxc-gpio-002 |
| `i2c_blocking_transfer_used` | 1 | nxp-mcxc-i2c-001 |
| `uart_isr_handler_defined` | 1 | nxp-mcxc-uart-002 |
| `read_and_write_api_used` | 1 | nxp-rt1170-audio-001 |
| `edma_transfer_started` | 1 | nxp-rt1170-dma-001 |
| `isr_handler_defined` | 1 | nxp-rt1170-gpt-001 |
| `sai_write_api_used` | 1 | nxp-rt1170-sai-001 |

## TC Improvement Suggestions

