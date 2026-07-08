# Benchmark Report: openrouter/qwen/qwen3-235b-a22b-2507

**Date:** 2026-06-13 15:45 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/qwen/qwen3-235b-a22b-2507 |
| Total Cases | 120 |
| Passed | 14 |
| Failed | 106 |
| pass@1 | 11.7% |

## Failed Cases (106)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_erase_sector_called, flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_erase_sector_called, flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_erase_sector_called, flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_erase_sector_called, flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_erase_sector_called, flash_verify_program_called |
| `nxp-mcxc-flash-002` | storage | static_analysis | full_flash_sequence_present |
| `nxp-mcxc-flash-002` | storage | static_analysis | full_flash_sequence_present |
| `nxp-mcxc-flash-002` | storage | static_analysis | full_flash_sequence_present |
| `nxp-mcxc-flash-002` | storage | static_analysis | full_flash_sequence_present |
| `nxp-mcxc-flash-002` | storage | static_analysis | full_flash_sequence_present |
| `nxp-mcxc-gpio-001` | gpio-basic | static_heuristic | clock_gate_before_gpio_init, pinmux_as_gpio_before_init, gpio_mux_enum_used |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_port_h |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_port_h, header_fsl_clock_h |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | header_fsl_clock_h, interrupt_flag_cleared |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | header_fsl_clock_h, isr_handler_defined |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | header_fsl_clock_h, isr_handler_defined |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | header_fsl_clock_h, pin_interrupt_configured |
| `nxp-mcxc-i2c-001` | spi-i2c | static_heuristic | pinmux_before_i2c_init, default_transfer_flag_set |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-i2c-001` | spi-i2c | static_heuristic | default_transfer_flag_set |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | two_separate_transfers |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | gpio_pin_read_in_code |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | gpio_pin_read_in_code |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined, gpio_pin_read_in_code |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined, gpio_pin_read_in_code |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h, header_fsl_clock_h, spi_blocking_transfer_used |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-timer-001` | timer | static_heuristic | clock_gate_before_pit_init |
| `nxp-mcxc-timer-001` | timer | static_heuristic | pit_flag_cleared_in_isr |
| `nxp-mcxc-timer-001` | timer | static_analysis | pit_isr_defined |
| `nxp-mcxc-timer-001` | timer | static_analysis | pit_isr_defined |
| `nxp-mcxc-uart-001` | uart | static_analysis | header_fsl_port_h |
| `nxp-mcxc-uart-001` | uart | static_heuristic | clock_gate_before_uart_init, pinmux_before_uart_init |
| `nxp-mcxc-uart-001` | uart | static_analysis | header_fsl_port_h |
| `nxp-mcxc-uart-001` | uart | static_heuristic | clock_gate_before_uart_init, pinmux_before_uart_init |
| `nxp-mcxc-uart-002` | uart | static_heuristic | clock_gate_before_uart_init, ring_buffer_volatile, ring_buffer_indices_volatile |
| `nxp-mcxc-uart-002` | uart | static_heuristic | clock_gate_before_uart_init, ring_buffer_volatile, ring_buffer_indices_volatile, rx_flag_checked_in_isr |
| `nxp-mcxc-uart-002` | uart | static_heuristic | ring_buffer_volatile |
| `nxp-mcxc-uart-002` | uart | static_heuristic | ring_buffer_volatile |
| `nxp-mcxc-uart-002` | uart | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-watchdog-001` | watchdog | static_heuristic | long_timeout_configured |
| `nxp-mcxc-watchdog-001` | watchdog | static_analysis | cop_refresh_called |
| `nxp-mcxc-watchdog-001` | watchdog | static_heuristic | long_timeout_configured |
| `nxp-mcxc-watchdog-001` | watchdog | static_heuristic | long_timeout_configured |
| `nxp-mcxc-watchdog-001` | watchdog | static_heuristic | long_timeout_configured |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | header_fsl_iomuxc_h, read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-dma-001` | dma | static_heuristic | dcache_coherency_handled, dcache_clean_before_start, dcache_invalidate_after_transfer, dma_buffers_cache_aligned |
| `nxp-rt1170-dma-001` | dma | static_heuristic | dcache_coherency_handled, dcache_clean_before_start, dcache_invalidate_after_transfer |
| `nxp-rt1170-dma-001` | dma | static_heuristic | dcache_coherency_handled, dcache_clean_before_start, dcache_invalidate_after_transfer, dma_buffers_cache_aligned |
| `nxp-rt1170-dma-001` | dma | static_heuristic | dcache_coherency_handled, dcache_clean_before_start, dcache_invalidate_after_transfer, dma_buffers_cache_aligned |
| `nxp-rt1170-dma-001` | dma | static_heuristic | dcache_coherency_handled, dcache_clean_before_start, dcache_invalidate_after_transfer, dma_buffers_cache_aligned |
| `nxp-rt1170-gpio-001` | gpio-basic | static_analysis | header_fsl_iomuxc_h |
| `nxp-rt1170-gpio-001` | gpio-basic | static_analysis | header_fsl_iomuxc_h |
| `nxp-rt1170-gpio-001` | gpio-basic | static_analysis | header_fsl_iomuxc_h |
| `nxp-rt1170-gpio-001` | gpio-basic | static_analysis | header_fsl_iomuxc_h |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | header_fsl_iomuxc_h, isr_handler_defined |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | header_fsl_iomuxc_h, isr_handler_defined |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | header_fsl_iomuxc_h, isr_handler_defined |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | header_fsl_iomuxc_h, isr_handler_defined |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | header_fsl_iomuxc_h, isr_handler_defined |
| `nxp-rt1170-gpt-001` | timer | static_heuristic | clock_root_configured |
| `nxp-rt1170-gpt-001` | timer | static_heuristic | clock_root_configured |
| `nxp-rt1170-gpt-001` | timer | static_heuristic | clock_root_configured |
| `nxp-rt1170-gpt-001` | timer | static_heuristic | clock_root_configured |
| `nxp-rt1170-gpt-001` | timer | static_heuristic | clock_root_configured |
| `nxp-rt1170-isr-001` | isr-concurrency | static_heuristic | critical_section_around_read |
| `nxp-rt1170-isr-001` | isr-concurrency | static_heuristic | critical_section_around_read |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_heuristic | clock_root_configured |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_analysis | lpi2c_blocking_transfer_used |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_analysis | lpi2c_blocking_transfer_used |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_heuristic | clock_root_configured, default_transfer_flag_set |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_heuristic | clock_root_configured, default_transfer_flag_set |
| `nxp-rt1170-lpspi-001` | spi-i2c | static_heuristic | clock_root_configured |
| `nxp-rt1170-lpspi-001` | spi-i2c | static_heuristic | clock_root_configured, pcs_continuous_set |
| `nxp-rt1170-lpspi-001` | spi-i2c | static_heuristic | clock_root_configured, transfer_status_checked |
| `nxp-rt1170-lpspi-001` | spi-i2c | static_heuristic | clock_root_configured |
| `nxp-rt1170-lpuart-001` | uart | static_heuristic | clock_root_configured, init_status_checked |
| `nxp-rt1170-lpuart-001` | uart | static_heuristic | clock_root_configured, init_status_checked |
| `nxp-rt1170-lpuart-001` | uart | static_heuristic | clock_root_configured, init_status_checked |
| `nxp-rt1170-lpuart-001` | uart | static_heuristic | clock_root_configured, init_status_checked |
| `nxp-rt1170-lpuart-001` | uart | static_heuristic | clock_root_configured, init_status_checked |
| `nxp-rt1170-rtwdog-001` | watchdog | static_heuristic | no_legacy_kinetis_wdog_api |
| `nxp-rt1170-rtwdog-001` | watchdog | static_heuristic | no_legacy_kinetis_wdog_api |
| `nxp-rt1170-rtwdog-001` | watchdog | static_heuristic | timeout_configured, no_legacy_kinetis_wdog_api |
| `nxp-rt1170-rtwdog-001` | watchdog | static_heuristic | no_legacy_kinetis_wdog_api |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_tx_configured, sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | lpi2c_blocking_transfer_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_tx_configured, sai_write_api_used, lpi2c_blocking_transfer_used |
| `nxp-rt1170-sai-002` | audio | static_analysis | header_fsl_iomuxc_h |
| `nxp-rt1170-sai-002` | audio | static_heuristic | clock_root_configured, bit_clock_rate_set |
| `nxp-rt1170-sai-002` | audio | static_heuristic | clock_root_configured, bit_clock_rate_set, fifo_underrun_handled |
| `nxp-rt1170-sai-002` | audio | static_analysis | header_fsl_iomuxc_h |
| `nxp-rt1170-sai-002` | audio | static_analysis | header_fsl_iomuxc_h |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `clock_root_configured` | 19 | nxp-rt1170-gpt-001, nxp-rt1170-gpt-001, nxp-rt1170-gpt-001, nxp-rt1170-gpt-001, nxp-rt1170-gpt-001 (+14 more) |
| `header_fsl_iomuxc_h` | 13 | nxp-rt1170-audio-001, nxp-rt1170-gpio-001, nxp-rt1170-gpio-001, nxp-rt1170-gpio-001, nxp-rt1170-gpio-001 (+8 more) |
| `header_fsl_port_h` | 10 | nxp-mcxc-gpio-001, nxp-mcxc-gpio-001, nxp-mcxc-i2c-001, nxp-mcxc-spi-001, nxp-mcxc-spi-001 (+5 more) |
| `header_fsl_clock_h` | 10 | nxp-mcxc-gpio-001, nxp-mcxc-gpio-001, nxp-mcxc-gpio-001, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002 (+5 more) |
| `isr_handler_defined` | 7 | nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-rt1170-gpio-002, nxp-rt1170-gpio-002, nxp-rt1170-gpio-002 (+2 more) |
| `flash_erase_sector_called` | 5 | nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001 |
| `flash_verify_program_called` | 5 | nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001 |
| `full_flash_sequence_present` | 5 | nxp-mcxc-flash-002, nxp-mcxc-flash-002, nxp-mcxc-flash-002, nxp-mcxc-flash-002, nxp-mcxc-flash-002 |
| `pit_isr_defined` | 5 | nxp-mcxc-isr-001, nxp-mcxc-isr-001, nxp-mcxc-isr-001, nxp-mcxc-timer-001, nxp-mcxc-timer-001 |
| `read_and_write_api_used` | 5 | nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-audio-001 |
| `dcache_coherency_handled` | 5 | nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001 |
| `dcache_clean_before_start` | 5 | nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001 |
| `dcache_invalidate_after_transfer` | 5 | nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001 |
| `init_status_checked` | 5 | nxp-rt1170-lpuart-001, nxp-rt1170-lpuart-001, nxp-rt1170-lpuart-001, nxp-rt1170-lpuart-001, nxp-rt1170-lpuart-001 |
| `default_transfer_flag_set` | 4 | nxp-mcxc-i2c-001, nxp-mcxc-i2c-001, nxp-rt1170-lpi2c-001, nxp-rt1170-lpi2c-001 |
| `gpio_pin_read_in_code` | 4 | nxp-mcxc-isr-001, nxp-mcxc-isr-001, nxp-mcxc-isr-001, nxp-mcxc-isr-001 |
| `clock_gate_before_uart_init` | 4 | nxp-mcxc-uart-001, nxp-mcxc-uart-001, nxp-mcxc-uart-002, nxp-mcxc-uart-002 |
| `ring_buffer_volatile` | 4 | nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002 |
| `long_timeout_configured` | 4 | nxp-mcxc-watchdog-001, nxp-mcxc-watchdog-001, nxp-mcxc-watchdog-001, nxp-mcxc-watchdog-001 |
| `dma_buffers_cache_aligned` | 4 | nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001 |
| `lpi2c_blocking_transfer_used` | 4 | nxp-rt1170-lpi2c-001, nxp-rt1170-lpi2c-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `no_legacy_kinetis_wdog_api` | 4 | nxp-rt1170-rtwdog-001, nxp-rt1170-rtwdog-001, nxp-rt1170-rtwdog-001, nxp-rt1170-rtwdog-001 |
| `sai_write_api_used` | 4 | nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `pinmux_before_uart_init` | 2 | nxp-mcxc-uart-001, nxp-mcxc-uart-001 |
| `ring_buffer_indices_volatile` | 2 | nxp-mcxc-uart-002, nxp-mcxc-uart-002 |
| `critical_section_around_read` | 2 | nxp-rt1170-isr-001, nxp-rt1170-isr-001 |
| `sai_init_called` | 2 | nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `sai_tx_configured` | 2 | nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `bit_clock_rate_set` | 2 | nxp-rt1170-sai-002, nxp-rt1170-sai-002 |
| `clock_gate_before_gpio_init` | 1 | nxp-mcxc-gpio-001 |
| `pinmux_as_gpio_before_init` | 1 | nxp-mcxc-gpio-001 |
| `gpio_mux_enum_used` | 1 | nxp-mcxc-gpio-001 |
| `interrupt_flag_cleared` | 1 | nxp-mcxc-gpio-002 |
| `pin_interrupt_configured` | 1 | nxp-mcxc-gpio-002 |
| `pinmux_before_i2c_init` | 1 | nxp-mcxc-i2c-001 |
| `two_separate_transfers` | 1 | nxp-mcxc-i2c-002 |
| `spi_blocking_transfer_used` | 1 | nxp-mcxc-spi-001 |
| `clock_gate_before_pit_init` | 1 | nxp-mcxc-timer-001 |
| `pit_flag_cleared_in_isr` | 1 | nxp-mcxc-timer-001 |
| `rx_flag_checked_in_isr` | 1 | nxp-mcxc-uart-002 |
| `cop_refresh_called` | 1 | nxp-mcxc-watchdog-001 |
| `pcs_continuous_set` | 1 | nxp-rt1170-lpspi-001 |
| `transfer_status_checked` | 1 | nxp-rt1170-lpspi-001 |
| `timeout_configured` | 1 | nxp-rt1170-rtwdog-001 |
| `fifo_underrun_handled` | 1 | nxp-rt1170-sai-002 |

## TC Improvement Suggestions

