# Benchmark Report: openrouter/google/gemma-4-31b-it

**Date:** 2026-06-24 17:55 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/google/gemma-4-31b-it |
| Total Cases | 120 |
| Passed | 0 |
| Failed | 120 |
| pass@1 | 0.0% |

## Failed Cases (120)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_init_called, flash_erase_sector_called, flash_program_called, flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_init_called, flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_init_called, flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_init_called, flash_program_called, flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_init_called, flash_verify_program_called |
| `nxp-mcxc-flash-002` | storage | static_analysis | crc_function_implemented |
| `nxp-mcxc-flash-002` | storage | static_analysis | crc_function_implemented |
| `nxp-mcxc-flash-002` | storage | static_analysis | crc_function_implemented, full_flash_sequence_present |
| `nxp-mcxc-flash-002` | storage | static_analysis | crc_function_implemented, full_flash_sequence_present |
| `nxp-mcxc-flash-002` | storage | static_analysis | crc_function_implemented, full_flash_sequence_present |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_port_h |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_port_h |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_port_h, header_fsl_clock_h |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_port_h |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_port_h |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | pin_interrupt_configured, interrupt_flag_cleared, isr_handler_defined |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | pin_interrupt_configured, interrupt_flag_cleared |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | pin_interrupt_configured |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | pin_interrupt_configured, isr_handler_defined |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | both_write_and_read_transfers |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | both_write_and_read_transfers, two_separate_transfers |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | both_write_and_read_transfers |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | both_write_and_read_transfers, two_separate_transfers |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | header_fsl_port_h, both_write_and_read_transfers, two_separate_transfers |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | header_fsl_clock_h, pit_isr_defined |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-timer-001` | timer | static_analysis | pit_period_set, pit_isr_defined |
| `nxp-mcxc-timer-001` | timer | static_analysis | header_fsl_clock_h, pit_isr_defined |
| `nxp-mcxc-timer-001` | timer | static_analysis | pit_isr_defined |
| `nxp-mcxc-timer-001` | timer | static_analysis | pit_period_set, pit_isr_defined |
| `nxp-mcxc-timer-001` | timer | static_analysis | pit_period_set, pit_isr_defined |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-001` | uart | static_analysis | header_fsl_port_h |
| `nxp-mcxc-uart-001` | uart | static_analysis | header_fsl_port_h |
| `nxp-mcxc-uart-001` | uart | static_analysis | header_fsl_port_h |
| `nxp-mcxc-uart-001` | uart | static_analysis | uart_write_blocking_used |
| `nxp-mcxc-uart-002` | uart | static_analysis | header_fsl_port_h, uart_isr_handler_defined |
| `nxp-mcxc-uart-002` | uart | static_analysis | header_fsl_port_h, uart_isr_handler_defined |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-uart-002` | uart | static_analysis | header_fsl_port_h, uart_rx_interrupt_enabled, uart_isr_handler_defined |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-watchdog-001` | watchdog | static_analysis | cop_refresh_called |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | header_fsl_iomuxc_h, read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | header_fsl_iomuxc_h, read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | header_fsl_iomuxc_h, read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-dma-001` | dma | static_analysis | edma_init_called, edma_transfer_prepared, edma_transfer_started |
| `nxp-rt1170-dma-001` | dma | static_analysis | edma_transfer_prepared, edma_transfer_started |
| `nxp-rt1170-dma-001` | dma | static_analysis | edma_init_called, edma_transfer_prepared, edma_transfer_started |
| `nxp-rt1170-dma-001` | dma | static_analysis | edma_init_called, edma_transfer_prepared, edma_transfer_started |
| `nxp-rt1170-dma-001` | dma | static_analysis | edma_init_called, edma_transfer_prepared, edma_transfer_started |
| `nxp-rt1170-gpio-001` | gpio-basic | static_analysis | gpio_pin_init_called |
| `nxp-rt1170-gpio-001` | gpio-basic | static_analysis | header_fsl_iomuxc_h, gpio_pin_init_called, gpio_toggle_called |
| `nxp-rt1170-gpio-001` | gpio-basic | static_analysis | header_fsl_iomuxc_h |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared, falling_edge_configured |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared, falling_edge_configured |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared, falling_edge_configured |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared, falling_edge_configured |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | isr_handler_defined, interrupt_flag_cleared, falling_edge_configured |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-gpt-001` | timer | static_analysis | interrupt_flag_cleared |
| `nxp-rt1170-gpt-001` | timer | static_analysis | interrupt_flag_cleared |
| `nxp-rt1170-gpt-001` | timer | static_analysis | interrupt_flag_cleared |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | static_analysis | interrupt_flag_cleared |
| `nxp-rt1170-isr-001` | isr-concurrency | static_analysis | interrupt_flag_cleared |
| `nxp-rt1170-isr-001` | isr-concurrency | static_analysis | interrupt_flag_cleared |
| `nxp-rt1170-isr-001` | isr-concurrency | static_analysis | interrupt_flag_cleared |
| `nxp-rt1170-isr-001` | isr-concurrency | static_analysis | interrupt_flag_cleared |
| `nxp-rt1170-lpi2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpi2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpi2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpi2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpi2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpspi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpspi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpspi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpspi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpspi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | static_analysis | header_fsl_iomuxc_h |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | static_analysis | rtwdog_init_called |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_tx_configured, sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | header_fsl_iomuxc_h, sai_tx_configured, sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | header_fsl_iomuxc_h, sai_tx_configured, sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | header_fsl_iomuxc_h, sai_tx_configured, sai_write_api_used, lpi2c_blocking_transfer_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | header_fsl_iomuxc_h, sai_tx_configured, sai_write_api_used, lpi2c_blocking_transfer_used |
| `nxp-rt1170-sai-002` | audio | static_analysis | header_fsl_iomuxc_h |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-002` | audio | static_analysis | header_fsl_iomuxc_h |
| `nxp-rt1170-sai-002` | audio | static_analysis | header_fsl_iomuxc_h |
| `nxp-rt1170-sai-002` | audio | static_analysis | header_fsl_iomuxc_h |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `nxp_gcc` | 33 | nxp-mcxc-i2c-001, nxp-mcxc-i2c-001, nxp-mcxc-i2c-001, nxp-mcxc-i2c-001, nxp-mcxc-i2c-001 (+28 more) |
| `header_fsl_port_h` | 17 | nxp-mcxc-gpio-001, nxp-mcxc-gpio-001, nxp-mcxc-gpio-001, nxp-mcxc-gpio-001, nxp-mcxc-gpio-001 (+12 more) |
| `interrupt_flag_cleared` | 16 | nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-rt1170-gpio-002, nxp-rt1170-gpio-002 (+11 more) |
| `header_fsl_iomuxc_h` | 14 | nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-gpio-001, nxp-rt1170-gpio-001 (+9 more) |
| `pit_isr_defined` | 10 | nxp-mcxc-isr-001, nxp-mcxc-isr-001, nxp-mcxc-isr-001, nxp-mcxc-isr-001, nxp-mcxc-isr-001 (+5 more) |
| `flash_init_called` | 5 | nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001 |
| `flash_verify_program_called` | 5 | nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001 |
| `crc_function_implemented` | 5 | nxp-mcxc-flash-002, nxp-mcxc-flash-002, nxp-mcxc-flash-002, nxp-mcxc-flash-002, nxp-mcxc-flash-002 |
| `both_write_and_read_transfers` | 5 | nxp-mcxc-i2c-002, nxp-mcxc-i2c-002, nxp-mcxc-i2c-002, nxp-mcxc-i2c-002, nxp-mcxc-i2c-002 |
| `uart_isr_handler_defined` | 5 | nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002 |
| `read_and_write_api_used` | 5 | nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-audio-001 |
| `edma_transfer_prepared` | 5 | nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001 |
| `edma_transfer_started` | 5 | nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001 |
| `falling_edge_configured` | 5 | nxp-rt1170-gpio-002, nxp-rt1170-gpio-002, nxp-rt1170-gpio-002, nxp-rt1170-gpio-002, nxp-rt1170-gpio-002 |
| `sai_tx_configured` | 5 | nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `sai_write_api_used` | 5 | nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `pin_interrupt_configured` | 4 | nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002 |
| `edma_init_called` | 4 | nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001, nxp-rt1170-dma-001 |
| `full_flash_sequence_present` | 3 | nxp-mcxc-flash-002, nxp-mcxc-flash-002, nxp-mcxc-flash-002 |
| `header_fsl_clock_h` | 3 | nxp-mcxc-gpio-001, nxp-mcxc-isr-001, nxp-mcxc-timer-001 |
| `isr_handler_defined` | 3 | nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-rt1170-gpio-002 |
| `two_separate_transfers` | 3 | nxp-mcxc-i2c-002, nxp-mcxc-i2c-002, nxp-mcxc-i2c-002 |
| `pit_period_set` | 3 | nxp-mcxc-timer-001, nxp-mcxc-timer-001, nxp-mcxc-timer-001 |
| `flash_program_called` | 2 | nxp-mcxc-flash-001, nxp-mcxc-flash-001 |
| `gpio_pin_init_called` | 2 | nxp-rt1170-gpio-001, nxp-rt1170-gpio-001 |
| `lpi2c_blocking_transfer_used` | 2 | nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `flash_erase_sector_called` | 1 | nxp-mcxc-flash-001 |
| `uart_write_blocking_used` | 1 | nxp-mcxc-uart-001 |
| `uart_rx_interrupt_enabled` | 1 | nxp-mcxc-uart-002 |
| `cop_refresh_called` | 1 | nxp-mcxc-watchdog-001 |
| `gpio_toggle_called` | 1 | nxp-rt1170-gpio-001 |
| `rtwdog_init_called` | 1 | nxp-rt1170-rtwdog-001 |

## TC Improvement Suggestions

