# Benchmark Report: openrouter/google/gemma-4-31b-it

**Date:** 2026-07-01 23:15 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/google/gemma-4-31b-it |
| Total Cases | 50 |
| Passed | 21 |
| Failed | 29 |
| pass@1 | 42.0% |

## Failed Cases (29)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `boot-001` | boot | static_analysis | mcuboot_enabled |
| `boot-001` | boot | static_analysis | img_manager_enabled |
| `boot-001` | boot | static_analysis | img_manager_enabled |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `dma-001` | dma | static_analysis | dma_header_included, dma_block_config_struct |
| `dma-001` | dma | static_analysis | dma_block_config_struct |
| `dma-001` | dma | compile_gate | west_build |
| `dma-001` | dma | static_analysis | dma_block_config_struct |
| `dma-001` | dma | compile_gate | west_build |
| `isr-concurrency-001` | isr-concurrency | static_analysis | no_printk, uses_atomic_operations, zephyr_headers_included |
| `isr-concurrency-001` | isr-concurrency | static_analysis | uses_atomic_operations, zephyr_headers_included |
| `isr-concurrency-001` | isr-concurrency | static_analysis | no_printk |
| `isr-concurrency-001` | isr-concurrency | static_analysis | uses_atomic_operations, zephyr_headers_included |
| `isr-concurrency-001` | isr-concurrency | static_analysis | no_printk, uses_atomic_operations |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `memory-opt-001` | memory-opt | compile_gate | west_build |
| `memory-opt-001` | memory-opt | compile_gate | west_build |
| `memory-opt-001` | memory-opt | compile_gate | west_build |
| `memory-opt-001` | memory-opt | compile_gate | west_build |
| `memory-opt-001` | memory-opt | compile_gate | west_build |
| `storage-006` | storage | static_heuristic | success_printed |
| `storage-006` | storage | compile_gate | west_build |
| `storage-006` | storage | compile_gate | west_build |
| `storage-006` | storage | static_heuristic | success_printed |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `west_build` | 9 | dma-001, dma-001, memory-opt-001, memory-opt-001, memory-opt-001 (+4 more) |
| `interrupt_gpio_present` | 4 | device-tree-001, device-tree-001, device-tree-001, device-tree-001 |
| `uses_atomic_operations` | 4 | isr-concurrency-001, isr-concurrency-001, isr-concurrency-001, isr-concurrency-001 |
| `dma_block_config_struct` | 3 | dma-001, dma-001, dma-001 |
| `no_printk` | 3 | isr-concurrency-001, isr-concurrency-001, isr-concurrency-001 |
| `zephyr_headers_included` | 3 | isr-concurrency-001, isr-concurrency-001, isr-concurrency-001 |
| `spi_dma_enabled` | 3 | kconfig-001, kconfig-001, kconfig-001 |
| `img_manager_enabled` | 2 | boot-001, boot-001 |
| `success_printed` | 2 | storage-006, storage-006 |
| `mcuboot_enabled` | 1 | boot-001 |
| `dma_header_included` | 1 | dma-001 |

## TC Improvement Suggestions

