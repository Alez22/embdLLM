# Benchmark Report: openrouter/z-ai/glm-5.2

**Date:** 2026-07-02 00:21 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/z-ai/glm-5.2 |
| Total Cases | 120 |
| Passed | 8 |
| Failed | 112 |
| pass@1 | 6.7% |

## Failed Cases (112)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_heuristic | flash_return_value_checked, flash_erase_key_used |
| `nxp-mcxc-flash-001` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared, isr_handler_defined |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | static_analysis | two_separate_transfers |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined |
| `nxp-mcxc-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-mcxc-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-timer-001` | timer | static_analysis | pit_isr_defined |
| `nxp-mcxc-timer-001` | timer | compile_gate | nxp_gcc |
| `nxp-mcxc-timer-001` | timer | compile_gate | nxp_gcc |
| `nxp-mcxc-timer-001` | timer | compile_gate | nxp_gcc |
| `nxp-mcxc-timer-001` | timer | static_analysis | pit_isr_defined |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-001` | uart | static_analysis | header_fsl_port_h |
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
| `nxp-rt1170-audio-001` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | static_analysis | llm_call |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_heuristic | clock_root_configured |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_heuristic | transfer_return_value_checked |
| `nxp-rt1170-lpi2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpi2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_heuristic | clock_root_configured, transfer_return_value_checked |
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
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, lpi2c_blocking_transfer_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_write_api_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_write_api_used, lpi2c_blocking_transfer_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | llm_call |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_write_api_used |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-sai-002` | audio | compile_gate | nxp_gcc |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `nxp_gcc` | 80 | nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-002, nxp-mcxc-flash-002, nxp-mcxc-flash-002 (+75 more) |
| `interrupt_flag_cleared` | 6 | nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002, nxp-mcxc-gpio-002 (+1 more) |
| `uart_isr_handler_defined` | 5 | nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002, nxp-mcxc-uart-002 |
| `pit_isr_defined` | 4 | nxp-mcxc-isr-001, nxp-mcxc-isr-001, nxp-mcxc-timer-001, nxp-mcxc-timer-001 |
| `sai_init_called` | 4 | nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `read_and_write_api_used` | 3 | nxp-rt1170-audio-001, nxp-rt1170-audio-001, nxp-rt1170-audio-001 |
| `sai_write_api_used` | 3 | nxp-rt1170-sai-001, nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `flash_verify_program_called` | 2 | nxp-mcxc-flash-001, nxp-mcxc-flash-001 |
| `llm_call` | 2 | nxp-rt1170-isr-001, nxp-rt1170-sai-001 |
| `clock_root_configured` | 2 | nxp-rt1170-lpi2c-001, nxp-rt1170-lpi2c-001 |
| `transfer_return_value_checked` | 2 | nxp-rt1170-lpi2c-001, nxp-rt1170-lpi2c-001 |
| `lpi2c_blocking_transfer_used` | 2 | nxp-rt1170-sai-001, nxp-rt1170-sai-001 |
| `flash_return_value_checked` | 1 | nxp-mcxc-flash-001 |
| `flash_erase_key_used` | 1 | nxp-mcxc-flash-001 |
| `isr_handler_defined` | 1 | nxp-mcxc-gpio-002 |
| `two_separate_transfers` | 1 | nxp-mcxc-i2c-002 |
| `header_fsl_port_h` | 1 | nxp-mcxc-uart-001 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 110 | nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-001 (+105 more) |
| LLM format failure (prose) | 2 | nxp-rt1170-isr-001, nxp-rt1170-sai-001 |

*Adjusted pass@1 (excluding format failures): 6.8% (8/118)*


## TC Improvement Suggestions

