# Benchmark Report: groq/openai/gpt-oss-120b

**Date:** 2026-05-25 23:08 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/openai/gpt-oss-120b |
| Total Cases | 12 |
| Passed | 3 |
| Failed | 9 |
| pass@1 | 25.0% |

## Failed Cases (9)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | static_analysis | flash_init_called, flash_erase_sector_called, flash_program_called, flash_verify_program_called |
| `nxp-mcxc-flash-002` | storage | static_analysis | two_flash_slots_defined, full_flash_sequence_present |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-isr-001` | isr-concurrency | static_heuristic | clock_gate_before_gpio_init |
| `nxp-mcxc-spi-001` | spi-i2c | static_heuristic | cs_asserted_before_transfer, cs_deasserted_after_transfer, cs_idle_high_initial_state |
| `nxp-mcxc-timer-001` | timer | static_analysis | pit_isr_defined |
| `nxp-mcxc-uart-001` | uart | static_analysis | header_fsl_clock_h |
| `nxp-mcxc-uart-002` | uart | static_heuristic | ring_buffer_volatile, ring_buffer_indices_volatile |
| `nxp-mcxc-watchdog-001` | watchdog | static_heuristic | long_timeout_configured, cop_refresh_inside_main_loop |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `flash_init_called` | 1 | nxp-mcxc-flash-001 |
| `flash_erase_sector_called` | 1 | nxp-mcxc-flash-001 |
| `flash_program_called` | 1 | nxp-mcxc-flash-001 |
| `flash_verify_program_called` | 1 | nxp-mcxc-flash-001 |
| `two_flash_slots_defined` | 1 | nxp-mcxc-flash-002 |
| `full_flash_sequence_present` | 1 | nxp-mcxc-flash-002 |
| `interrupt_flag_cleared` | 1 | nxp-mcxc-gpio-002 |
| `clock_gate_before_gpio_init` | 1 | nxp-mcxc-isr-001 |
| `cs_asserted_before_transfer` | 1 | nxp-mcxc-spi-001 |
| `cs_deasserted_after_transfer` | 1 | nxp-mcxc-spi-001 |
| `cs_idle_high_initial_state` | 1 | nxp-mcxc-spi-001 |
| `pit_isr_defined` | 1 | nxp-mcxc-timer-001 |
| `header_fsl_clock_h` | 1 | nxp-mcxc-uart-001 |
| `ring_buffer_volatile` | 1 | nxp-mcxc-uart-002 |
| `ring_buffer_indices_volatile` | 1 | nxp-mcxc-uart-002 |
| `long_timeout_configured` | 1 | nxp-mcxc-watchdog-001 |
| `cop_refresh_inside_main_loop` | 1 | nxp-mcxc-watchdog-001 |

## TC Improvement Suggestions

