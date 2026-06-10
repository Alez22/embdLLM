# Benchmark Report: openrouter/qwen/qwen3-30b-a3b

**Date:** 2026-06-07 20:13 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/qwen/qwen3-30b-a3b |
| Total Cases | 40 |
| Passed | 0 |
| Failed | 40 |
| pass@1 | 0.0% |

## Failed Cases (40)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `kconfig-001` | kconfig | static_analysis | llm_call |
| `kconfig-001` | kconfig | static_analysis | llm_call |
| `kconfig-001` | kconfig | static_analysis | llm_call |
| `kconfig-001` | kconfig | static_analysis | llm_call |
| `kconfig-001` | kconfig | static_analysis | llm_call |
| `kconfig-002` | kconfig | static_analysis | llm_call |
| `kconfig-002` | kconfig | static_analysis | llm_call |
| `kconfig-002` | kconfig | static_analysis | llm_call |
| `kconfig-002` | kconfig | static_analysis | llm_call |
| `kconfig-002` | kconfig | static_analysis | llm_call |
| `kconfig-003` | kconfig | static_analysis | llm_call |
| `kconfig-003` | kconfig | static_analysis | llm_call |
| `kconfig-003` | kconfig | static_analysis | llm_call |
| `kconfig-003` | kconfig | static_analysis | llm_call |
| `kconfig-003` | kconfig | static_analysis | llm_call |
| `kconfig-004` | kconfig | static_analysis | llm_call |
| `kconfig-004` | kconfig | static_analysis | llm_call |
| `kconfig-004` | kconfig | static_analysis | llm_call |
| `kconfig-004` | kconfig | static_analysis | llm_call |
| `kconfig-004` | kconfig | static_analysis | llm_call |
| `kconfig-005` | kconfig | static_analysis | llm_call |
| `kconfig-005` | kconfig | static_analysis | llm_call |
| `kconfig-005` | kconfig | static_analysis | llm_call |
| `kconfig-005` | kconfig | static_analysis | llm_call |
| `kconfig-005` | kconfig | static_analysis | llm_call |
| `kconfig-006` | kconfig | static_analysis | llm_call |
| `kconfig-006` | kconfig | static_analysis | llm_call |
| `kconfig-006` | kconfig | static_analysis | llm_call |
| `kconfig-006` | kconfig | static_analysis | llm_call |
| `kconfig-006` | kconfig | static_analysis | llm_call |
| `kconfig-007` | kconfig | static_analysis | llm_call |
| `kconfig-007` | kconfig | static_analysis | llm_call |
| `kconfig-007` | kconfig | static_analysis | llm_call |
| `kconfig-007` | kconfig | static_analysis | llm_call |
| `kconfig-007` | kconfig | static_analysis | llm_call |
| `kconfig-008` | kconfig | static_analysis | llm_call |
| `kconfig-008` | kconfig | static_analysis | llm_call |
| `kconfig-008` | kconfig | static_analysis | llm_call |
| `kconfig-008` | kconfig | static_analysis | llm_call |
| `kconfig-008` | kconfig | static_analysis | llm_call |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `llm_call` | 40 | kconfig-001, kconfig-001, kconfig-001, kconfig-001, kconfig-001 (+35 more) |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 0 |  |
| LLM format failure (prose) | 40 | kconfig-001, kconfig-001, kconfig-001, kconfig-001, kconfig-001, kconfig-002, kconfig-002, kconfig-002, kconfig-002, kconfig-002, kconfig-003, kconfig-003, kconfig-003, kconfig-003, kconfig-003, kconfig-004, kconfig-004, kconfig-004, kconfig-004, kconfig-004, kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-006, kconfig-006, kconfig-006, kconfig-006, kconfig-006, kconfig-007, kconfig-007, kconfig-007, kconfig-007, kconfig-007, kconfig-008, kconfig-008, kconfig-008, kconfig-008, kconfig-008 |


## TC Improvement Suggestions

