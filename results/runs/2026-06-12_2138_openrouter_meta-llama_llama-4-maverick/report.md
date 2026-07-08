# Benchmark Report: openrouter/meta-llama/llama-4-maverick

**Date:** 2026-06-12 21:38 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/meta-llama/llama-4-maverick |
| Total Cases | 10 |
| Passed | 0 |
| Failed | 10 |
| pass@1 | 0.0% |

## Failed Cases (10)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `adc-001` | adc | static_analysis | llm_call |
| `adc-001` | adc | static_analysis | llm_call |
| `adc-001` | adc | static_analysis | llm_call |
| `adc-001` | adc | static_analysis | llm_call |
| `adc-001` | adc | static_analysis | llm_call |
| `adc-002` | adc | static_analysis | llm_call |
| `adc-002` | adc | static_analysis | llm_call |
| `adc-002` | adc | static_analysis | llm_call |
| `adc-002` | adc | static_analysis | llm_call |
| `adc-002` | adc | static_analysis | llm_call |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `llm_call` | 10 | adc-001, adc-001, adc-001, adc-001, adc-001 (+5 more) |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 0 |  |
| LLM format failure (prose) | 10 | adc-001, adc-001, adc-001, adc-001, adc-001, adc-002, adc-002, adc-002, adc-002, adc-002 |


## TC Improvement Suggestions

