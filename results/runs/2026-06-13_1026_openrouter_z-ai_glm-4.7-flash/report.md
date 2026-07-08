# Benchmark Report: openrouter/z-ai/glm-4.7-flash

**Date:** 2026-06-13 10:26 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/z-ai/glm-4.7-flash |
| Total Cases | 40 |
| Passed | 24 |
| Failed | 16 |
| pass@1 | 60.0% |

## Failed Cases (16)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | dma_enabled |
| `kconfig-002` | kconfig | static_analysis | bt_hci_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | usb_device_stack_enabled, uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-004` | kconfig | static_analysis | log_mode_deferred_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_sockopt_tls_enabled, tls_credentials_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_enabled, net_sockets_sockopt_tls_enabled, tls_credentials_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_sockopt_tls_enabled, mbedtls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled, tls_credentials_enabled, mbedtls_builtin_enabled |
| `kconfig-007` | kconfig | static_heuristic | no_hallucinated_config_options |
| `kconfig-007` | kconfig | static_heuristic | no_hallucinated_config_options |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `uart_line_ctrl_enabled` | 5 | kconfig-003, kconfig-003, kconfig-003, kconfig-003, kconfig-003 |
| `net_sockets_sockopt_tls_enabled` | 5 | kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `mbedtls_builtin_enabled` | 4 | kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `networking_enabled` | 3 | kconfig-005, kconfig-005, kconfig-005 |
| `tls_credentials_enabled` | 3 | kconfig-005, kconfig-005, kconfig-005 |
| `no_hallucinated_config_options` | 2 | kconfig-007, kconfig-007 |
| `spi_dma_enabled` | 1 | kconfig-001 |
| `dma_enabled` | 1 | kconfig-001 |
| `bt_hci_enabled` | 1 | kconfig-002 |
| `usb_device_stack_enabled` | 1 | kconfig-003 |
| `log_mode_deferred_enabled` | 1 | kconfig-004 |
| `net_sockets_enabled` | 1 | kconfig-005 |
| `mbedtls_enabled` | 1 | kconfig-005 |

## TC Improvement Suggestions

