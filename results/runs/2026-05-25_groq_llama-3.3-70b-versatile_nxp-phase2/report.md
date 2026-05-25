# Benchmark Report: groq/llama-3.3-70b-versatile

**Date:** 2026-05-25 23:04 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/llama-3.3-70b-versatile |
| Total Cases | 12 |
| Passed | 0 |
| Failed | 12 |
| pass@1 | 0.0% |

## Failed Cases (12)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-002` | storage | static_analysis | full_flash_sequence_present |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_port_h, header_fsl_clock_h, gpio_toggle_called |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | header_fsl_clock_h, pin_interrupt_configured, interrupt_flag_cleared, isr_handler_defined |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | header_fsl_port_h, header_fsl_clock_h, i2c_master_init_called |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | header_fsl_port_h, header_fsl_clock_h, both_write_and_read_transfers, two_separate_transfers |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | header_fsl_clock_h, pit_isr_defined, gpio_pin_read_in_code |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h, header_fsl_clock_h |
| `nxp-mcxc-timer-001` | timer | static_analysis | header_fsl_clock_h, pit_timer_started, pit_isr_defined |
| `nxp-mcxc-uart-001` | uart | static_analysis | header_fsl_port_h, header_fsl_clock_h |
| `nxp-mcxc-uart-002` | uart | static_analysis | header_fsl_port_h, header_fsl_clock_h, uart_isr_handler_defined |
| `nxp-mcxc-watchdog-001` | watchdog | static_analysis | cop_refresh_called |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `header_fsl_clock_h` | 9 | nxp-mcxc-gpio-001, nxp-mcxc-gpio-002, nxp-mcxc-i2c-001, nxp-mcxc-i2c-002, nxp-mcxc-isr-001 (+4 more) |
| `header_fsl_port_h` | 6 | nxp-mcxc-gpio-001, nxp-mcxc-i2c-001, nxp-mcxc-i2c-002, nxp-mcxc-spi-001, nxp-mcxc-uart-001 (+1 more) |
| `pit_isr_defined` | 2 | nxp-mcxc-isr-001, nxp-mcxc-timer-001 |
| `flash_verify_program_called` | 1 | nxp-mcxc-flash-001 |
| `full_flash_sequence_present` | 1 | nxp-mcxc-flash-002 |
| `gpio_toggle_called` | 1 | nxp-mcxc-gpio-001 |
| `pin_interrupt_configured` | 1 | nxp-mcxc-gpio-002 |
| `interrupt_flag_cleared` | 1 | nxp-mcxc-gpio-002 |
| `isr_handler_defined` | 1 | nxp-mcxc-gpio-002 |
| `i2c_master_init_called` | 1 | nxp-mcxc-i2c-001 |
| `both_write_and_read_transfers` | 1 | nxp-mcxc-i2c-002 |
| `two_separate_transfers` | 1 | nxp-mcxc-i2c-002 |
| `gpio_pin_read_in_code` | 1 | nxp-mcxc-isr-001 |
| `pit_timer_started` | 1 | nxp-mcxc-timer-001 |
| `uart_isr_handler_defined` | 1 | nxp-mcxc-uart-002 |
| `cop_refresh_called` | 1 | nxp-mcxc-watchdog-001 |

## TC Improvement Suggestions

