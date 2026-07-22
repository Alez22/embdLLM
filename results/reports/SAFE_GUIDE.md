# EmbedEval Safe Guide for Embedded Engineers

*Auto-generated from benchmark results. Use this to decide when LLM-generated code needs human review.*

**Last updated:** 2026-07-02 00:21 UTC

## Models Tested

| Model | pass@1 | Cases |
|-------|--------|-------|
| groq/llama-3.3-70b-versatile | 50.0% | 18 |
| groq/meta-llama/llama-4-scout-17b-16e-instruct | 50.0% | 18 |
| groq/openai/gpt-oss-120b | 83.3% | 18 |
| groq/openai/gpt-oss-20b | 66.7% | 18 |
| groq/qwen/qwen3-32b | 50.0% | 18 |
| mock | 0.0% | 1 |
| openrouter/anthropic/claude-opus-4.8 | 66.7% | 6 |
| openrouter/anthropic/claude-sonnet-4.6 | 0.0% | 24 |
| openrouter/deepseek/deepseek-v4-flash | 70.0% | 10 |
| openrouter/deepseek/deepseek-v4-pro | 4.2% | 24 |
| openrouter/google/gemma-4-31b-it | 70.0% | 10 |
| openrouter/meta-llama/llama-4-maverick | 0.0% | 2 |
| openrouter/mistralai/mistral-small-3.2-24b-instruct | 25.0% | 8 |
| openrouter/openai/gpt-oss-120b | 70.0% | 10 |
| openrouter/qwen/qwen3-235b-a22b | 75.0% | 8 |
| openrouter/qwen/qwen3-235b-a22b-2507 | 63.6% | 11 |
| openrouter/qwen/qwen3-30b-a3b | 0.0% | 8 |
| openrouter/z-ai/glm-4.7-flash | 75.0% | 8 |
| openrouter/z-ai/glm-5.2 | 12.5% | 24 |

## CRITICAL — Do Not Trust

*LLM fails >50% of the time. Always write this code manually or review every line.*

| Category | groq/llama-3.3-70b-versatile | groq/meta-llama/llama-4-scout-17b-16e-instruct | groq/openai/gpt-oss-120b | groq/openai/gpt-oss-20b | groq/qwen/qwen3-32b | mock | openrouter/anthropic/claude-opus-4.8 | openrouter/anthropic/claude-sonnet-4.6 | openrouter/deepseek/deepseek-v4-flash | openrouter/deepseek/deepseek-v4-pro | openrouter/google/gemma-4-31b-it | openrouter/meta-llama/llama-4-maverick | openrouter/mistralai/mistral-small-3.2-24b-instruct | openrouter/openai/gpt-oss-120b | openrouter/qwen/qwen3-235b-a22b | openrouter/qwen/qwen3-235b-a22b-2507 | openrouter/qwen/qwen3-30b-a3b | openrouter/z-ai/glm-4.7-flash | openrouter/z-ai/glm-5.2 |
|----------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| adc | 0% | 0% | 100% | 50% | 0% | - | - | - | 100% | - | 100% | 0% | - | 100% | - | 100% | - | - | - |
| audio | - | - | - | - | - | - | - | 0% | - | 0% | - | - | - | - | - | - | - | - | 0% |
| dma | - | - | - | - | - | - | - | 0% | 0% | 0% | 0% | - | - | 0% | - | 0% | - | - | 0% |
| gpio-basic | - | - | - | - | - | 0% | 100% | 0% | 100% | 0% | 100% | - | - | 100% | - | 100% | - | - | 25% |
| isr-concurrency | - | - | - | - | - | - | - | 0% | 0% | 50% | 0% | - | - | 0% | - | 0% | - | - | 50% |
| kconfig | 38% | 50% | 75% | 62% | 62% | - | - | - | 100% | - | 100% | - | 25% | 100% | - | 100% | 0% | 75% | - |
| memory-opt | - | - | - | - | - | - | - | - | 0% | - | 0% | - | - | 0% | - | 0% | - | - | - |
| spi-i2c | - | - | - | - | - | - | 100% | 0% | 100% | 0% | 100% | - | - | 100% | - | 100% | - | - | 0% |
| storage | - | - | - | - | - | - | 0% | 0% | 100% | 0% | 100% | - | - | 100% | - | 0% | - | - | 0% |
| timer | - | - | - | - | - | - | - | 0% | - | 0% | - | - | - | - | - | - | - | - | 50% |
| uart | - | - | - | - | - | - | - | 0% | - | 0% | - | - | - | - | - | - | - | - | 0% |
| watchdog | - | - | - | - | - | - | - | 0% | - | 0% | - | - | - | - | - | - | - | - | 0% |

## CAUTION — Always Review

*LLM fails 20-50%. Use as starting point only. Expert review mandatory.*

