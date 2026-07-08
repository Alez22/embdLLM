# Benchmark Report: openrouter/qwen/qwen3-235b-a22b

**Date:** 2026-06-13 13:27 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/qwen/qwen3-235b-a22b |
| Total Cases | 40 |
| Passed | 27 |
| Failed | 13 |
| pass@1 | 67.5% |

## Failed Cases (13)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present, gpio_active_low |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present, gpio_active_low |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present, node_at_address_format |
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-004` | device-tree | static_heuristic | can0_node_present, transceiver_nested_in_can0 |
| `device-tree-004` | device-tree | static_heuristic | transceiver_nested_in_can0 |
| `device-tree-007` | device-tree | static_heuristic | peripheral_node_referenced |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `pwm_polarity_specified` | 5 | device-tree-003, device-tree-003, device-tree-003, device-tree-003, device-tree-003 |
| `gpio_active_low` | 4 | device-tree-001, device-tree-001, device-tree-001, device-tree-001 |
| `interrupt_gpio_present` | 3 | device-tree-001, device-tree-001, device-tree-001 |
| `transceiver_nested_in_can0` | 2 | device-tree-004, device-tree-004 |
| `node_at_address_format` | 1 | device-tree-001 |
| `can0_node_present` | 1 | device-tree-004 |
| `peripheral_node_referenced` | 1 | device-tree-007 |

## TC Improvement Suggestions

