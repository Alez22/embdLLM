# Benchmark Report: groq/llama-3.3-70b-versatile

**Date:** 2026-06-07 19:40 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/llama-3.3-70b-versatile |
| Total Cases | 25 |
| Passed | 2 |
| Failed | 23 |
| pass@1 | 8.0% |

## Failed Cases (23)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | kconfig_format |
| `kconfig-001` | kconfig | static_analysis | kconfig_format |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-002` | kconfig | static_analysis | bt_hci_enabled |
| `kconfig-002` | kconfig | static_analysis | bt_hci_enabled |
| `kconfig-002` | kconfig | static_analysis | bt_mesh_enabled |
| `kconfig-002` | kconfig | static_analysis | kconfig_format, bt_mesh_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | kconfig_format |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-004` | kconfig | static_analysis | kconfig_format, log_enabled, log_backend_uart_enabled, log_mode_deferred_enabled, log_buffer_size_set |
| `kconfig-004` | kconfig | static_analysis | kconfig_format, log_enabled, log_backend_uart_enabled, log_mode_deferred_enabled, log_buffer_size_set |
| `kconfig-004` | kconfig | static_analysis | log_buffer_size_set |
| `kconfig-004` | kconfig | static_analysis | log_backend_uart_enabled, log_buffer_size_set |
| `kconfig-004` | kconfig | static_analysis | log_buffer_size_set |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_sockopt_tls_enabled, tls_credentials_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_enabled, net_sockets_sockopt_tls_enabled, mbedtls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_enabled, net_sockets_sockopt_tls_enabled, tls_credentials_enabled, mbedtls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled, tls_credentials_enabled |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `kconfig_format` | 6 | kconfig-001, kconfig-001, kconfig-002, kconfig-003, kconfig-004 (+1 more) |
| `log_buffer_size_set` | 5 | kconfig-004, kconfig-004, kconfig-004, kconfig-004, kconfig-004 |
| `networking_enabled` | 4 | kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `net_sockets_sockopt_tls_enabled` | 4 | kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `spi_dma_enabled` | 3 | kconfig-001, kconfig-001, kconfig-001 |
| `uart_line_ctrl_enabled` | 3 | kconfig-003, kconfig-003, kconfig-003 |
| `log_backend_uart_enabled` | 3 | kconfig-004, kconfig-004, kconfig-004 |
| `tls_credentials_enabled` | 3 | kconfig-005, kconfig-005, kconfig-005 |
| `mbedtls_builtin_enabled` | 3 | kconfig-005, kconfig-005, kconfig-005 |
| `bt_hci_enabled` | 2 | kconfig-002, kconfig-002 |
| `bt_mesh_enabled` | 2 | kconfig-002, kconfig-002 |
| `log_enabled` | 2 | kconfig-004, kconfig-004 |
| `log_mode_deferred_enabled` | 2 | kconfig-004, kconfig-004 |
| `net_sockets_enabled` | 2 | kconfig-005, kconfig-005 |
| `mbedtls_enabled` | 2 | kconfig-005, kconfig-005 |

## TC Improvement Suggestions

