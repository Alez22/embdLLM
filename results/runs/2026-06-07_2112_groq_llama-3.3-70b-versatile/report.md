# Benchmark Report: groq/llama-3.3-70b-versatile

**Date:** 2026-06-07 21:12 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/llama-3.3-70b-versatile |
| Total Cases | 40 |
| Passed | 26 |
| Failed | 14 |
| pass@1 | 65.0% |

## Failed Cases (14)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-004` | device-tree | static_heuristic | can0_node_present |
| `device-tree-005` | device-tree | static_heuristic | two_gpio_pins_configured |
| `device-tree-005` | device-tree | static_heuristic | two_gpio_pins_configured |
| `device-tree-006` | device-tree | static_analysis | no_fake_pinctrl_properties |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `gpio_active_low` | 5 | device-tree-001, device-tree-001, device-tree-001, device-tree-001, device-tree-001 |
| `pwm_polarity_specified` | 5 | device-tree-003, device-tree-003, device-tree-003, device-tree-003, device-tree-003 |
| `two_gpio_pins_configured` | 2 | device-tree-005, device-tree-005 |
| `can0_node_present` | 1 | device-tree-004 |
| `no_fake_pinctrl_properties` | 1 | device-tree-006 |

## TC Improvement Suggestions

