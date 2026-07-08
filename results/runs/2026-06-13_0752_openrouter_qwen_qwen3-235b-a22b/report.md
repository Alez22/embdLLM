# Benchmark Report: openrouter/qwen/qwen3-235b-a22b

**Date:** 2026-06-13 07:52 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/qwen/qwen3-235b-a22b |
| Total Cases | 40 |
| Passed | 28 |
| Failed | 12 |
| pass@1 | 70.0% |

## Failed Cases (12)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-003` | kconfig | static_analysis | usb_device_stack_enabled, uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-004` | kconfig | static_analysis | log_buffer_size_set |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled, tls_credentials_enabled, mbedtls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled, tls_credentials_enabled, mbedtls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, tls_credentials_enabled, mbedtls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_sockopt_tls_enabled, tls_credentials_enabled, mbedtls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_sockopt_tls_enabled, tls_credentials_enabled, mbedtls_builtin_enabled |
| `kconfig-007` | kconfig | static_heuristic | no_hallucinated_config_options |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `tls_credentials_enabled` | 5 | kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `mbedtls_builtin_enabled` | 5 | kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `net_sockets_sockopt_tls_enabled` | 4 | kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `mbedtls_enabled` | 4 | kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `uart_line_ctrl_enabled` | 3 | kconfig-003, kconfig-003, kconfig-003 |
| `networking_enabled` | 3 | kconfig-005, kconfig-005, kconfig-005 |
| `spi_dma_enabled` | 2 | kconfig-001, kconfig-001 |
| `usb_device_stack_enabled` | 1 | kconfig-003 |
| `log_buffer_size_set` | 1 | kconfig-004 |
| `no_hallucinated_config_options` | 1 | kconfig-007 |

## TC Improvement Suggestions

