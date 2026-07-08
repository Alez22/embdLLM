# Benchmark Report: openrouter/deepseek/deepseek-v4-flash

**Date:** 2026-06-15 22:28 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/deepseek/deepseek-v4-flash |
| Total Cases | 24 |
| Passed | 6 |
| Failed | 18 |
| pass@1 | 25.0% |

## Failed Cases (18)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-002` | storage | static_heuristic | verify_after_each_write |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | header_fsl_clock_h, interrupt_flag_cleared |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-isr-001` | isr-concurrency | static_heuristic | nvic_pit_enabled |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h, header_fsl_clock_h |
| `nxp-mcxc-timer-001` | timer | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-uart-001` | uart | static_analysis | header_fsl_port_h, header_fsl_clock_h |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-watchdog-001` | watchdog | static_heuristic | long_timeout_configured |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-dma-001` | dma | static_analysis | edma_transfer_prepared |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_heuristic | clock_root_configured, transfer_return_value_checked |
| `nxp-rt1170-lpspi-001` | spi-i2c | static_heuristic | clock_root_configured, transfer_status_checked |
| `nxp-rt1170-lpuart-001` | uart | static_heuristic | clock_root_configured, init_status_checked |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_tx_configured, sai_write_api_used |
| `nxp-rt1170-sai-002` | audio | static_heuristic | bit_clock_rate_set, fifo_interrupt_enabled, tx_enabled, fifo_underrun_handled |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `header_fsl_clock_h` | 5 | nxp-mcxc-gpio-001, nxp-mcxc-gpio-002, nxp-mcxc-spi-001, nxp-mcxc-timer-001, nxp-mcxc-uart-001 |
| `header_fsl_port_h` | 3 | nxp-mcxc-i2c-002, nxp-mcxc-spi-001, nxp-mcxc-uart-001 |
| `clock_root_configured` | 3 | nxp-rt1170-lpi2c-001, nxp-rt1170-lpspi-001, nxp-rt1170-lpuart-001 |
| `flash_verify_program_called` | 1 | nxp-mcxc-flash-001 |
| `verify_after_each_write` | 1 | nxp-mcxc-flash-002 |
| `interrupt_flag_cleared` | 1 | nxp-mcxc-gpio-002 |
| `nvic_pit_enabled` | 1 | nxp-mcxc-isr-001 |
| `uart_isr_handler_defined` | 1 | nxp-mcxc-uart-002 |
| `long_timeout_configured` | 1 | nxp-mcxc-watchdog-001 |
| `read_and_write_api_used` | 1 | nxp-rt1170-audio-001 |
| `edma_transfer_prepared` | 1 | nxp-rt1170-dma-001 |
| `transfer_return_value_checked` | 1 | nxp-rt1170-lpi2c-001 |
| `transfer_status_checked` | 1 | nxp-rt1170-lpspi-001 |
| `init_status_checked` | 1 | nxp-rt1170-lpuart-001 |
| `sai_init_called` | 1 | nxp-rt1170-sai-001 |
| `sai_tx_configured` | 1 | nxp-rt1170-sai-001 |
| `sai_write_api_used` | 1 | nxp-rt1170-sai-001 |
| `bit_clock_rate_set` | 1 | nxp-rt1170-sai-002 |
| `fifo_interrupt_enabled` | 1 | nxp-rt1170-sai-002 |
| `tx_enabled` | 1 | nxp-rt1170-sai-002 |
| `fifo_underrun_handled` | 1 | nxp-rt1170-sai-002 |

## TC Improvement Suggestions

