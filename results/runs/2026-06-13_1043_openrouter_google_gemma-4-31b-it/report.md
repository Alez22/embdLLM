# Benchmark Report: openrouter/google/gemma-4-31b-it

**Date:** 2026-06-13 10:43 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/google/gemma-4-31b-it |
| Total Cases | 40 |
| Passed | 30 |
| Failed | 10 |
| pass@1 | 75.0% |

## Failed Cases (10)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-003` | device-tree | static_heuristic | period_20ms, pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | period_20ms |
| `device-tree-003` | device-tree | static_heuristic | period_20ms |
| `device-tree-003` | device-tree | static_analysis | label_property_present |
| `device-tree-003` | device-tree | static_heuristic | period_20ms |
| `device-tree-006` | device-tree | static_analysis | no_fake_pinctrl_properties |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `interrupt_gpio_present` | 4 | device-tree-001, device-tree-001, device-tree-001, device-tree-001 |
| `period_20ms` | 4 | device-tree-003, device-tree-003, device-tree-003, device-tree-003 |
| `pwm_polarity_specified` | 1 | device-tree-003 |
| `label_property_present` | 1 | device-tree-003 |
| `no_fake_pinctrl_properties` | 1 | device-tree-006 |

## TC Improvement Suggestions

