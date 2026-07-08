# Benchmark Report: openrouter/deepseek/deepseek-v4-flash

**Date:** 2026-06-14 14:40 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/deepseek/deepseek-v4-flash |
| Total Cases | 120 |
| Passed | 36 |
| Failed | 84 |
| pass@1 | 30.0% |

## Failed Cases (84)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_erase_sector_called, flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_heuristic | flash_return_value_checked, flash_erase_key_used |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-002` | storage | static_analysis | crc_function_implemented |
| `nxp-mcxc-flash-002` | storage | static_analysis | full_flash_sequence_present |
| `nxp-mcxc-flash-002` | storage | static_heuristic | verify_after_each_write |
| `nxp-mcxc-flash-002` | storage | static_analysis | full_flash_sequence_present |
| `nxp-mcxc-flash-002` | storage | static_analysis | full_flash_sequence_present |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | header_fsl_clock_h, interrupt_flag_cleared |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | header_fsl_clock_h, interrupt_flag_cleared |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | i2c_blocking_transfer_used |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | both_write_and_read_transfers, two_separate_transfers |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | both_write_and_read_transfers, two_separate_transfers |
| `nxp-mcxc-isr-001` | isr-concurrency | static_heuristic | clock_gate_before_gpio_init, nvic_pit_enabled |
| `nxp-mcxc-isr-001` | isr-concurrency | static_heuristic | nvic_pit_enabled |
| `nxp-mcxc-isr-001` | isr-concurrency | static_heuristic | pit_flag_cleared_in_isr |
| `nxp-mcxc-isr-001` | isr-concurrency | static_heuristic | nvic_pit_enabled |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h, header_fsl_clock_h |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h, header_fsl_clock_h |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-spi-001` | spi-i2c | static_heuristic | cs_asserted_before_transfer, cs_idle_high_initial_state |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h, header_fsl_clock_h, spi_blocking_transfer_used |
| `nxp-mcxc-timer-001` | timer | static_heuristic | nvic_pit_interrupt_enabled |
| `nxp-mcxc-timer-001` | timer | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-timer-001` | timer | static_analysis | pit_isr_defined |
| `nxp-mcxc-uart-001` | uart | static_heuristic | clock_gate_before_uart_init, pinmux_before_uart_init |
| `nxp-mcxc-uart-001` | uart | static_analysis | uart_write_blocking_used |
| `nxp-mcxc-uart-001` | uart | static_analysis | header_fsl_port_h |
| `nxp-mcxc-uart-002` | uart | static_heuristic | ring_buffer_indices_volatile |
| `nxp-mcxc-uart-002` | uart | static_heuristic | ring_buffer_volatile |
| `nxp-mcxc-uart-002` | uart | static_heuristic | ring_buffer_volatile |
| `nxp-mcxc-watchdog-001` | watchdog | static_heuristic | lpo_clock_source_used, long_timeout_configured |
| `nxp-mcxc-watchdog-001` | watchdog | static_heuristic | long_timeout_configured |
| `nxp-mcxc-watchdog-001` | watchdog | static_heuristic | long_timeout_configured |
| `nxp-mcxc-watchdog-001` | watchdog | static_heuristic | lpo_clock_source_used, long_timeout_configured |
| `nxp-mcxc-watchdog-001` | watchdog | static_heuristic | lpo_clock_source_used, long_timeout_configured |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_heuristic | clock_root_configured, bit_clock_rate_set |
| `nxp-rt1170-audio-001` | audio | static_analysis | header_fsl_iomuxc_h, read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_heuristic | clock_root_configured, bit_clock_rate_set, tx_and_rx_enabled |
| `nxp-rt1170-dma-001` | dma | static_heuristic | dcache_coherency_handled, dcache_clean_before_start, dcache_invalidate_after_transfer |
| `nxp-rt1170-dma-001` | dma | static_analysis | edma_transfer_prepared |
| `nxp-rt1170-dma-001` | dma | static_analysis | edma_transfer_started |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | falling_edge_configured |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | falling_edge_configured |
| `nxp-rt1170-gpio-002` | gpio-basic | static_heuristic | iomuxc_before_gpio_init, gpio_port_interrupts_enabled |
| `nxp-rt1170-gpt-001` | timer | static_heuristic | clock_root_configured |
| `nxp-rt1170-gpt-001` | timer | static_heuristic | peripheral_interrupt_enabled |
| `nxp-rt1170-gpt-001` | timer | static_heuristic | clock_root_configured |
| `nxp-rt1170-gpt-001` | timer | static_heuristic | clock_root_configured |
| `nxp-rt1170-isr-001` | isr-concurrency | static_heuristic | critical_section_around_read |
| `nxp-rt1170-isr-001` | isr-concurrency | static_heuristic | critical_section_around_read |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_analysis | header_fsl_clock_h |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_analysis | header_fsl_clock_h |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_heuristic | clock_root_configured |
| `nxp-rt1170-lpspi-001` | spi-i2c | static_analysis | header_fsl_iomuxc_h |
| `nxp-rt1170-lpspi-001` | spi-i2c | static_heuristic | transfer_status_checked |
| `nxp-rt1170-lpspi-001` | spi-i2c | static_heuristic | transfer_status_checked |
| `nxp-rt1170-lpspi-001` | spi-i2c | static_heuristic | transfer_status_checked |
| `nxp-rt1170-lpspi-001` | spi-i2c | static_heuristic | transfer_status_checked |
| `nxp-rt1170-lpuart-001` | uart | static_heuristic | init_status_checked |
| `nxp-rt1170-lpuart-001` | uart | static_heuristic | init_status_checked |
| `nxp-rt1170-lpuart-001` | uart | static_heuristic | clock_root_configured, init_status_checked |
| `nxp-rt1170-lpuart-001` | uart | static_heuristic | init_status_checked |
| `nxp-rt1170-rtwdog-001` | watchdog | static_heuristic | refresh_inside_main_loop |
| `nxp-rt1170-rtwdog-001` | watchdog | static_heuristic | refresh_inside_main_loop |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_tx_configured |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_write_api_used |
| `nxp-rt1170-sai-002` | audio | static_heuristic | fifo_underrun_handled |
| `nxp-rt1170-sai-002` | audio | static_analysis | isr_handler_defined |
| `nxp-rt1170-sai-002` | audio | static_heuristic | bit_clock_rate_set, fifo_interrupt_enabled, fifo_underrun_handled |
| `nxp-rt1170-sai-002` | audio | static_heuristic | bit_clock_rate_set, fifo_interrupt_enabled, fifo_underrun_handled |
| `nxp-rt1170-sai-002` | audio | static_heuristic | bit_clock_rate_set, fifo_interrupt_enabled, fifo_underrun_handled |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `header_fsl_clock_h` | 11 | nxp-mcxc-gpio-001, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-mcxc-i2c-001 (+6 more) |
| `clock_root_configured` | 7 | nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-gpt-001, nxp-rt1170-gpt-001, nxp-rt1170-gpt-001 (+2 more) |
| `header_fsl_port_h` | 5 | nxp-mcxc-spi-001, nxp-mcxc-spi-001, nxp-mcxc-spi-001, nxp-mcxc-spi-001, nxp-mcxc-uart-001 |
| `long_timeout_configured` | 5 | nxp-mcxc-watchdog-001, nxp-mcxc-watchdog-001, nxp-mcxc-watchdog-001, nxp-mcxc-watchdog-001, nxp-mcxc-watchdog-001 |
| `bit_clock_rate_set` | 5 | nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-sai-002, nxp-rt1170-sai-002, nxp-rt1170-sai-002 |
| `flash_verify_program_called` | 4 | nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001 |
| `interrupt_flag_cleared` | 4 | nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002 |
| `transfer_status_checked` | 4 | nxp-rt1170-lpspi-001, nxp-rt1170-lpspi-001, nxp-rt1170-lpspi-001, nxp-rt1170-lpspi-001 |
| `init_status_checked` | 4 | nxp-rt1170-lpuart-001, nxp-rt1170-lpuart-001, nxp-rt1170-lpuart-001, nxp-rt1170-lpuart-001 |
| `sai_write_api_used` | 4 | nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `fifo_underrun_handled` | 4 | nxp-rt1170-sai-002, nxp-rt1170-sai-002, nxp-rt1170-sai-002, nxp-rt1170-sai-002 |
| `full_flash_sequence_present` | 3 | nxp-mcxc-flash-002, nxp-mcxc-flash-002, nxp-mcxc-flash-002 |
| `nvic_pit_enabled` | 3 | nxp-mcxc-isr-001, nxp-mcxc-isr-001, nxp-mcxc-isr-001 |
| `lpo_clock_source_used` | 3 | nxp-mcxc-watchdog-001, nxp-mcxc-watchdog-001, nxp-mcxc-watchdog-001 |
| `read_and_write_api_used` | 3 | nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-audio-001 |
| `sai_init_called` | 3 | nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `fifo_interrupt_enabled` | 3 | nxp-rt1170-sai-002, nxp-rt1170-sai-002, nxp-rt1170-sai-002 |
| `both_write_and_read_transfers` | 2 | nxp-mcxc-i2c-002, nxp-mcxc-i2c-002 |
| `two_separate_transfers` | 2 | nxp-mcxc-i2c-002, nxp-mcxc-i2c-002 |
| `ring_buffer_volatile` | 2 | nxp-mcxc-uart-002, nxp-mcxc-uart-002 |
| `header_fsl_iomuxc_h` | 2 | nxp-rt1170-audio-001, nxp-rt1170-lpspi-001 |
| `falling_edge_configured` | 2 | nxp-rt1170-gpio-002, nxp-rt1170-gpio-002 |
| `critical_section_around_read` | 2 | nxp-rt1170-isr-001, nxp-rt1170-isr-001 |
| `refresh_inside_main_loop` | 2 | nxp-rt1170-rtwdog-001, nxp-rt1170-rtwdog-001 |
| `flash_erase_sector_called` | 1 | nxp-mcxc-flash-001 |
| `flash_return_value_checked` | 1 | nxp-mcxc-flash-001 |
| `flash_erase_key_used` | 1 | nxp-mcxc-flash-001 |
| `crc_function_implemented` | 1 | nxp-mcxc-flash-002 |
| `verify_after_each_write` | 1 | nxp-mcxc-flash-002 |
| `i2c_blocking_transfer_used` | 1 | nxp-mcxc-i2c-001 |
| `clock_gate_before_gpio_init` | 1 | nxp-mcxc-isr-001 |
| `pit_flag_cleared_in_isr` | 1 | nxp-mcxc-isr-001 |
| `cs_asserted_before_transfer` | 1 | nxp-mcxc-spi-001 |
| `cs_idle_high_initial_state` | 1 | nxp-mcxc-spi-001 |
| `spi_blocking_transfer_used` | 1 | nxp-mcxc-spi-001 |
| `nvic_pit_interrupt_enabled` | 1 | nxp-mcxc-timer-001 |
| `pit_isr_defined` | 1 | nxp-mcxc-timer-001 |
| `clock_gate_before_uart_init` | 1 | nxp-mcxc-uart-001 |
| `pinmux_before_uart_init` | 1 | nxp-mcxc-uart-001 |
| `uart_write_blocking_used` | 1 | nxp-mcxc-uart-001 |
| `ring_buffer_indices_volatile` | 1 | nxp-mcxc-uart-002 |
| `tx_and_rx_enabled` | 1 | nxp-rt1170-audio-001 |
| `dcache_coherency_handled` | 1 | nxp-rt1170-dma-001 |
| `dcache_clean_before_start` | 1 | nxp-rt1170-dma-001 |
| `dcache_invalidate_after_transfer` | 1 | nxp-rt1170-dma-001 |
| `edma_transfer_prepared` | 1 | nxp-rt1170-dma-001 |
| `edma_transfer_started` | 1 | nxp-rt1170-dma-001 |
| `iomuxc_before_gpio_init` | 1 | nxp-rt1170-gpio-002 |
| `gpio_port_interrupts_enabled` | 1 | nxp-rt1170-gpio-002 |
| `peripheral_interrupt_enabled` | 1 | nxp-rt1170-gpt-001 |
| `sai_tx_configured` | 1 | nxp-rt1170-sai-001 |
| `isr_handler_defined` | 1 | nxp-rt1170-sai-002 |

## TC Improvement Suggestions

