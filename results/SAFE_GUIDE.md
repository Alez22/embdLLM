# EmbedEval Safe Guide for Embedded Engineers

*Auto-generated from benchmark results. Use this to decide when LLM-generated code needs human review.*

**Last updated:** 2026-06-07 21:56 UTC

## Models Tested

| Model | pass@1 | Cases |
|-------|--------|-------|
| groq/llama-3.3-70b-versatile | 50.0% | 18 |
| groq/meta-llama/llama-4-scout-17b-16e-instruct | 50.0% | 18 |
| groq/openai/gpt-oss-120b | 83.3% | 18 |
| groq/openai/gpt-oss-20b | 66.7% | 18 |
| groq/qwen/qwen3-32b | 50.0% | 18 |
| openrouter/mistralai/mistral-small-3.2-24b-instruct | 25.0% | 8 |
| openrouter/qwen/qwen3-30b-a3b | 0.0% | 8 |

## CRITICAL — Do Not Trust

*LLM fails >50% of the time. Always write this code manually or review every line.*

| Category | groq/llama-3.3-70b-versatile | groq/meta-llama/llama-4-scout-17b-16e-instruct | groq/openai/gpt-oss-120b | groq/openai/gpt-oss-20b | groq/qwen/qwen3-32b | openrouter/mistralai/mistral-small-3.2-24b-instruct | openrouter/qwen/qwen3-30b-a3b |
|----------|------|------|------|------|------|------|------|
| adc | 0% | 0% | 100% | 50% | 0% | - | - |
| kconfig | 38% | 50% | 75% | 62% | 62% | 25% | 0% |

## CAUTION — Always Review

*LLM fails 20-50%. Use as starting point only. Expert review mandatory.*

| Category | groq/llama-3.3-70b-versatile | groq/meta-llama/llama-4-scout-17b-16e-instruct | groq/openai/gpt-oss-120b | groq/openai/gpt-oss-20b | groq/qwen/qwen3-32b | openrouter/mistralai/mistral-small-3.2-24b-instruct | openrouter/qwen/qwen3-30b-a3b |
|----------|------|------|------|------|------|------|------|
| device-tree | 75% | 62% | 88% | 75% | 50% | - | - |

## Most Common Failure Patterns

*These checks fail most often across all models and runs. Pay special attention to these patterns in LLM-generated code.*

| Pattern | Failures | What to Check |
|---------|----------|---------------|
| `llm_call` | 100 | Review LLM output against hardware/RTOS requirements |
| `code_extracted` | 38 | Review LLM output against hardware/RTOS requirements |
| `net_sockets_sockopt_tls_enabled` | 33 | Review LLM output against hardware/RTOS requirements |
| `mbedtls_builtin_enabled` | 27 | Review LLM output against hardware/RTOS requirements |
| `networking_enabled` | 22 | Review LLM output against hardware/RTOS requirements |
| `kconfig_format` | 21 | Review LLM output against hardware/RTOS requirements |
| `pwm_polarity_specified` | 20 | Review LLM output against hardware/RTOS requirements |
| `bt_hci_enabled` | 19 | Review LLM output against hardware/RTOS requirements |
| `uart_line_ctrl_enabled` | 18 | Review LLM output against hardware/RTOS requirements |
| `log_mode_deferred_enabled` | 18 | Review LLM output against hardware/RTOS requirements |
| `log_buffer_size_set` | 16 | Review LLM output against hardware/RTOS requirements |
| `tls_credentials_enabled` | 16 | Review LLM output against hardware/RTOS requirements |
| `spi_dma_enabled` | 14 | Review LLM output against hardware/RTOS requirements |
| `sample_buffer_nonzero` | 11 | Review LLM output against hardware/RTOS requirements |
| `net_sockets_enabled` | 10 | Review LLM output against hardware/RTOS requirements |
| `log_backend_uart_enabled` | 9 | Review LLM output against hardware/RTOS requirements |
| `mbedtls_enabled` | 9 | Review LLM output against hardware/RTOS requirements |
| `interrupt_gpio_present` | 8 | Review LLM output against hardware/RTOS requirements |
| `gpio_active_low` | 8 | Review LLM output against hardware/RTOS requirements |
| `can0_node_present` | 7 | Review LLM output against hardware/RTOS requirements |

## Practical Recommendations

### When using LLM for embedded code:

1. **Always review** volatile qualifiers, memory barriers, and ISR-safe patterns
2. **Never trust** DMA configuration, memory domain setup, or lock ordering without verification
3. **Verify** error handling paths — LLMs often generate happy-path-only code
4. **Check** that Kconfig/prj.conf options match the APIs used in the code
5. **Test** on actual hardware or QEMU — static checks alone miss runtime issues

