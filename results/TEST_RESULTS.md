# EmbedEval Test Results

*Last updated: 2026-06-07 21:56 UTC*

## Summary

| Model | Cases | Passed | Failed | pass@1 | Retest |
|-------|-------|--------|--------|--------|--------|
| groq/llama-3.3-70b-versatile | 18 | 8 | 10 | 44.4% | - |
| groq/meta-llama/llama-4-scout-17b-16e-instruct | 18 | 8 | 10 | 44.4% | - |
| groq/openai/gpt-oss-120b | 18 | 15 | 3 | 83.3% | - |
| groq/openai/gpt-oss-20b | 18 | 12 | 6 | 66.7% | - |
| groq/qwen/qwen3-32b | 18 | 9 | 9 | 50.0% | - |
| openrouter/mistralai/mistral-small-3.2-24b-instruct | 8 | 1 | 7 | 12.5% | - |
| openrouter/qwen/qwen3-30b-a3b | 8 | 0 | 8 | 0.0% | - |

## groq/llama-3.3-70b-versatile

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| adc | 2 | 0 | 0% | uses_adc_dt_spec, sample_buffer_nonzero |
| device-tree | 8 | 5 | 62% | gpio_active_low, pwm_polarity_specified, can0_node_present |
| kconfig | 8 | 3 | 38% | spi_dma_enabled, kconfig_format, bt_mesh_enabled, uart_line_ctrl_enabled, log_buffer_size_set (+2) |

### Failed Cases (10)

| Case | Layer | Failed Checks | Tested |
|------|-------|---------------|--------|
| adc-001 | L0 | uses_adc_dt_spec | 2026-06-07 |
| adc-002 | L3 | sample_buffer_nonzero | 2026-06-07 |
| device-tree-001 | L3 | gpio_active_low | 2026-06-07 |
| device-tree-003 | L3 | pwm_polarity_specified | 2026-06-07 |
| device-tree-004 | L3 | can0_node_present | 2026-06-07 |
| kconfig-001 | L0 | spi_dma_enabled | 2026-06-07 |
| kconfig-002 | L0 | kconfig_format, bt_mesh_enabled | 2026-06-07 |
| kconfig-003 | L0 | uart_line_ctrl_enabled | 2026-06-07 |
| kconfig-004 | L0 | log_buffer_size_set | 2026-06-07 |
| kconfig-005 | L0 | net_sockets_sockopt_tls_enabled, tls_credentials_enabled | 2026-06-07 |

## groq/meta-llama/llama-4-scout-17b-16e-instruct

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| adc | 2 | 0 | 0% | uses_adc_dt_spec, sample_buffer_nonzero |
| device-tree | 8 | 4 | 50% | interrupt_gpio_present, pwm_polarity_specified, can0_node_present, i2c0_enabled, spi0_enabled (+1) |
| kconfig | 8 | 4 | 50% | bt_hci_enabled, usb_device_stack_enabled, log_mode_deferred_enabled, networking_enabled, net_sockets_sockopt_tls_enabled (+1) |

### Failed Cases (10)

| Case | Layer | Failed Checks | Tested |
|------|-------|---------------|--------|
| adc-001 | L0 | uses_adc_dt_spec | 2026-06-07 |
| adc-002 | L3 | sample_buffer_nonzero | 2026-06-07 |
| device-tree-001 | L3 | interrupt_gpio_present | 2026-06-07 |
| device-tree-003 | L3 | pwm_polarity_specified | 2026-06-07 |
| device-tree-004 | L3 | can0_node_present | 2026-06-07 |
| device-tree-005 | L3 | i2c0_enabled, spi0_enabled, two_gpio_pins_configured | 2026-06-07 |
| kconfig-002 | L0 | bt_hci_enabled | 2026-06-07 |
| kconfig-003 | L0 | usb_device_stack_enabled | 2026-06-07 |
| kconfig-004 | L0 | log_mode_deferred_enabled | 2026-06-07 |
| kconfig-005 | L0 | networking_enabled, net_sockets_sockopt_tls_enabled, tls_credentials_enabled | 2026-06-07 |

## groq/openai/gpt-oss-120b

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| adc | 2 | 2 | 100% | - |
| device-tree | 8 | 7 | 88% | pwm_polarity_specified |
| kconfig | 8 | 6 | 75% | all_required_configs_enabled, net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled |

### Failed Cases (3)

