# Benchmark Report: groq/qwen/qwen3-32b

**Date:** 2026-06-12 21:37 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/qwen/qwen3-32b |
| Total Cases | 10 |
| Passed | 0 |
| Failed | 10 |
| pass@1 | 0.0% |

## Failed Cases (10)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `adc-001` | adc | static_analysis | code_extracted |
| `adc-001` | adc | static_analysis | code_extracted |
| `adc-001` | adc | static_analysis | code_extracted |
| `adc-001` | adc | static_analysis | code_extracted |
| `adc-001` | adc | static_analysis | code_extracted |
| `adc-002` | adc | static_analysis | code_extracted |
| `adc-002` | adc | static_analysis | code_extracted |
| `adc-002` | adc | static_analysis | oversampling_configured, adc_read_called |
| `adc-002` | adc | static_analysis | code_extracted |
| `adc-002` | adc | static_analysis | code_extracted |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `code_extracted` | 9 | adc-001, adc-001, adc-001, adc-001, adc-001 (+4 more) |
| `oversampling_configured` | 1 | adc-002 |
| `adc_read_called` | 1 | adc-002 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 1 | adc-002 |
| LLM format failure (prose) | 9 | adc-001, adc-001, adc-001, adc-001, adc-001, adc-002, adc-002, adc-002, adc-002 |

*Adjusted pass@1 (excluding format failures): 0.0% (0/1)*


## TC Improvement Suggestions

