# Benchmark Report: groq/qwen/qwen3-32b

**Date:** 2026-06-07 21:37 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/qwen/qwen3-32b |
| Total Cases | 40 |
| Passed | 14 |
| Failed | 26 |
| pass@1 | 35.0% |

## Failed Cases (26)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_analysis | code_extracted |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_analysis | code_extracted |
| `device-tree-002` | device-tree | static_analysis | code_extracted |
| `device-tree-002` | device-tree | static_heuristic | spi0_parent_enabled |
| `device-tree-003` | device-tree | static_analysis | code_extracted |
| `device-tree-003` | device-tree | static_analysis | pwms_property_present |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_analysis | pwms_property_present |
| `device-tree-003` | device-tree | static_analysis | code_extracted |
| `device-tree-004` | device-tree | static_analysis | code_extracted |
| `device-tree-004` | device-tree | static_heuristic | can0_node_present |
| `device-tree-005` | device-tree | static_analysis | code_extracted |
| `device-tree-005` | device-tree | static_analysis | code_extracted |
| `device-tree-005` | device-tree | static_analysis | code_extracted |
| `device-tree-005` | device-tree | static_analysis | code_extracted |
| `device-tree-005` | device-tree | static_analysis | code_extracted |
| `device-tree-006` | device-tree | static_analysis | code_extracted |
| `device-tree-006` | device-tree | static_analysis | code_extracted |
| `device-tree-006` | device-tree | static_analysis | code_extracted |
| `device-tree-006` | device-tree | static_analysis | code_extracted |
| `device-tree-006` | device-tree | static_analysis | code_extracted |
| `device-tree-007` | device-tree | static_analysis | code_extracted |
| `device-tree-007` | device-tree | static_analysis | code_extracted |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `code_extracted` | 18 | device-tree-001, device-tree-001, device-tree-002, device-tree-003, device-tree-003 (+13 more) |
| `interrupt_gpio_present` | 3 | device-tree-001, device-tree-001, device-tree-001 |
| `pwms_property_present` | 2 | device-tree-003, device-tree-003 |
| `spi0_parent_enabled` | 1 | device-tree-002 |
| `pwm_polarity_specified` | 1 | device-tree-003 |
| `can0_node_present` | 1 | device-tree-004 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 8 | device-tree-001, device-tree-001, device-tree-001, device-tree-002, device-tree-003 (+3 more) |
| LLM format failure (prose) | 18 | device-tree-001, device-tree-001, device-tree-002, device-tree-003, device-tree-003, device-tree-004, device-tree-005, device-tree-005, device-tree-005, device-tree-005, device-tree-005, device-tree-006, device-tree-006, device-tree-006, device-tree-006, device-tree-006, device-tree-007, device-tree-007 |

*Adjusted pass@1 (excluding format failures): 63.6% (14/22)*


## TC Improvement Suggestions

