# Benchmark Report: groq/openai/gpt-oss-20b

**Date:** 2026-06-07 20:37 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/openai/gpt-oss-20b |
| Total Cases | 40 |
| Passed | 24 |
| Failed | 16 |
| pass@1 | 60.0% |

## Failed Cases (16)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `kconfig-002` | kconfig | static_analysis | bt_hci_enabled |
| `kconfig-002` | kconfig | static_analysis | bt_hci_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | usb_cdc_acm_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-004` | kconfig | static_analysis | log_mode_deferred_enabled, log_buffer_size_set |
| `kconfig-004` | kconfig | static_analysis | log_buffer_size_set |
| `kconfig-004` | kconfig | static_analysis | log_mode_deferred_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_enabled, net_sockets_sockopt_tls_enabled, mbedtls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_sockopt_tls_enabled, mbedtls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_sockopt_tls_enabled, mbedtls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | networking_enabled, net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled |
| `kconfig-008` | kconfig | static_analysis | kconfig_format, userspace_enabled, mpu_enabled, arm_mpu_enabled, memory_sizing_configured |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `networking_enabled` | 5 | kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `net_sockets_sockopt_tls_enabled` | 5 | kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `mbedtls_builtin_enabled` | 5 | kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `uart_line_ctrl_enabled` | 4 | kconfig-003, kconfig-003, kconfig-003, kconfig-003 |
| `mbedtls_enabled` | 3 | kconfig-005, kconfig-005, kconfig-005 |
| `bt_hci_enabled` | 2 | kconfig-002, kconfig-002 |
| `log_mode_deferred_enabled` | 2 | kconfig-004, kconfig-004 |
| `log_buffer_size_set` | 2 | kconfig-004, kconfig-004 |
| `usb_cdc_acm_enabled` | 1 | kconfig-003 |
| `net_sockets_enabled` | 1 | kconfig-005 |
| `kconfig_format` | 1 | kconfig-008 |
| `userspace_enabled` | 1 | kconfig-008 |
| `mpu_enabled` | 1 | kconfig-008 |
| `arm_mpu_enabled` | 1 | kconfig-008 |
| `memory_sizing_configured` | 1 | kconfig-008 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 15 | kconfig-002, kconfig-002, kconfig-003, kconfig-003, kconfig-003 (+10 more) |
| LLM format failure (prose) | 1 | kconfig-008 |

*Adjusted pass@1 (excluding format failures): 61.5% (24/39)*


## TC Improvement Suggestions

