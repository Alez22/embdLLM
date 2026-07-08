# Benchmark Report: openrouter/anthropic/claude-sonnet-4.6

**Date:** 2026-06-14 15:27 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/anthropic/claude-sonnet-4.6 |
| Total Cases | 24 |
| Passed | 6 |
| Failed | 18 |
| pass@1 | 25.0% |

## Failed Cases (18)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_erase_sector_called |
| `nxp-mcxc-flash-002` | storage | static_heuristic | crc_excludes_crc_field, flash_erase_key_used |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | pin_interrupt_configured, interrupt_flag_cleared |
| `nxp-mcxc-i2c-001` | spi-i2c | static_heuristic | clock_gate_before_i2c_init, pinmux_before_i2c_init, default_transfer_flag_set |
| `nxp-mcxc-i2c-002` | spi-i2c | static_heuristic | both_transfer_returns_checked |
| `nxp-mcxc-spi-001` | spi-i2c | static_heuristic | cs_asserted_before_transfer |
| `nxp-mcxc-timer-001` | timer | static_heuristic | clock_gate_before_pit_init |
| `nxp-mcxc-uart-002` | uart | static_heuristic | clock_gate_before_uart_init, rx_flag_checked_in_isr |
| `nxp-mcxc-watchdog-001` | watchdog | static_heuristic | long_timeout_configured |
| `nxp-rt1170-audio-001` | audio | static_analysis | read_and_write_api_used |
| `nxp-rt1170-dma-001` | dma | static_heuristic | dcache_coherency_handled, dcache_clean_before_start, dcache_invalidate_after_transfer |
| `nxp-rt1170-gpio-001` | gpio-basic | static_heuristic | iomuxc_before_gpio_init, pad_config_set |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | header_fsl_gpio_h, header_fsl_iomuxc_h, interrupt_flag_cleared, falling_edge_configured |
| `nxp-rt1170-isr-001` | isr-concurrency | static_analysis | isr_handler_defined |
| `nxp-rt1170-lpuart-001` | uart | static_analysis | baud_rate_configured |
| `nxp-rt1170-rtwdog-001` | watchdog | static_heuristic | refresh_inside_main_loop |
| `nxp-rt1170-sai-001` | audio | static_analysis | sai_init_called, sai_write_api_used |
| `nxp-rt1170-sai-002` | audio | static_heuristic | bit_clock_rate_set |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `interrupt_flag_cleared` | 2 | nxp-mcxc-gpio-002, nxp-rt1170-gpio-002 |
| `flash_erase_sector_called` | 1 | nxp-mcxc-flash-001 |
| `crc_excludes_crc_field` | 1 | nxp-mcxc-flash-002 |
| `flash_erase_key_used` | 1 | nxp-mcxc-flash-002 |
| `pin_interrupt_configured` | 1 | nxp-mcxc-gpio-002 |
| `clock_gate_before_i2c_init` | 1 | nxp-mcxc-i2c-001 |
| `pinmux_before_i2c_init` | 1 | nxp-mcxc-i2c-001 |
| `default_transfer_flag_set` | 1 | nxp-mcxc-i2c-001 |
| `both_transfer_returns_checked` | 1 | nxp-mcxc-i2c-002 |
| `cs_asserted_before_transfer` | 1 | nxp-mcxc-spi-001 |
| `clock_gate_before_pit_init` | 1 | nxp-mcxc-timer-001 |
| `clock_gate_before_uart_init` | 1 | nxp-mcxc-uart-002 |
| `rx_flag_checked_in_isr` | 1 | nxp-mcxc-uart-002 |
| `long_timeout_configured` | 1 | nxp-mcxc-watchdog-001 |
| `read_and_write_api_used` | 1 | nxp-rt1170-audio-001 |
| `dcache_coherency_handled` | 1 | nxp-rt1170-dma-001 |
| `dcache_clean_before_start` | 1 | nxp-rt1170-dma-001 |
| `dcache_invalidate_after_transfer` | 1 | nxp-rt1170-dma-001 |
| `iomuxc_before_gpio_init` | 1 | nxp-rt1170-gpio-001 |
| `pad_config_set` | 1 | nxp-rt1170-gpio-001 |
| `header_fsl_gpio_h` | 1 | nxp-rt1170-gpio-002 |
| `header_fsl_iomuxc_h` | 1 | nxp-rt1170-gpio-002 |
| `falling_edge_configured` | 1 | nxp-rt1170-gpio-002 |
| `isr_handler_defined` | 1 | nxp-rt1170-isr-001 |
| `baud_rate_configured` | 1 | nxp-rt1170-lpuart-001 |
| `refresh_inside_main_loop` | 1 | nxp-rt1170-rtwdog-001 |
| `sai_init_called` | 1 | nxp-rt1170-sai-001 |
| `sai_write_api_used` | 1 | nxp-rt1170-sai-001 |
| `bit_clock_rate_set` | 1 | nxp-rt1170-sai-002 |

## TC Improvement Suggestions

