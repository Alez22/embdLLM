# Benchmark Report: openrouter/qwen/qwen3-235b-a22b-2507

**Date:** 2026-07-01 23:32 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/qwen/qwen3-235b-a22b-2507 |
| Total Cases | 50 |
| Passed | 22 |
| Failed | 28 |
| pass@1 | 44.0% |

## Failed Cases (28)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `boot-001` | boot | static_heuristic | img_manager_dependency |
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `dma-001` | dma | static_analysis | dma_config_called |
| `dma-001` | dma | static_analysis | dma_config_called |
| `dma-001` | dma | static_analysis | dma_config_called |
| `dma-001` | dma | static_analysis | dma_config_called |
| `dma-001` | dma | static_analysis | llm_call |
| `gpio-basic-001` | gpio-basic | static_analysis | uses_dt_spec |
| `isr-concurrency-001` | isr-concurrency | static_analysis | no_printk |
| `isr-concurrency-001` | isr-concurrency | static_analysis | no_printk |
| `isr-concurrency-001` | isr-concurrency | static_analysis | no_printk |
| `isr-concurrency-001` | isr-concurrency | static_analysis | no_printk |
| `isr-concurrency-001` | isr-concurrency | static_analysis | no_printk |
| `memory-opt-001` | memory-opt | static_analysis | mem_slab_defined, slab_alloc_called, slab_free_called |
| `memory-opt-001` | memory-opt | runtime_execution | output_validation |
| `memory-opt-001` | memory-opt | runtime_execution | output_validation |
| `memory-opt-001` | memory-opt | static_analysis | mem_slab_defined, slab_alloc_called, slab_free_called |
| `memory-opt-001` | memory-opt | static_analysis | mem_slab_defined, slab_alloc_called, slab_free_called |
| `spi-i2c-001` | spi-i2c | static_heuristic | i2c_error_handling |
| `spi-i2c-001` | spi-i2c | static_heuristic | i2c_error_handling |
| `spi-i2c-001` | spi-i2c | static_heuristic | i2c_error_handling |
| `spi-i2c-001` | spi-i2c | static_heuristic | i2c_error_handling |
| `storage-006` | storage | compile_gate | west_build |
| `storage-006` | storage | compile_gate | west_build |
| `storage-006` | storage | compile_gate | west_build |
| `storage-006` | storage | compile_gate | west_build |
| `storage-006` | storage | compile_gate | west_build |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `no_printk` | 5 | isr-concurrency-001, isr-concurrency-001, isr-concurrency-001, isr-concurrency-001, isr-concurrency-001 |
| `west_build` | 5 | storage-006, storage-006, storage-006, storage-006, storage-006 |
| `dma_config_called` | 4 | dma-001, dma-001, dma-001, dma-001 |
| `i2c_error_handling` | 4 | spi-i2c-001, spi-i2c-001, spi-i2c-001, spi-i2c-001 |
| `mem_slab_defined` | 3 | memory-opt-001, memory-opt-001, memory-opt-001 |
| `slab_alloc_called` | 3 | memory-opt-001, memory-opt-001, memory-opt-001 |
| `slab_free_called` | 3 | memory-opt-001, memory-opt-001, memory-opt-001 |
| `gpio_active_low` | 2 | device-tree-001, device-tree-001 |
| `output_validation` | 2 | memory-opt-001, memory-opt-001 |
| `img_manager_dependency` | 1 | boot-001 |
| `llm_call` | 1 | dma-001 |
| `uses_dt_spec` | 1 | gpio-basic-001 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 27 | boot-001, device-tree-001, device-tree-001, dma-001, dma-001 (+22 more) |
| LLM format failure (prose) | 1 | dma-001 |

*Adjusted pass@1 (excluding format failures): 44.9% (22/49)*


## TC Improvement Suggestions

