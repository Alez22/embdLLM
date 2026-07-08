# Benchmark Report: openrouter/google/gemma-4-31b-it

**Date:** 2026-06-13 10:35 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/google/gemma-4-31b-it |
| Total Cases | 40 |
| Passed | 32 |
| Failed | 8 |
| pass@1 | 80.0% |

## Failed Cases (8)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled, tls_credentials_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_enabled, net_sockets_sockopt_tls_enabled, tls_credentials_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled, tls_credentials_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `net_sockets_sockopt_tls_enabled` | 5 | kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `spi_dma_enabled` | 3 | kconfig-001, kconfig-001, kconfig-001 |
| `tls_credentials_enabled` | 3 | kconfig-005, kconfig-005, kconfig-005 |
| `mbedtls_builtin_enabled` | 2 | kconfig-005, kconfig-005 |
| `net_sockets_enabled` | 1 | kconfig-005 |

## TC Improvement Suggestions

