# Benchmark Report: groq/meta-llama/llama-4-scout-17b-16e-instruct

**Date:** 2026-06-07 20:18 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/meta-llama/llama-4-scout-17b-16e-instruct |
| Total Cases | 40 |
| Passed | 21 |
| Failed | 19 |
| pass@1 | 52.5% |

## Failed Cases (19)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `kconfig-002` | kconfig | static_analysis | bt_hci_enabled |
| `kconfig-002` | kconfig | static_analysis | kconfig_format, bt_hci_enabled |
| `kconfig-002` | kconfig | static_analysis | bt_hci_enabled |
| `kconfig-002` | kconfig | static_analysis | bt_hci_enabled |
| `kconfig-002` | kconfig | static_analysis | bt_hci_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | usb_device_stack_enabled |
| `kconfig-003` | kconfig | static_analysis | usb_device_stack_enabled |
| `kconfig-003` | kconfig | static_analysis | usb_device_stack_enabled |
| `kconfig-004` | kconfig | static_analysis | log_buffer_size_set |
| `kconfig-004` | kconfig | static_analysis | log_mode_deferred_enabled |
| `kconfig-004` | kconfig | static_analysis | log_mode_deferred_enabled |
| `kconfig-004` | kconfig | static_analysis | log_buffer_size_set |
| `kconfig-004` | kconfig | static_analysis | log_mode_deferred_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_sockopt_tls_enabled, tls_credentials_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_enabled, net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_enabled, net_sockets_sockopt_tls_enabled, tls_credentials_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_sockopt_tls_enabled, tls_credentials_enabled |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `bt_hci_enabled` | 5 | kconfig-002, kconfig-002, kconfig-002, kconfig-002, kconfig-002 |
| `net_sockets_sockopt_tls_enabled` | 5 | kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `networking_enabled` | 4 | kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `mbedtls_builtin_enabled` | 4 | kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `usb_device_stack_enabled` | 3 | kconfig-003, kconfig-003, kconfig-003 |
| `log_mode_deferred_enabled` | 3 | kconfig-004, kconfig-004, kconfig-004 |
| `tls_credentials_enabled` | 3 | kconfig-005, kconfig-005, kconfig-005 |
| `log_buffer_size_set` | 2 | kconfig-004, kconfig-004 |
| `net_sockets_enabled` | 2 | kconfig-005, kconfig-005 |
| `kconfig_format` | 1 | kconfig-002 |
| `uart_line_ctrl_enabled` | 1 | kconfig-003 |

## TC Improvement Suggestions

