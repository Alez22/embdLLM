# Benchmark Report: openrouter/qwen/qwen3-235b-a22b-2507

**Date:** 2026-06-17 17:50 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/qwen/qwen3-235b-a22b-2507 |
| Total Cases | 48 |
| Passed | 8 |
| Failed | 40 |
| pass@1 | 16.7% |

## Failed Cases (40)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_verify_program_called |
| `nxp-mcxc-flash-002` | storage | static_heuristic | verify_after_each_write, crc_excludes_crc_field |
| `nxp-mcxc-flash-002` | storage | static_analysis | full_flash_sequence_present |
| `nxp-mcxc-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | pin_interrupt_configured |
| `nxp-mcxc-gpio-002` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | gpio_pin_read_in_code |
| `nxp-mcxc-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-mcxc-spi-001` | spi-i2c | static_heuristic | cs_idle_high_initial_state |
| `nxp-mcxc-spi-001` | spi-i2c | static_analysis | spi_master_init_called |
| `nxp-mcxc-timer-001` | timer | static_analysis | pit_isr_defined |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-watchdog-001` | watchdog | static_heuristic | lpo_clock_source_used, long_timeout_configured |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-dma-001` | dma | static_heuristic | dcache_invalidate_after_transfer, dma_buffers_cache_aligned, done_flag_volatile |
| `nxp-rt1170-dma-001` | dma | static_analysis | edma_transfer_started |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | static_heuristic | gpio_port_interrupts_enabled |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared, falling_edge_configured |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `nxp-rt1170-isr-001` | isr-concurrency | static_heuristic | critical_section_around_read |
| `nxp-rt1170-isr-001` | isr-concurrency | compile_gate | nxp_gcc |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_analysis | lpi2c_blocking_transfer_used |
| `nxp-rt1170-lpi2c-001` | spi-i2c | static_analysis | lpi2c_blocking_transfer_used |
| `nxp-rt1170-lpspi-001` | spi-i2c | static_heuristic | iomuxc_before_lpspi_init, clock_root_configured |
| `nxp-rt1170-lpspi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-rt1170-lpuart-001` | uart | static_heuristic | iomuxc_before_lpuart_init, clock_root_configured, init_status_checked |
| `nxp-rt1170-lpuart-001` | uart | compile_gate | nxp_gcc |
| `nxp-rt1170-rtwdog-001` | watchdog | static_analysis | llm_call |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_tx_configured, sai_write_api_used, lpi2c_blocking_transfer_used |
| `nxp-rt1170-sai-001` | audio | static_analysis | llm_call |
| `nxp-rt1170-sai-002` | audio | static_heuristic | iomuxc_before_sai_init, bit_clock_rate_set, fifo_interrupt_enabled, tx_enabled, fifo_underrun_handled |
| `nxp-rt1170-sai-002` | audio | static_analysis | llm_call |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `nxp_gcc` | 12 | nxp-mcxc-gpio-001, nxp-mcxc-gpio-002, nxp-mcxc-i2c-001, nxp-mcxc-i2c-002, nxp-mcxc-isr-001 (+7 more) |
| `lpi2c_blocking_transfer_used` | 3 | nxp-rt1170-lpi2c-001, nxp-rt1170-lpi2c-001, nxp-rt1170-sai-001 |
| `llm_call` | 3 | nxp-rt1170-rtwdog-001, nxp-rt1170-sai-001, nxp-rt1170-sai-002 |
| `flash_verify_program_called` | 2 | nxp-mcxc-flash-001, nxp-mcxc-flash-001 |
| `uart_isr_handler_defined` | 2 | nxp-mcxc-uart-002, nxp-mcxc-uart-002 |
| `read_and_write_api_used` | 2 | nxp-rt1170-audio-001, nxp-rt1170-audio-001 |
| `clock_root_configured` | 2 | nxp-rt1170-lpspi-001, nxp-rt1170-lpuart-001 |
| `verify_after_each_write` | 1 | nxp-mcxc-flash-002 |
| `crc_excludes_crc_field` | 1 | nxp-mcxc-flash-002 |
| `full_flash_sequence_present` | 1 | nxp-mcxc-flash-002 |
| `pin_interrupt_configured` | 1 | nxp-mcxc-gpio-002 |
| `gpio_pin_read_in_code` | 1 | nxp-mcxc-isr-001 |
| `cs_idle_high_initial_state` | 1 | nxp-mcxc-spi-001 |
| `spi_master_init_called` | 1 | nxp-mcxc-spi-001 |
| `pit_isr_defined` | 1 | nxp-mcxc-timer-001 |
| `lpo_clock_source_used` | 1 | nxp-mcxc-watchdog-001 |
| `long_timeout_configured` | 1 | nxp-mcxc-watchdog-001 |
| `dcache_invalidate_after_transfer` | 1 | nxp-rt1170-dma-001 |
| `dma_buffers_cache_aligned` | 1 | nxp-rt1170-dma-001 |
| `done_flag_volatile` | 1 | nxp-rt1170-dma-001 |
| `edma_transfer_started` | 1 | nxp-rt1170-dma-001 |
| `gpio_port_interrupts_enabled` | 1 | nxp-rt1170-gpio-002 |
| `interrupt_flag_cleared` | 1 | nxp-rt1170-gpio-002 |
| `falling_edge_configured` | 1 | nxp-rt1170-gpio-002 |
| `critical_section_around_read` | 1 | nxp-rt1170-isr-001 |
| `iomuxc_before_lpspi_init` | 1 | nxp-rt1170-lpspi-001 |
| `iomuxc_before_lpuart_init` | 1 | nxp-rt1170-lpuart-001 |
| `init_status_checked` | 1 | nxp-rt1170-lpuart-001 |
| `sai_tx_configured` | 1 | nxp-rt1170-sai-001 |
| `sai_write_api_used` | 1 | nxp-rt1170-sai-001 |
| `iomuxc_before_sai_init` | 1 | nxp-rt1170-sai-002 |
| `bit_clock_rate_set` | 1 | nxp-rt1170-sai-002 |
| `fifo_interrupt_enabled` | 1 | nxp-rt1170-sai-002 |
| `tx_enabled` | 1 | nxp-rt1170-sai-002 |
| `fifo_underrun_handled` | 1 | nxp-rt1170-sai-002 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 37 | nxp-mcxc-flash-001, nxp-mcxc-flash-001, nxp-mcxc-flash-002, nxp-mcxc-flash-002, nxp-mcxc-gpio-001 (+32 more) |
| LLM format failure (prose) | 3 | nxp-rt1170-rtwdog-001, nxp-rt1170-sai-001, nxp-rt1170-sai-002 |

*Adjusted pass@1 (excluding format failures): 17.8% (8/45)*


## TC Improvement Suggestions

