# Benchmark Report: groq/openai/gpt-oss-120b

**Date:** 2026-06-07 21:56 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/openai/gpt-oss-120b |
| Total Cases | 40 |
| Passed | 32 |
| Failed | 8 |
| pass@1 | 80.0% |

## Failed Cases (8)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-002` | device-tree | static_analysis | compatible_present, reg_property_present, status_property_present, spi_max_frequency_present, spi_bus_referenced |
| `device-tree-003` | device-tree | static_analysis | braces_balanced, compatible_present, pwms_property_present, label_property_present, nested_node_structure |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-007` | device-tree | static_analysis | status_present |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `pwm_polarity_specified` | 4 | device-tree-003, device-tree-003, device-tree-003, device-tree-003 |
| `compatible_present` | 2 | device-tree-002, device-tree-003 |
| `interrupt_gpio_present` | 1 | device-tree-001 |
| `reg_property_present` | 1 | device-tree-002 |
| `status_property_present` | 1 | device-tree-002 |
| `spi_max_frequency_present` | 1 | device-tree-002 |
| `spi_bus_referenced` | 1 | device-tree-002 |
| `braces_balanced` | 1 | device-tree-003 |
| `pwms_property_present` | 1 | device-tree-003 |
| `label_property_present` | 1 | device-tree-003 |
| `nested_node_structure` | 1 | device-tree-003 |
| `status_present` | 1 | device-tree-007 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 7 | device-tree-001, device-tree-002, device-tree-003, device-tree-003, device-tree-003 (+2 more) |
| LLM format failure (prose) | 1 | device-tree-003 |

*Adjusted pass@1 (excluding format failures): 82.1% (32/39)*


## TC Improvement Suggestions

