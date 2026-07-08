# Benchmark Report: openrouter/qwen/qwen3-235b-a22b-2507

**Date:** 2026-06-13 12:33 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/qwen/qwen3-235b-a22b-2507 |
| Total Cases | 40 |
| Passed | 31 |
| Failed | 9 |
| pass@1 | 77.5% |

## Failed Cases (9)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `kconfig-003` | kconfig | static_analysis | usb_cdc_acm_enabled |
| `kconfig-004` | kconfig | static_analysis | log_buffer_size_set |
| `kconfig-004` | kconfig | static_analysis | log_buffer_size_set |
| `kconfig-005` | kconfig | static_analysis | mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | tls_credentials_enabled, mbedtls_builtin_enabled |
| `kconfig-007` | kconfig | static_analysis | networking_enabled |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `mbedtls_builtin_enabled` | 5 | kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `log_buffer_size_set` | 2 | kconfig-004, kconfig-004 |
| `networking_enabled` | 2 | kconfig-005, kconfig-007 |
| `usb_cdc_acm_enabled` | 1 | kconfig-003 |
| `net_sockets_sockopt_tls_enabled` | 1 | kconfig-005 |
| `tls_credentials_enabled` | 1 | kconfig-005 |

## TC Improvement Suggestions

