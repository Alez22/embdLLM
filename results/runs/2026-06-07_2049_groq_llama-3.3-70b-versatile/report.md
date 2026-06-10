# Benchmark Report: groq/llama-3.3-70b-versatile

**Date:** 2026-06-07 20:49 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/llama-3.3-70b-versatile |
| Total Cases | 10 |
| Passed | 1 |
| Failed | 9 |
| pass@1 | 10.0% |

## Failed Cases (9)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `adc-001` | adc | static_analysis | uses_adc_dt_spec |
| `adc-001` | adc | static_analysis | uses_adc_dt_spec |
| `adc-001` | adc | static_analysis | uses_adc_dt_spec |
| `adc-001` | adc | static_analysis | uses_adc_dt_spec |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `sample_buffer_nonzero` | 5 | adc-002, adc-002, adc-002, adc-002, adc-002 |
| `uses_adc_dt_spec` | 4 | adc-001, adc-001, adc-001, adc-001 |

## TC Improvement Suggestions

