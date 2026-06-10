# Benchmark Report: groq/openai/gpt-oss-120b

**Date:** 2026-06-07 20:40 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/openai/gpt-oss-120b |
| Total Cases | 40 |
| Passed | 24 |
| Failed | 16 |
| pass@1 | 60.0% |

## Failed Cases (16)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `kconfig-001` | kconfig | static_heuristic | all_required_configs_enabled |
| `kconfig-002` | kconfig | static_heuristic | all_required_configs_enabled |
| `kconfig-002` | kconfig | static_heuristic | all_required_configs_enabled |
| `kconfig-003` | kconfig | static_analysis | usb_cdc_acm_enabled, uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | usb_cdc_acm_enabled |
| `kconfig-003` | kconfig | static_analysis | usb_cdc_acm_enabled |
| `kconfig-004` | kconfig | static_analysis | log_mode_deferred_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled |
| `kconfig-007` | kconfig | static_heuristic | no_hallucinated_config_options |
| `kconfig-007` | kconfig | static_heuristic | no_hallucinated_config_options |
| `kconfig-007` | kconfig | static_heuristic | no_hallucinated_config_options |
| `kconfig-007` | kconfig | static_heuristic | no_hallucinated_config_options |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `net_sockets_sockopt_tls_enabled` | 5 | kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `no_hallucinated_config_options` | 4 | kconfig-007, kconfig-007, kconfig-007, kconfig-007 |
| `all_required_configs_enabled` | 3 | kconfig-001, kconfig-002, kconfig-002 |
| `usb_cdc_acm_enabled` | 3 | kconfig-003, kconfig-003, kconfig-003 |
| `mbedtls_builtin_enabled` | 3 | kconfig-005, kconfig-005, kconfig-005 |
| `uart_line_ctrl_enabled` | 1 | kconfig-003 |
| `log_mode_deferred_enabled` | 1 | kconfig-004 |

## TC Improvement Suggestions

