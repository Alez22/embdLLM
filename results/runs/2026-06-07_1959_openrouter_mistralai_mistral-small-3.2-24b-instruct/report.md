# Benchmark Report: openrouter/mistralai/mistral-small-3.2-24b-instruct

**Date:** 2026-06-07 19:59 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/mistralai/mistral-small-3.2-24b-instruct |
| Total Cases | 40 |
| Passed | 2 |
| Failed | 38 |
| pass@1 | 5.0% |

## Failed Cases (38)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-002` | kconfig | static_analysis | kconfig_format |
| `kconfig-002` | kconfig | static_analysis | kconfig_format, bt_hci_enabled |
| `kconfig-002` | kconfig | static_analysis | bt_hci_enabled |
| `kconfig-002` | kconfig | static_analysis | kconfig_format, bt_mesh_enabled, bt_mesh_relay_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | usb_device_stack_enabled, usb_cdc_acm_enabled, uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-004` | kconfig | static_analysis | log_mode_deferred_enabled |
| `kconfig-004` | kconfig | static_analysis | log_mode_deferred_enabled |
| `kconfig-004` | kconfig | static_analysis | log_mode_deferred_enabled |
| `kconfig-004` | kconfig | static_analysis | log_backend_uart_enabled, log_mode_deferred_enabled |
| `kconfig-004` | kconfig | static_analysis | log_backend_uart_enabled, log_mode_deferred_enabled |
| `kconfig-005` | kconfig | static_analysis | llm_call |
| `kconfig-005` | kconfig | static_analysis | llm_call |
| `kconfig-005` | kconfig | static_analysis | llm_call |
| `kconfig-005` | kconfig | static_analysis | llm_call |
| `kconfig-005` | kconfig | static_analysis | llm_call |
| `kconfig-006` | kconfig | static_analysis | llm_call |
| `kconfig-006` | kconfig | static_analysis | llm_call |
| `kconfig-006` | kconfig | static_analysis | llm_call |
| `kconfig-006` | kconfig | static_analysis | llm_call |
| `kconfig-006` | kconfig | static_analysis | llm_call |
| `kconfig-007` | kconfig | static_analysis | llm_call |
| `kconfig-007` | kconfig | static_analysis | llm_call |
| `kconfig-007` | kconfig | static_analysis | llm_call |
| `kconfig-007` | kconfig | static_analysis | llm_call |
| `kconfig-007` | kconfig | static_analysis | llm_call |
| `kconfig-008` | kconfig | static_analysis | llm_call |
| `kconfig-008` | kconfig | static_analysis | llm_call |
| `kconfig-008` | kconfig | static_analysis | llm_call |
| `kconfig-008` | kconfig | static_analysis | llm_call |
| `kconfig-008` | kconfig | static_analysis | llm_call |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `llm_call` | 20 | kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005 (+15 more) |
| `uart_line_ctrl_enabled` | 5 | kconfig-003, kconfig-003, kconfig-003, kconfig-003, kconfig-003 |
| `log_mode_deferred_enabled` | 5 | kconfig-004, kconfig-004, kconfig-004, kconfig-004, kconfig-004 |
| `spi_dma_enabled` | 4 | kconfig-001, kconfig-001, kconfig-001, kconfig-001 |
| `kconfig_format` | 3 | kconfig-002, kconfig-002, kconfig-002 |
| `bt_hci_enabled` | 2 | kconfig-002, kconfig-002 |
| `log_backend_uart_enabled` | 2 | kconfig-004, kconfig-004 |
| `bt_mesh_enabled` | 1 | kconfig-002 |
| `bt_mesh_relay_enabled` | 1 | kconfig-002 |
| `usb_device_stack_enabled` | 1 | kconfig-003 |
| `usb_cdc_acm_enabled` | 1 | kconfig-003 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 15 | kconfig-001, kconfig-001, kconfig-001, kconfig-001, kconfig-002 (+10 more) |
| LLM format failure (prose) | 23 | kconfig-002, kconfig-002, kconfig-002, kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-006, kconfig-006, kconfig-006, kconfig-006, kconfig-006, kconfig-007, kconfig-007, kconfig-007, kconfig-007, kconfig-007, kconfig-008, kconfig-008, kconfig-008, kconfig-008, kconfig-008 |

*Adjusted pass@1 (excluding format failures): 11.8% (2/17)*


## TC Improvement Suggestions