| Category | groq/llama-3.3-70b-versatile | groq/meta-llama/llama-4-scout-17b-16e-instruct | groq/openai/gpt-oss-120b | groq/openai/gpt-oss-20b | groq/qwen/qwen3-32b | mock | openrouter/anthropic/claude-opus-4.8 | openrouter/anthropic/claude-sonnet-4.6 | openrouter/deepseek/deepseek-v4-flash | openrouter/deepseek/deepseek-v4-pro | openrouter/google/gemma-4-31b-it | openrouter/meta-llama/llama-4-maverick | openrouter/mistralai/mistral-small-3.2-24b-instruct | openrouter/openai/gpt-oss-120b | openrouter/qwen/qwen3-235b-a22b | openrouter/qwen/qwen3-235b-a22b-2507 | openrouter/qwen/qwen3-30b-a3b | openrouter/z-ai/glm-4.7-flash | openrouter/z-ai/glm-5.2 |
|----------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| device-tree | 75% | 62% | 88% | 75% | 50% | - | - | - | 100% | - | 100% | - | - | 100% | 75% | 100% | - | - | - |

## RELIABLE — Generally Safe

*LLM passes 90%+. Standard code review is sufficient.*

| Category | groq/llama-3.3-70b-versatile | groq/meta-llama/llama-4-scout-17b-16e-instruct | groq/openai/gpt-oss-120b | groq/openai/gpt-oss-20b | groq/qwen/qwen3-32b | mock | openrouter/anthropic/claude-opus-4.8 | openrouter/anthropic/claude-sonnet-4.6 | openrouter/deepseek/deepseek-v4-flash | openrouter/deepseek/deepseek-v4-pro | openrouter/google/gemma-4-31b-it | openrouter/meta-llama/llama-4-maverick | openrouter/mistralai/mistral-small-3.2-24b-instruct | openrouter/openai/gpt-oss-120b | openrouter/qwen/qwen3-235b-a22b | openrouter/qwen/qwen3-235b-a22b-2507 | openrouter/qwen/qwen3-30b-a3b | openrouter/z-ai/glm-4.7-flash | openrouter/z-ai/glm-5.2 |
|----------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| boot | - | - | - | - | - | - | - | - | 100% | - | 100% | - | - | 100% | - | 100% | - | - | - |

## Most Common Failure Patterns

*These checks fail most often across all models and runs. Pay special attention to these patterns in LLM-generated code.*

| Pattern | Failures | What to Check |
|---------|----------|---------------|
| `nxp_gcc` | 528 | Review LLM output against hardware/RTOS requirements |
| `llm_call` | 358 | Review LLM output against hardware/RTOS requirements |
| `header_fsl_clock_h` | 150 | Review LLM output against hardware/RTOS requirements |
| `clock_root_configured` | 113 | Review LLM output against hardware/RTOS requirements |
| `header_fsl_port_h` | 109 | Review LLM output against hardware/RTOS requirements |
| `interrupt_flag_cleared` | 86 | Review LLM output against hardware/RTOS requirements |
| `flash_verify_program_called` | 79 | Review LLM output against hardware/RTOS requirements |
| `header_fsl_iomuxc_h` | 75 | Review LLM output against hardware/RTOS requirements |
| `sai_write_api_used` | 72 | Review LLM output against hardware/RTOS requirements |
| `read_and_write_api_used` | 70 | Review LLM output against hardware/RTOS requirements |
| `net_sockets_sockopt_tls_enabled` | 58 | Review LLM output against hardware/RTOS requirements |
| `pit_isr_defined` | 55 | Review LLM output against hardware/RTOS requirements |
| `long_timeout_configured` | 50 | Review LLM output against hardware/RTOS requirements |
| `mbedtls_builtin_enabled` | 49 | Review LLM output against hardware/RTOS requirements |
| `sai_init_called` | 48 | Review LLM output against hardware/RTOS requirements |
| `init_status_checked` | 48 | Review LLM output against hardware/RTOS requirements |
| `uart_isr_handler_defined` | 47 | Review LLM output against hardware/RTOS requirements |
| `code_extracted` | 47 | Review LLM output against hardware/RTOS requirements |
| `isr_handler_defined` | 47 | Review LLM output against hardware/RTOS requirements |
| `bit_clock_rate_set` | 46 | Review LLM output against hardware/RTOS requirements |

## Practical Recommendations

### When using LLM for embedded code:

1. **Always review** volatile qualifiers, memory barriers, and ISR-safe patterns
2. **Never trust** DMA configuration, memory domain setup, or lock ordering without verification
3. **Verify** error handling paths — LLMs often generate happy-path-only code
4. **Check** that Kconfig/prj.conf options match the APIs used in the code
5. **Test** on actual hardware or QEMU — static checks alone miss runtime issues

