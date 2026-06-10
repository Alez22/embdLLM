# Benchmark Report: groq/qwen/qwen3-32b

**Date:** 2026-06-07 20:31 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/qwen/qwen3-32b |
| Total Cases | 40 |
| Passed | 22 |
| Failed | 18 |
| pass@1 | 55.0% |

## Failed Cases (18)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-002` | kconfig | static_analysis | bt_enabled, bt_hci_enabled, bt_mesh_enabled, bt_mesh_relay_enabled |
| `kconfig-002` | kconfig | static_analysis | kconfig_format, bt_mesh_enabled, bt_mesh_relay_enabled |
| `kconfig-003` | kconfig | static_analysis | code_extracted |
| `kconfig-003` | kconfig | static_analysis | code_extracted |
| `kconfig-003` | kconfig | static_analysis | code_extracted |
| `kconfig-003` | kconfig | static_analysis | code_extracted |
| `kconfig-003` | kconfig | static_analysis | code_extracted |
| `kconfig-004` | kconfig | static_analysis | log_backend_uart_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_enabled, net_sockets_sockopt_tls_enabled, tls_credentials_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | kconfig_format, networking_enabled, net_sockets_sockopt_tls_enabled, tls_credentials_enabled, mbedtls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled, tls_credentials_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | kconfig_format, net_sockets_sockopt_tls_enabled, tls_credentials_enabled, mbedtls_enabled, mbedtls_builtin_enabled |
| `kconfig-007` | kconfig | static_heuristic | no_hallucinated_config_options |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `code_extracted` | 5 | kconfig-003, kconfig-003, kconfig-003, kconfig-003, kconfig-003 |
| `net_sockets_sockopt_tls_enabled` | 5 | kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `mbedtls_builtin_enabled` | 5 | kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `spi_dma_enabled` | 4 | kconfig-001, kconfig-001, kconfig-001, kconfig-001 |
| `tls_credentials_enabled` | 4 | kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `kconfig_format` | 3 | kconfig-002, kconfig-005, kconfig-005 |
| `bt_mesh_enabled` | 2 | kconfig-002, kconfig-002 |
| `bt_mesh_relay_enabled` | 2 | kconfig-002, kconfig-002 |
| `mbedtls_enabled` | 2 | kconfig-005, kconfig-005 |
| `bt_enabled` | 1 | kconfig-002 |
| `bt_hci_enabled` | 1 | kconfig-002 |
| `log_backend_uart_enabled` | 1 | kconfig-004 |
| `net_sockets_enabled` | 1 | kconfig-005 |
| `networking_enabled` | 1 | kconfig-005 |
| `no_hallucinated_config_options` | 1 | kconfig-007 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 13 | kconfig-001, kconfig-001, kconfig-001, kconfig-001, kconfig-002 (+8 more) |
| LLM format failure (prose) | 5 | kconfig-003, kconfig-003, kconfig-003, kconfig-003, kconfig-003 |

*Adjusted pass@1 (excluding format failures): 62.9% (22/35)*


## TC Improvement Suggestions

