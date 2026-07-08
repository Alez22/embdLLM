# Benchmark Report: openrouter/qwen/qwen3-235b-a22b-2507

**Date:** 2026-06-13 12:26 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/qwen/qwen3-235b-a22b-2507 |
| Total Cases | 40 |
| Passed | 30 |
| Failed | 10 |
| pass@1 | 75.0% |

## Failed Cases (10)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `device-tree-003` | device-tree | static_analysis | pwms_property_present |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-005` | device-tree | static_heuristic | two_gpio_pins_configured |
| `device-tree-005` | device-tree | static_heuristic | two_gpio_pins_configured |
| `device-tree-005` | device-tree | static_heuristic | two_gpio_pins_configured |
| `device-tree-005` | device-tree | static_heuristic | two_gpio_pins_configured |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `two_gpio_pins_configured` | 4 | device-tree-005, device-tree-005, device-tree-005, device-tree-005 |
| `pwm_polarity_specified` | 3 | device-tree-003, device-tree-003, device-tree-003 |
| `gpio_active_low` | 2 | device-tree-001, device-tree-001 |
| `pwms_property_present` | 1 | device-tree-003 |

## TC Improvement Suggestions

