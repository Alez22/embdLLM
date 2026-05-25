# Benchmark Report: groq/openai/gpt-oss-20b

**Date:** 2026-05-25 23:09 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/openai/gpt-oss-20b |
| Total Cases | 12 |
| Passed | 1 |
| Failed | 11 |
| pass@1 | 8.3% |

## Failed Cases (11)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_init_called, flash_erase_sector_called, flash_program_called, flash_verify_program_called |
| `nxp-mcxc-flash-002` | storage | static_analysis | crc_function_implemented, full_flash_sequence_present |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | header_fsl_clock_h, interrupt_flag_cleared |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | header_fsl_port_h, header_fsl_clock_h, i2c_master_init_called, i2c_blocking_transfer_used |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | header_fsl_port_h, i2c_master_init_called, both_write_and_read_transfers, two_separate_transfers |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined, volatile_shared_data, gpio_pin_read_in_code |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_spi_h, header_fsl_gpio_h, header_fsl_port_h, header_fsl_clock_h, spi_master_init_called, spi_blocking_transfer_used |
| `nxp-mcxc-timer-001` | timer | static_analysis | header_fsl_pit_h, header_fsl_clock_h, pit_init_called, pit_period_set, pit_timer_started, pit_isr_defined |
| `nxp-mcxc-uart-001` | uart | static_heuristic | uart_tx_enabled_in_config |
| `nxp-mcxc-uart-002` | uart | static_analysis | header_fsl_uart_h, header_fsl_port_h, header_fsl_clock_h, uart_rx_interrupt_enabled, uart_isr_handler_defined, ring_buffer_array_declared |
| `nxp-mcxc-watchdog-001` | watchdog | static_analysis | cop_refresh_called |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `header_fsl_clock_h` | 5 | nxp-mcxc-gpio-002, nxp-mcxc-i2c-001, nxp-mcxc-spi-001, nxp-mcxc-timer-001, nxp-mcxc-uart-002 |
| `header_fsl_port_h` | 4 | nxp-mcxc-i2c-001, nxp-mcxc-i2c-002, nxp-mcxc-spi-001, nxp-mcxc-uart-002 |
| `i2c_master_init_called` | 2 | nxp-mcxc-i2c-001, nxp-mcxc-i2c-002 |
| `pit_isr_defined` | 2 | nxp-mcxc-isr-001, nxp-mcxc-timer-001 |
| `flash_init_called` | 1 | nxp-mcxc-flash-001 |
| `flash_erase_sector_called` | 1 | nxp-mcxc-flash-001 |
| `flash_program_called` | 1 | nxp-mcxc-flash-001 |
| `flash_verify_program_called` | 1 | nxp-mcxc-flash-001 |
| `crc_function_implemented` | 1 | nxp-mcxc-flash-002 |
| `full_flash_sequence_present` | 1 | nxp-mcxc-flash-002 |
| `interrupt_flag_cleared` | 1 | nxp-mcxc-gpio-002 |
| `i2c_blocking_transfer_used` | 1 | nxp-mcxc-i2c-001 |
| `both_write_and_read_transfers` | 1 | nxp-mcxc-i2c-002 |
| `two_separate_transfers` | 1 | nxp-mcxc-i2c-002 |
| `volatile_shared_data` | 1 | nxp-mcxc-isr-001 |
| `gpio_pin_read_in_code` | 1 | nxp-mcxc-isr-001 |
| `header_fsl_spi_h` | 1 | nxp-mcxc-spi-001 |
| `header_fsl_gpio_h` | 1 | nxp-mcxc-spi-001 |
| `spi_master_init_called` | 1 | nxp-mcxc-spi-001 |
| `spi_blocking_transfer_used` | 1 | nxp-mcxc-spi-001 |
| `header_fsl_pit_h` | 1 | nxp-mcxc-timer-001 |
| `pit_init_called` | 1 | nxp-mcxc-timer-001 |
| `pit_period_set` | 1 | nxp-mcxc-timer-001 |
| `pit_timer_started` | 1 | nxp-mcxc-timer-001 |
| `uart_tx_enabled_in_config` | 1 | nxp-mcxc-uart-001 |
| `header_fsl_uart_h` | 1 | nxp-mcxc-uart-002 |
| `uart_rx_interrupt_enabled` | 1 | nxp-mcxc-uart-002 |
| `uart_isr_handler_defined` | 1 | nxp-mcxc-uart-002 |
| `ring_buffer_array_declared` | 1 | nxp-mcxc-uart-002 |
| `cop_refresh_called` | 1 | nxp-mcxc-watchdog-001 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 8 | nxp-mcxc-flash-001, nxp-mcxc-flash-002, nxp-mcxc-gpio-002, nxp-mcxc-i2c-001, nxp-mcxc-i2c-002 (+3 more) |
| LLM format failure (prose) | 3 | nxp-mcxc-spi-001, nxp-mcxc-timer-001, nxp-mcxc-uart-002 |

*Adjusted pass@1 (excluding format failures): 11.1% (1/9)*


## TC Improvement Suggestions

