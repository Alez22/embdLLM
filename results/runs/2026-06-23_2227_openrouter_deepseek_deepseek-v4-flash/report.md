# Benchmark Report: openrouter/deepseek/deepseek-v4-flash

**Date:** 2026-06-23 22:27 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/deepseek/deepseek-v4-flash |
| Total Cases | 120 |
| Passed | 2 |
| Failed | 118 |
| pass@1 | 1.7% |

## Failed Cases (118)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | header_fsl_flash_h, flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-flash-002` | storage | static_analysis | crc_function_implemented |
| `nxp-mcxc-flash-002` | storage | static_analysis | two_flash_slots_defined |
| `nxp-mcxc-flash-002` | storage | static_analysis | two_flash_slots_defined |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_clock_h, gpio_pin_init_called, gpio_toggle_called |
| `nxp-mcxc-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-i2c-001` | spi-i2c | static_analysis | i2c_blocking_transfer_used |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | both_write_and_read_transfers, two_separate_transfers |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | both_write_and_read_transfers, two_separate_transfers |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-isr-001` | isr-concurrency | static_heuristic | clock_gate_before_gpio_init, nvic_pit_enabled |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | header_fsl_port_h, header_fsl_clock_h |
| `nxp-mcxc-timer-001` | timer | compile_gate | nxp_gcc |
| `nxp-mcxc-timer-001` | timer | compile_gate | nxp_gcc |
| `nxp-mcxc-timer-001` | timer | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-timer-001` | timer | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-timer-001` | timer | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-001` | uart | static_analysis | uart_write_blocking_used |
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
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-audio-001` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-audio-001` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-audio-001` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | static_analysis | edma_transfer_prepared |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | static_analysis | edma_transfer_prepared |
| `nxp-rt1170-gpio-001` | gpio-basic | static_analysis | gpio_toggle_called |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | static_analysis | gpio_toggle_called |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | falling_edge_configured |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | falling_edge_configured |
| `nxp-rt1170-gpio-002` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | isr_handler_defined, falling_edge_configured |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_analysis | header_fsl_clock_h |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_analysis | lpi2c_blocking_transfer_used |
| `nxp-rt1170-lpi2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_analysis | lpi2c_blocking_transfer_used |
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
| `nxp-rt1170-rtwdog-001` | watchdog | static_analysis | rtwdog_init_called, rtwdog_refresh_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | lpi2c_blocking_transfer_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_write_api_used |
| `nxp-rt1170-sai-002` | audio | static_analysis | isr_handler_defined |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `nxp_gcc` | 66 | nxp-mcxc-flash-001, nxp-mcxc-flash-002, nxp-mcxc-flash-002, nxp-mcxc-gpio-001, nxp-mcxc-i2c-001 (+61 more) |
| `header_fsl_clock_h` | 10 | nxp-mcxc-gpio-001, nxp-mcxc-gpio-001, nxp-mcxc-gpio-001, nxp-mcxc-isr-001, nxp-mcxc-isr-001 (+5 more) |
| `interrupt_flag_cleared` | 5 | nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002 |
| `uart_isr_handler_defined` | 5 | nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002 |
| `flash_verify_program_called` | 4 | nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001 |
| `sai_write_api_used` | 4 | nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `gpio_toggle_called` | 3 | nxp-mcxc-gpio-001, nxp-rt1170-gpio-001, nxp-rt1170-gpio-001 |
| `falling_edge_configured` | 3 | nxp-rt1170-gpio-002, nxp-rt1170-gpio-002, nxp-rt1170-gpio-002 |
| `lpi2c_blocking_transfer_used` | 3 | nxp-rt1170-lpi2c-001, nxp-rt1170-lpi2c-001, nxp-rt1170-sai-001 |
| `sai_init_called` | 3 | nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `two_flash_slots_defined` | 2 | nxp-mcxc-flash-002, nxp-mcxc-flash-002 |
| `both_write_and_read_transfers` | 2 | nxp-mcxc-i2c-002, nxp-mcxc-i2c-002 |
| `two_separate_transfers` | 2 | nxp-mcxc-i2c-002, nxp-mcxc-i2c-002 |
| `pit_isr_defined` | 2 | nxp-mcxc-isr-001, nxp-mcxc-isr-001 |
| `edma_transfer_prepared` | 2 | nxp-rt1170-dma-001, nxp-rt1170-dma-001 |
| `isr_handler_defined` | 2 | nxp-rt1170-gpio-002, nxp-rt1170-sai-002 |
| `header_fsl_flash_h` | 1 | nxp-mcxc-flash-001 |
| `crc_function_implemented` | 1 | nxp-mcxc-flash-002 |
| `gpio_pin_init_called` | 1 | nxp-mcxc-gpio-001 |
| `i2c_blocking_transfer_used` | 1 | nxp-mcxc-i2c-001 |
| `clock_gate_before_gpio_init` | 1 | nxp-mcxc-isr-001 |
| `nvic_pit_enabled` | 1 | nxp-mcxc-isr-001 |
| `header_fsl_port_h` | 1 | nxp-mcxc-spi-001 |
| `uart_write_blocking_used` | 1 | nxp-mcxc-uart-001 |
| `read_and_write_api_used` | 1 | nxp-rt1170-audio-001 |
| `header_fsl_iomuxc_h` | 1 | nxp-rt1170-lpuart-001 |
| `rtwdog_init_called` | 1 | nxp-rt1170-rtwdog-001 |
| `rtwdog_refresh_used` | 1 | nxp-rt1170-rtwdog-001 |

## TC Improvement Suggestions

