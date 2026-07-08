# Benchmark Report: openrouter/openai/gpt-oss-120b

**Date:** 2026-07-01 23:42 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/openai/gpt-oss-120b |
| Total Cases | 50 |
| Passed | 20 |
| Failed | 30 |
| pass@1 | 40.0% |

## Failed Cases (30)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `adc-001` | adc | static_analysis | adc_sequence_defined |
| `adc-001` | adc | static_analysis | adc_sequence_defined |
| `adc-001` | adc | static_heuristic | channel_setup_before_read, periodic_sampling_loop |
| `boot-001` | boot | static_analysis | img_manager_enabled |
| `boot-001` | boot | static_analysis | img_manager_enabled |
| `boot-001` | boot | static_analysis | img_manager_enabled |
| `boot-001` | boot | static_analysis | img_manager_enabled |
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `dma-001` | dma | static_analysis | dma_header_included |
| `dma-001` | dma | static_analysis | dma_header_included |
| `dma-001` | dma | static_analysis | dma_header_included |
| `dma-001` | dma | static_analysis | dma_header_included |
| `dma-001` | dma | static_analysis | dma_header_included |
| `isr-concurrency-001` | isr-concurrency | static_analysis | zephyr_headers_included |
| `isr-concurrency-001` | isr-concurrency | static_analysis | no_printk |
| `isr-concurrency-001` | isr-concurrency | static_analysis | no_printk |
| `isr-concurrency-001` | isr-concurrency | static_analysis | no_printk, zephyr_headers_included |
| `isr-concurrency-001` | isr-concurrency | static_analysis | zephyr_headers_included |
| `memory-opt-001` | memory-opt | compile_gate | west_build |
| `memory-opt-001` | memory-opt | compile_gate | west_build |
| `memory-opt-001` | memory-opt | compile_gate | west_build |
| `memory-opt-001` | memory-opt | compile_gate | west_build |
| `memory-opt-001` | memory-opt | compile_gate | west_build |
| `spi-i2c-001` | spi-i2c | static_heuristic | i2c_error_handling |
| `spi-i2c-001` | spi-i2c | static_heuristic | i2c_error_handling |
| `spi-i2c-001` | spi-i2c | static_heuristic | i2c_error_handling |
| `storage-006` | storage | compile_gate | west_build |
| `storage-006` | storage | static_heuristic | flash_erase_return_checked |
| `storage-006` | storage | compile_gate | west_build |
| `storage-006` | storage | compile_gate | west_build |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `west_build` | 8 | memory-opt-001, memory-opt-001, memory-opt-001, memory-opt-001, memory-opt-001 (+3 more) |
| `dma_header_included` | 5 | dma-001, dma-001, dma-001, dma-001, dma-001 |
| `img_manager_enabled` | 4 | boot-001, boot-001, boot-001, boot-001 |
| `zephyr_headers_included` | 3 | isr-concurrency-001, isr-concurrency-001, isr-concurrency-001 |
| `no_printk` | 3 | isr-concurrency-001, isr-concurrency-001, isr-concurrency-001 |
| `i2c_error_handling` | 3 | spi-i2c-001, spi-i2c-001, spi-i2c-001 |
| `adc_sequence_defined` | 2 | adc-001, adc-001 |
| `channel_setup_before_read` | 1 | adc-001 |
| `periodic_sampling_loop` | 1 | adc-001 |
| `gpio_active_low` | 1 | device-tree-001 |
| `flash_erase_return_checked` | 1 | storage-006 |

## TC Improvement Suggestions

