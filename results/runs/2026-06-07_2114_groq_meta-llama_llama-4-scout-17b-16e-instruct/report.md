# Benchmark Report: groq/meta-llama/llama-4-scout-17b-16e-instruct

**Date:** 2026-06-07 21:14 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/meta-llama/llama-4-scout-17b-16e-instruct |
| Total Cases | 40 |
| Passed | 23 |
| Failed | 17 |
| pass@1 | 57.5% |

## Failed Cases (17)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-004` | device-tree | static_heuristic | can0_node_present |
| `device-tree-004` | device-tree | static_heuristic | can0_node_present |
| `device-tree-005` | device-tree | static_heuristic | i2c0_enabled, spi0_enabled |
| `device-tree-005` | device-tree | static_heuristic | i2c0_enabled, spi0_enabled, two_gpio_pins_configured |
| `device-tree-005` | device-tree | static_heuristic | i2c0_enabled, spi0_enabled |
| `device-tree-005` | device-tree | static_heuristic | i2c0_enabled, spi0_enabled |
| `device-tree-005` | device-tree | static_heuristic | i2c0_enabled, spi0_enabled, two_gpio_pins_configured |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `pwm_polarity_specified` | 5 | device-tree-003, device-tree-003, device-tree-003, device-tree-003, device-tree-003 |
| `i2c0_enabled` | 5 | device-tree-005, device-tree-005, device-tree-005, device-tree-005, device-tree-005 |
| `spi0_enabled` | 5 | device-tree-005, device-tree-005, device-tree-005, device-tree-005, device-tree-005 |
| `interrupt_gpio_present` | 3 | device-tree-001, device-tree-001, device-tree-001 |
| `gpio_active_low` | 2 | device-tree-001, device-tree-001 |
| `can0_node_present` | 2 | device-tree-004, device-tree-004 |
| `two_gpio_pins_configured` | 2 | device-tree-005, device-tree-005 |

## TC Improvement Suggestions

