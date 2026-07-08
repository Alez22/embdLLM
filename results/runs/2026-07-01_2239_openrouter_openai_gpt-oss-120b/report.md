# Benchmark Report: openrouter/openai/gpt-oss-120b

**Date:** 2026-07-01 22:39 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/openai/gpt-oss-120b |
| Total Cases | 108 |
| Passed | 1 |
| Failed | 107 |
| pass@1 | 0.9% |

## Failed Cases (107)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-002` | storage | static_analysis | two_flash_slots_defined |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-flash-002` | storage | static_analysis | two_flash_slots_defined |
| `nxp-mcxc-flash-002` | storage | static_analysis | two_flash_slots_defined |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | pin_interrupt_configured, interrupt_flag_cleared |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | header_fsl_port_h |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined |
| `nxp-mcxc-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-mcxc-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
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
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-audio-001` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | static_analysis | edma_transfer_prepared |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | static_analysis | gpio_toggle_called |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | falling_edge_configured |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | isr_handler_defined, falling_edge_configured |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | isr_handler_defined |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | isr_handler_defined |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | falling_edge_configured |
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
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | header_fsl_iomuxc_h, sai_init_called, sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_write_api_used |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-002` | audio | static_analysis | no_blocking_write |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `nxp_gcc` | 69 | nxp-mcxc-gpio-001, nxp-mcxc-i2c-001, nxp-mcxc-flash-002, nxp-mcxc-flash-002, nxp-mcxc-i2c-002 (+64 more) |
| `flash_verify_program_called` | 5 | nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001 |
| `pit_isr_defined` | 5 | nxp-mcxc-isr-001, nxp-mcxc-isr-001, nxp-mcxc-isr-001, nxp-mcxc-timer-001, nxp-mcxc-timer-001 |
| `uart_isr_handler_defined` | 5 | nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002 |
| `sai_init_called` | 5 | nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `read_and_write_api_used` | 4 | nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-audio-001 |
| `two_flash_slots_defined` | 3 | nxp-mcxc-flash-002, nxp-mcxc-flash-002, nxp-mcxc-flash-002 |
| `falling_edge_configured` | 3 | nxp-rt1170-gpio-002, nxp-rt1170-gpio-002, nxp-rt1170-gpio-002 |
| `isr_handler_defined` | 3 | nxp-rt1170-gpio-002, nxp-rt1170-gpio-002, nxp-rt1170-gpio-002 |
| `sai_write_api_used` | 3 | nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `header_fsl_port_h` | 2 | nxp-mcxc-i2c-002, nxp-mcxc-i2c-002 |
| `pin_interrupt_configured` | 1 | nxp-mcxc-gpio-002 |
| `interrupt_flag_cleared` | 1 | nxp-mcxc-gpio-002 |
| `edma_transfer_prepared` | 1 | nxp-rt1170-dma-001 |
| `gpio_toggle_called` | 1 | nxp-rt1170-gpio-001 |
| `header_fsl_iomuxc_h` | 1 | nxp-rt1170-sai-001 |
| `no_blocking_write` | 1 | nxp-rt1170-sai-002 |

## TC Improvement Suggestions

