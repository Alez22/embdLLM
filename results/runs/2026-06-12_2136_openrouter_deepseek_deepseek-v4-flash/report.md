# Benchmark Report: openrouter/deepseek/deepseek-v4-flash

**Date:** 2026-06-12 21:36 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/deepseek/deepseek-v4-flash |
| Total Cases | 105 |
| Passed | 4 |
| Failed | 101 |
| pass@1 | 3.8% |

## Failed Cases (101)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `adc-001` | adc | static_analysis | llm_call |
| `adc-001` | adc | static_analysis | llm_call |
| `adc-001` | adc | static_analysis | llm_call |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_analysis | llm_call |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `dma-001` | dma | static_analysis | llm_call |
| `dma-001` | dma | static_analysis | llm_call |
| `dma-001` | dma | static_analysis | llm_call |
| `dma-002` | dma | static_analysis | llm_call |
| `dma-002` | dma | static_analysis | llm_call |
| `dma-002` | dma | static_analysis | llm_call |
| `dma-002` | dma | static_analysis | llm_call |
| `dma-002` | dma | static_analysis | llm_call |
| `dma-003` | dma | static_analysis | llm_call |
| `dma-003` | dma | static_analysis | llm_call |
| `dma-003` | dma | static_analysis | llm_call |
| `dma-003` | dma | static_analysis | llm_call |
| `dma-003` | dma | static_analysis | llm_call |
| `dma-004` | dma | static_analysis | llm_call |
| `dma-004` | dma | static_analysis | llm_call |
| `dma-004` | dma | static_analysis | llm_call |
| `dma-004` | dma | static_analysis | llm_call |
| `dma-004` | dma | static_analysis | llm_call |
| `dma-005` | dma | static_analysis | llm_call |
| `dma-005` | dma | static_analysis | llm_call |
| `dma-005` | dma | static_analysis | llm_call |
| `dma-005` | dma | static_analysis | llm_call |
| `dma-005` | dma | static_analysis | llm_call |
| `dma-006` | dma | static_analysis | llm_call |
| `dma-006` | dma | static_analysis | llm_call |
| `dma-006` | dma | static_analysis | llm_call |
| `dma-006` | dma | static_analysis | llm_call |
| `dma-006` | dma | static_analysis | llm_call |
| `dma-007` | dma | static_analysis | llm_call |
| `dma-007` | dma | static_analysis | llm_call |
| `dma-007` | dma | static_analysis | llm_call |
| `dma-007` | dma | static_analysis | llm_call |
| `dma-007` | dma | static_analysis | llm_call |
| `dma-008` | dma | static_analysis | llm_call |
| `dma-008` | dma | static_analysis | llm_call |
| `dma-008` | dma | static_analysis | llm_call |
| `dma-008` | dma | static_analysis | llm_call |
| `dma-008` | dma | static_analysis | llm_call |
| `dma-009` | dma | static_analysis | llm_call |
| `dma-009` | dma | static_analysis | llm_call |
| `dma-009` | dma | static_analysis | llm_call |
| `dma-009` | dma | static_analysis | llm_call |
| `dma-009` | dma | static_analysis | llm_call |
| `dma-011` | dma | static_analysis | llm_call |
| `dma-011` | dma | static_analysis | llm_call |
| `dma-011` | dma | static_analysis | llm_call |
| `dma-011` | dma | static_analysis | llm_call |
| `dma-011` | dma | static_analysis | llm_call |
| `dma-012` | dma | static_analysis | llm_call |
| `dma-012` | dma | static_analysis | llm_call |
| `dma-012` | dma | static_analysis | llm_call |
| `dma-012` | dma | static_analysis | llm_call |
| `dma-012` | dma | static_analysis | llm_call |
| `timer-001` | timer | static_analysis | llm_call |
| `timer-001` | timer | static_analysis | llm_call |
| `timer-001` | timer | static_analysis | llm_call |
| `timer-001` | timer | static_analysis | llm_call |
| `timer-001` | timer | static_analysis | llm_call |
| `timer-002` | timer | static_analysis | llm_call |
| `timer-002` | timer | static_analysis | llm_call |
| `timer-002` | timer | static_analysis | llm_call |
| `timer-002` | timer | static_analysis | llm_call |
| `timer-002` | timer | static_analysis | llm_call |
| `timer-003` | timer | static_analysis | llm_call |
| `timer-003` | timer | static_analysis | llm_call |
| `timer-003` | timer | static_analysis | llm_call |
| `timer-003` | timer | static_analysis | llm_call |
| `timer-003` | timer | static_analysis | llm_call |
| `timer-004` | timer | static_analysis | llm_call |
| `timer-004` | timer | static_analysis | llm_call |
| `timer-004` | timer | static_analysis | llm_call |
| `timer-004` | timer | static_analysis | llm_call |
| `timer-004` | timer | static_analysis | llm_call |
| `timer-005` | timer | static_analysis | llm_call |
| `timer-005` | timer | static_analysis | llm_call |
| `timer-005` | timer | static_analysis | llm_call |
| `timer-005` | timer | static_analysis | llm_call |
| `timer-005` | timer | static_analysis | llm_call |
| `timer-006` | timer | static_analysis | llm_call |
| `timer-006` | timer | static_analysis | llm_call |
| `timer-006` | timer | static_analysis | llm_call |
| `timer-006` | timer | static_analysis | llm_call |
| `timer-006` | timer | static_analysis | llm_call |
| `timer-007` | timer | static_analysis | llm_call |
| `timer-007` | timer | static_analysis | llm_call |
| `timer-007` | timer | static_analysis | llm_call |
| `timer-007` | timer | static_analysis | llm_call |
| `timer-007` | timer | static_analysis | llm_call |
| `timer-008` | timer | static_analysis | llm_call |
| `timer-008` | timer | static_analysis | llm_call |
| `timer-008` | timer | static_analysis | llm_call |
| `timer-008` | timer | static_analysis | llm_call |
| `timer-008` | timer | static_analysis | llm_call |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `llm_call` | 97 | adc-001, adc-001, adc-001, adc-002, dma-001 (+92 more) |
| `sample_buffer_nonzero` | 4 | adc-002, adc-002, adc-002, adc-002 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 4 | adc-002, adc-002, adc-002, adc-002 |
| LLM format failure (prose) | 97 | adc-001, adc-001, adc-001, adc-002, dma-001, dma-001, dma-001, dma-002, dma-002, dma-002, dma-002, dma-002, dma-003, dma-003, dma-003, dma-003, dma-003, dma-004, dma-004, dma-004, dma-004, dma-004, dma-005, dma-005, dma-005, dma-005, dma-005, dma-006, dma-006, dma-006, dma-006, dma-006, dma-007, dma-007, dma-007, dma-007, dma-007, dma-008, dma-008, dma-008, dma-008, dma-008, dma-009, dma-009, dma-009, dma-009, dma-009, dma-011, dma-011, dma-011, dma-011, dma-011, dma-012, dma-012, dma-012, dma-012, dma-012, timer-001, timer-001, timer-001, timer-001, timer-001, timer-002, timer-002, timer-002, timer-002, timer-002, timer-003, timer-003, timer-003, timer-003, timer-003, timer-004, timer-004, timer-004, timer-004, timer-004, timer-005, timer-005, timer-005, timer-005, timer-005, timer-006, timer-006, timer-006, timer-006, timer-006, timer-007, timer-007, timer-007, timer-007, timer-007, timer-008, timer-008, timer-008, timer-008, timer-008 |

*Adjusted pass@1 (excluding format failures): 50.0% (4/8)*


## TC Improvement Suggestions

