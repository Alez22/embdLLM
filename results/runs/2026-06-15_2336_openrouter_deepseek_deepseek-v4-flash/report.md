# Benchmark Report: openrouter/deepseek/deepseek-v4-flash

**Date:** 2026-06-15 23:36 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/deepseek/deepseek-v4-flash |
| Total Cases | 24 |
| Passed | 0 |
| Failed | 24 |
| pass@1 | 0.0% |

## Failed Cases (24)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | both_write_and_read_transfers, two_separate_transfers |
| `nxp-mcxc-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-timer-001` | timer | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | falling_edge_configured |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-rt1170-lpi2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpspi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_write_api_used |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `nxp_gcc` | 16 | nxp-mcxc-flash-002, nxp-mcxc-gpio-001, nxp-mcxc-i2c-001, nxp-mcxc-isr-001, nxp-mcxc-timer-001 (+11 more) |
| `flash_verify_program_called` | 1 | nxp-mcxc-flash-001 |
| `interrupt_flag_cleared` | 1 | nxp-mcxc-gpio-002 |
| `both_write_and_read_transfers` | 1 | nxp-mcxc-i2c-002 |
| `two_separate_transfers` | 1 | nxp-mcxc-i2c-002 |
| `header_fsl_port_h` | 1 | nxp-mcxc-spi-001 |
| `uart_isr_handler_defined` | 1 | nxp-mcxc-uart-002 |
| `read_and_write_api_used` | 1 | nxp-rt1170-audio-001 |
| `falling_edge_configured` | 1 | nxp-rt1170-gpio-002 |
| `sai_write_api_used` | 1 | nxp-rt1170-sai-001 |

## TC Improvement Suggestions

