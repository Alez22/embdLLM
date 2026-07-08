# Benchmark Report: openrouter/deepseek/deepseek-v4-flash

**Date:** 2026-06-15 22:59 UTC

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
| `nxp-mcxc-gpio-002` | gpio-basic | static_heuristic | nvic_interrupt_enabled, isr_shared_variable_volatile |
| `nxp-mcxc-i2c-001` | spi-i2c | static_heuristic | clock_gate_before_i2c_init, pinmux_before_i2c_init |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | header_fsl_clock_h, pit_isr_defined |
| `nxp-mcxc-timer-001` | timer | static_heuristic | pit_interrupts_enabled |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-watchdog-001` | watchdog | static_heuristic | lpo_clock_source_used, long_timeout_configured, cop_refresh_inside_main_loop |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-dma-001` | dma | static_heuristic | dcache_coherency_handled, dcache_clean_before_start, dcache_invalidate_after_transfer |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | isr_handler_defined |
| `nxp-rt1170-gpt-001` | timer | static_heuristic | clock_root_configured |
| `nxp-rt1170-isr-001` | isr-concurrency | static_heuristic | critical_section_around_read |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_analysis | lpi2c_blocking_transfer_used |
| `nxp-rt1170-lpspi-001` | spi-i2c | static_heuristic | clock_root_configured, transfer_status_checked |
| `nxp-rt1170-lpuart-001` | uart | static_heuristic | clock_root_configured, init_status_checked |
| `nxp-rt1170-sai-001` | audio | static_heuristic | bit_clock_rate_set |
| `nxp-rt1170-sai-002` | audio | static_heuristic | bit_clock_rate_set, fifo_interrupt_enabled, fifo_underrun_handled |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `clock_root_configured` | 3 | nxp-rt1170-gpt-001, nxp-rt1170-lpspi-001, nxp-rt1170-lpuart-001 |
| `bit_clock_rate_set` | 2 | nxp-rt1170-sai-001, nxp-rt1170-sai-002 |
| `flash_verify_program_called` | 1 | nxp-mcxc-flash-001 |
| `verify_after_each_write` | 1 | nxp-mcxc-flash-002 |
| `nvic_interrupt_enabled` | 1 | nxp-mcxc-gpio-002 |
| `isr_shared_variable_volatile` | 1 | nxp-mcxc-gpio-002 |
| `clock_gate_before_i2c_init` | 1 | nxp-mcxc-i2c-001 |
| `pinmux_before_i2c_init` | 1 | nxp-mcxc-i2c-001 |
| `header_fsl_clock_h` | 1 | nxp-mcxc-isr-001 |
| `pit_isr_defined` | 1 | nxp-mcxc-isr-001 |
| `pit_interrupts_enabled` | 1 | nxp-mcxc-timer-001 |
| `uart_isr_handler_defined` | 1 | nxp-mcxc-uart-002 |
| `lpo_clock_source_used` | 1 | nxp-mcxc-watchdog-001 |
| `long_timeout_configured` | 1 | nxp-mcxc-watchdog-001 |
| `cop_refresh_inside_main_loop` | 1 | nxp-mcxc-watchdog-001 |
| `read_and_write_api_used` | 1 | nxp-rt1170-audio-001 |
| `dcache_coherency_handled` | 1 | nxp-rt1170-dma-001 |
| `dcache_clean_before_start` | 1 | nxp-rt1170-dma-001 |
| `dcache_invalidate_after_transfer` | 1 | nxp-rt1170-dma-001 |
| `isr_handler_defined` | 1 | nxp-rt1170-gpio-002 |
| `critical_section_around_read` | 1 | nxp-rt1170-isr-001 |
| `lpi2c_blocking_transfer_used` | 1 | nxp-rt1170-lpi2c-001 |
| `transfer_status_checked` | 1 | nxp-rt1170-lpspi-001 |
| `init_status_checked` | 1 | nxp-rt1170-lpuart-001 |
| `fifo_interrupt_enabled` | 1 | nxp-rt1170-sai-002 |
| `fifo_underrun_handled` | 1 | nxp-rt1170-sai-002 |

## TC Improvement Suggestions

