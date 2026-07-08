# Benchmark Report: openrouter/deepseek/deepseek-v4-flash

**Date:** 2026-07-01 23:18 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/deepseek/deepseek-v4-flash |
| Total Cases | 50 |
| Passed | 25 |
| Failed | 25 |
| pass@1 | 50.0% |

## Failed Cases (25)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `boot-001` | boot | static_heuristic | img_manager_dependency |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `dma-001` | dma | compile_gate | west_build |
| `dma-001` | dma | static_analysis | dma_header_included |
| `dma-001` | dma | compile_gate | west_build |
| `dma-001` | dma | compile_gate | west_build |
| `dma-001` | dma | runtime_execution | output_validation |
| `isr-concurrency-001` | isr-concurrency | static_analysis | no_printk |
| `isr-concurrency-001` | isr-concurrency | static_analysis | zephyr_headers_included |
| `isr-concurrency-001` | isr-concurrency | compile_gate | west_build |
| `isr-concurrency-001` | isr-concurrency | compile_gate | west_build |
| `isr-concurrency-001` | isr-concurrency | compile_gate | west_build |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `memory-opt-001` | memory-opt | compile_gate | west_build |
| `memory-opt-001` | memory-opt | static_analysis | mem_slab_defined, slab_alloc_called, slab_free_called |
| `memory-opt-001` | memory-opt | compile_gate | west_build |
| `memory-opt-001` | memory-opt | compile_gate | west_build |
| `memory-opt-001` | memory-opt | runtime_execution | output_validation |
| `spi-i2c-001` | spi-i2c | static_heuristic | ready_check_before_io |
| `storage-006` | storage | compile_gate | west_build |
| `storage-006` | storage | compile_gate | west_build |
| `storage-006` | storage | compile_gate | west_build |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `west_build` | 12 | dma-001, dma-001, dma-001, isr-concurrency-001, isr-concurrency-001 (+7 more) |
| `interrupt_gpio_present` | 4 | device-tree-001, device-tree-001, device-tree-001, device-tree-001 |
| `output_validation` | 2 | dma-001, memory-opt-001 |
| `img_manager_dependency` | 1 | boot-001 |
| `dma_header_included` | 1 | dma-001 |
| `no_printk` | 1 | isr-concurrency-001 |
| `zephyr_headers_included` | 1 | isr-concurrency-001 |
| `spi_dma_enabled` | 1 | kconfig-001 |
| `mem_slab_defined` | 1 | memory-opt-001 |
| `slab_alloc_called` | 1 | memory-opt-001 |
| `slab_free_called` | 1 | memory-opt-001 |
| `ready_check_before_io` | 1 | spi-i2c-001 |

## TC Improvement Suggestions

