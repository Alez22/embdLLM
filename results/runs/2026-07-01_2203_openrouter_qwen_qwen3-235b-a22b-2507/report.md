# Benchmark Report: openrouter/qwen/qwen3-235b-a22b-2507

**Date:** 2026-07-01 22:03 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/qwen/qwen3-235b-a22b-2507 |
| Total Cases | 120 |
| Passed | 0 |
| Failed | 120 |
| pass@1 | 0.0% |

## Failed Cases (120)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-flash-002` | storage | static_analysis | full_flash_sequence_present |
| `nxp-mcxc-flash-002` | storage | static_analysis | full_flash_sequence_present |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_port_h |
| `nxp-mcxc-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | pin_interrupt_configured |
| `nxp-mcxc-gpio-002` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | header_fsl_clock_h, interrupt_flag_cleared |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | header_fsl_clock_h, interrupt_flag_cleared |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | header_fsl_clock_h, pin_interrupt_configured, interrupt_flag_cleared |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | i2c_master_init_called |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | gpio_pin_read_in_code |
| `nxp-mcxc-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | gpio_pin_read_in_code |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | gpio_pin_read_in_code |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined, gpio_pin_read_in_code |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | spi_master_init_called |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h, spi_master_init_called, spi_blocking_transfer_used |
| `nxp-mcxc-timer-001` | timer | compile_gate | nxp_gcc |
| `nxp-mcxc-timer-001` | timer | static_analysis | pit_isr_defined |
| `nxp-mcxc-timer-001` | timer | static_analysis | pit_isr_defined |
| `nxp-mcxc-timer-001` | timer | compile_gate | nxp_gcc |
| `nxp-mcxc-timer-001` | timer | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-mcxc-watchdog-001` | watchdog | static_analysis | cop_refresh_called |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | static_analysis | edma_transfer_started |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared, falling_edge_configured |
| `nxp-rt1170-gpio-002` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-gpt-001` | timer | static_analysis | isr_handler_defined, interrupt_flag_cleared |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_analysis | lpi2c_blocking_transfer_used |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_analysis | lpi2c_blocking_transfer_used |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_analysis | header_fsl_iomuxc_h, lpi2c_blocking_transfer_used |
| `nxp-rt1170-lpi2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpi2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpspi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpspi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpspi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpspi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpspi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | static_analysis | header_fsl_iomuxc_h |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_tx_configured, sai_write_api_used, lpi2c_blocking_transfer_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_tx_configured, sai_write_api_used, lpi2c_blocking_transfer_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_tx_configured, lpi2c_blocking_transfer_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_tx_configured, lpi2c_blocking_transfer_used |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `nxp_gcc` | 76 | nxp-mcxc-flash-002, nxp-mcxc-flash-002, nxp-mcxc-flash-002, nxp-mcxc-gpio-001, nxp-mcxc-gpio-001 (+71 more) |
| `lpi2c_blocking_transfer_used` | 7 | nxp-rt1170-lpi2c-001, nxp-rt1170-lpi2c-001, nxp-rt1170-lpi2c-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001 (+2 more) |
| `flash_verify_program_called` | 5 | nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001 |
| `interrupt_flag_cleared` | 5 | nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-rt1170-gpio-002, nxp-rt1170-gpt-001 |
| `uart_isr_handler_defined` | 5 | nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002 |
| `read_and_write_api_used` | 5 | nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-audio-001 |
| `gpio_pin_read_in_code` | 4 | nxp-mcxc-isr-001, nxp-mcxc-isr-001, nxp-mcxc-isr-001, nxp-mcxc-isr-001 |
| `sai_tx_configured` | 4 | nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `header_fsl_clock_h` | 3 | nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002 |
| `pit_isr_defined` | 3 | nxp-mcxc-isr-001, nxp-mcxc-timer-001, nxp-mcxc-timer-001 |
| `sai_write_api_used` | 3 | nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `full_flash_sequence_present` | 2 | nxp-mcxc-flash-002, nxp-mcxc-flash-002 |
| `header_fsl_port_h` | 2 | nxp-mcxc-gpio-001, nxp-mcxc-spi-001 |
| `pin_interrupt_configured` | 2 | nxp-mcxc-gpio-002, nxp-mcxc-gpio-002 |
| `spi_master_init_called` | 2 | nxp-mcxc-spi-001, nxp-mcxc-spi-001 |
| `header_fsl_iomuxc_h` | 2 | nxp-rt1170-lpi2c-001, nxp-rt1170-lpuart-001 |
| `i2c_master_init_called` | 1 | nxp-mcxc-i2c-002 |
| `spi_blocking_transfer_used` | 1 | nxp-mcxc-spi-001 |
| `cop_refresh_called` | 1 | nxp-mcxc-watchdog-001 |
| `edma_transfer_started` | 1 | nxp-rt1170-dma-001 |
| `falling_edge_configured` | 1 | nxp-rt1170-gpio-002 |
| `isr_handler_defined` | 1 | nxp-rt1170-gpt-001 |

## TC Improvement Suggestions

