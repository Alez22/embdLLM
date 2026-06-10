# Benchmark Report: groq/openai/gpt-oss-20b

**Date:** 2026-06-07 21:50 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/openai/gpt-oss-20b |
| Total Cases | 40 |
| Passed | 21 |
| Failed | 19 |
| pass@1 | 52.5% |

## Failed Cases (19)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `device-tree-001` | device-tree | static_heuristic | gpio_active_low, node_at_address_format |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-002` | device-tree | static_heuristic | spi0_parent_enabled |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-004` | device-tree | static_heuristic | can0_node_present |
| `device-tree-004` | device-tree | static_heuristic | can0_node_present |
| `device-tree-004` | device-tree | static_heuristic | can0_node_present |
| `device-tree-005` | device-tree | static_analysis | code_extracted |
| `device-tree-005` | device-tree | static_analysis | code_extracted |
| `device-tree-005` | device-tree | static_heuristic | two_gpio_pins_configured |
| `device-tree-005` | device-tree | static_analysis | code_extracted |
| `device-tree-005` | device-tree | static_heuristic | i2c0_enabled, spi0_enabled |
| `device-tree-006` | device-tree | static_analysis | code_extracted |
| `device-tree-006` | device-tree | static_analysis | code_extracted |
| `device-tree-006` | device-tree | static_analysis | code_extracted |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `code_extracted` | 6 | device-tree-005, device-tree-005, device-tree-005, device-tree-006, device-tree-006 (+1 more) |
| `pwm_polarity_specified` | 5 | device-tree-003, device-tree-003, device-tree-003, device-tree-003, device-tree-003 |
| `can0_node_present` | 3 | device-tree-004, device-tree-004, device-tree-004 |
| `gpio_active_low` | 1 | device-tree-001 |
| `node_at_address_format` | 1 | device-tree-001 |
| `interrupt_gpio_present` | 1 | device-tree-001 |
| `spi0_parent_enabled` | 1 | device-tree-002 |
| `two_gpio_pins_configured` | 1 | device-tree-005 |
| `i2c0_enabled` | 1 | device-tree-005 |
| `spi0_enabled` | 1 | device-tree-005 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 12 | device-tree-001, device-tree-001, device-tree-002, device-tree-003, device-tree-003 (+7 more) |
| LLM format failure (prose) | 7 | device-tree-003, device-tree-005, device-tree-005, device-tree-005, device-tree-006, device-tree-006, device-tree-006 |

*Adjusted pass@1 (excluding format failures): 63.6% (21/33)*


## TC Improvement Suggestions