| Case | Layer | Failed Checks | Tested |
|------|-------|---------------|--------|
| device-tree-003 | L3 | pwm_polarity_specified | 2026-06-07 |
| kconfig-002 | L3 | all_required_configs_enabled | 2026-06-07 |
| kconfig-005 | L0 | net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled | 2026-06-07 |

## groq/openai/gpt-oss-20b

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| adc | 2 | 1 | 50% | device_ready_check |
| device-tree | 8 | 6 | 75% | pwm_polarity_specified, i2c0_enabled, spi0_enabled |
| kconfig | 8 | 5 | 62% | uart_line_ctrl_enabled, log_mode_deferred_enabled, networking_enabled, net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled |

### Failed Cases (6)

| Case | Layer | Failed Checks | Tested |
|------|-------|---------------|--------|
| adc-001 | L3 | device_ready_check | 2026-06-07 |
| device-tree-003 | L3 | pwm_polarity_specified | 2026-06-07 |
| device-tree-005 | L3 | i2c0_enabled, spi0_enabled | 2026-06-07 |
| kconfig-003 | L0 | uart_line_ctrl_enabled | 2026-06-07 |
| kconfig-004 | L0 | log_mode_deferred_enabled | 2026-06-07 |
| kconfig-005 | L0 | networking_enabled, net_sockets_sockopt_tls_enabled, mbedtls_builtin_enabled | 2026-06-07 |

## groq/qwen/qwen3-32b

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| adc | 2 | 0 | 0% | code_extracted, code_extracted |
| device-tree | 8 | 4 | 50% | code_extracted, code_extracted, code_extracted, code_extracted |
| kconfig | 8 | 5 | 62% | spi_dma_enabled, code_extracted, kconfig_format, net_sockets_sockopt_tls_enabled, tls_credentials_enabled |

### Failed Cases (9)

| Case | Layer | Failed Checks | Tested |
|------|-------|---------------|--------|
| adc-001 | L0 | code_extracted | 2026-06-07 |
| adc-002 | L0 | code_extracted | 2026-06-07 |
| device-tree-001 | L0 | code_extracted | 2026-06-07 |
| device-tree-003 | L0 | code_extracted | 2026-06-07 |
| device-tree-005 | L0 | code_extracted | 2026-06-07 |
| device-tree-006 | L0 | code_extracted | 2026-06-07 |
| kconfig-001 | L0 | spi_dma_enabled | 2026-06-07 |
| kconfig-003 | L0 | code_extracted | 2026-06-07 |
| kconfig-005 | L0 | kconfig_format, net_sockets_sockopt_tls_enabled, tls_credentials_enabled, mbedtls_enabled (+1) | 2026-06-07 |

## openrouter/mistralai/mistral-small-3.2-24b-instruct

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| kconfig | 8 | 1 | 12% | kconfig_format, bt_mesh_enabled, bt_mesh_relay_enabled, uart_line_ctrl_enabled, log_backend_uart_enabled (+5) |

### Failed Cases (7)

| Case | Layer | Failed Checks | Tested |
|------|-------|---------------|--------|
| kconfig-002 | L0 | kconfig_format, bt_mesh_enabled, bt_mesh_relay_enabled | 2026-06-07 |
| kconfig-003 | L0 | uart_line_ctrl_enabled | 2026-06-07 |
| kconfig-004 | L0 | log_backend_uart_enabled, log_mode_deferred_enabled | 2026-06-07 |
| kconfig-005 | L0 | llm_call | 2026-06-07 |
| kconfig-006 | L0 | llm_call | 2026-06-07 |
| kconfig-007 | L0 | llm_call | 2026-06-07 |
| kconfig-008 | L0 | llm_call | 2026-06-07 |

## openrouter/qwen/qwen3-30b-a3b

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| kconfig | 8 | 0 | 0% | llm_call, llm_call, llm_call, llm_call, llm_call (+3) |

### Failed Cases (8)

| Case | Layer | Failed Checks | Tested |
|------|-------|---------------|--------|
| kconfig-001 | L0 | llm_call | 2026-06-07 |
| kconfig-002 | L0 | llm_call | 2026-06-07 |
| kconfig-003 | L0 | llm_call | 2026-06-07 |
| kconfig-004 | L0 | llm_call | 2026-06-07 |
| kconfig-005 | L0 | llm_call | 2026-06-07 |
| kconfig-006 | L0 | llm_call | 2026-06-07 |
| kconfig-007 | L0 | llm_call | 2026-06-07 |
| kconfig-008 | L0 | llm_call | 2026-06-07 |

