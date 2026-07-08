# Benchmark Report: openrouter/z-ai/glm-5.2

**Date:** 2026-07-02 00:10 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/z-ai/glm-5.2 |
| Total Cases | 67 |
| Passed | 22 |
| Failed | 45 |
| pass@1 | 32.8% |

## Failed Cases (45)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `boot-001` | boot | static_analysis | img_manager_enabled |
| `boot-001` | boot | static_analysis | img_manager_enabled |
| `boot-001` | boot | static_heuristic | img_manager_dependency |
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `dma-001` | dma | runtime_execution | output_validation |
| `dma-001` | dma | compile_gate | west_build |
| `dma-001` | dma | compile_gate | west_build |
| `dma-001` | dma | runtime_execution | output_validation |
| `dma-001` | dma | static_heuristic | separate_src_dst_buffers |
| `isr-concurrency-001` | isr-concurrency | static_analysis | uses_atomic_operations |
| `isr-concurrency-001` | isr-concurrency | static_analysis | uses_atomic_operations |
| `isr-concurrency-001` | isr-concurrency | compile_gate | west_build |
| `isr-concurrency-001` | isr-concurrency | compile_gate | west_build |
| `isr-concurrency-001` | isr-concurrency | compile_gate | west_build |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `memory-opt-001` | memory-opt | runtime_execution | output_validation |
| `memory-opt-001` | memory-opt | runtime_execution | output_validation |
| `memory-opt-001` | memory-opt | runtime_execution | output_validation |
| `memory-opt-001` | memory-opt | runtime_execution | output_validation |
| `memory-opt-001` | memory-opt | compile_gate | west_build |
| `nxp-mcxc-flash-001` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-flash-002` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-mcxc-i2c-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-i2c-002` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-isr-001` | isr-concurrency | static_analysis | pit_isr_defined |
| `nxp-mcxc-spi-001` | spi-i2c | compile_gate | nxp_gcc |
| `nxp-mcxc-timer-001` | timer | static_analysis | pit_isr_defined |
| `nxp-mcxc-uart-001` | uart | compile_gate | nxp_gcc |
| `nxp-mcxc-uart-002` | uart | static_analysis | uart_isr_handler_defined |
| `nxp-mcxc-watchdog-001` | watchdog | compile_gate | nxp_gcc |
| `nxp-rt1170-audio-001` | audio | compile_gate | nxp_gcc |
| `nxp-rt1170-dma-001` | dma | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-001` | gpio-basic | compile_gate | nxp_gcc |
| `nxp-rt1170-gpio-002` | gpio-basic | static_analysis | interrupt_flag_cleared |
| `nxp-rt1170-gpt-001` | timer | compile_gate | nxp_gcc |
| `storage-006` | storage | compile_gate | west_build |
| `storage-006` | storage | static_heuristic | device_ready_checked |
| `storage-006` | storage | compile_gate | west_build |
| `storage-006` | storage | compile_gate | west_build |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `nxp_gcc` | 11 | nxp-mcxc-flash-001, nxp-mcxc-flash-002, nxp-mcxc-i2c-001, nxp-mcxc-i2c-002, nxp-mcxc-spi-001 (+6 more) |
| `west_build` | 9 | dma-001, dma-001, isr-concurrency-001, isr-concurrency-001, isr-concurrency-001 (+4 more) |
| `output_validation` | 6 | dma-001, dma-001, memory-opt-001, memory-opt-001, memory-opt-001 (+1 more) |
| `spi_dma_enabled` | 4 | kconfig-001, kconfig-001, kconfig-001, kconfig-001 |
| `interrupt_flag_cleared` | 2 | nxp-mcxc-gpio-002, nxp-rt1170-gpio-002 |
| `pit_isr_defined` | 2 | nxp-mcxc-isr-001, nxp-mcxc-timer-001 |
| `img_manager_enabled` | 2 | boot-001, boot-001 |
| `gpio_active_low` | 2 | device-tree-001, device-tree-001 |
| `uses_atomic_operations` | 2 | isr-concurrency-001, isr-concurrency-001 |
| `uart_isr_handler_defined` | 1 | nxp-mcxc-uart-002 |
| `img_manager_dependency` | 1 | boot-001 |
| `interrupt_gpio_present` | 1 | device-tree-001 |
| `separate_src_dst_buffers` | 1 | dma-001 |
| `device_ready_checked` | 1 | storage-006 |

## TC Improvement Suggestions

