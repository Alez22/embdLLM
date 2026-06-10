# Benchmark Report: groq/meta-llama/llama-4-scout-17b-16e-instruct

**Date:** 2026-06-07 20:50 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/meta-llama/llama-4-scout-17b-16e-instruct |
| Total Cases | 10 |
| Passed | 2 |
| Failed | 8 |
| pass@1 | 20.0% |

## Failed Cases (8)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `adc-001` | adc | static_heuristic | device_ready_check |
| `adc-001` | adc | static_analysis | uses_adc_dt_spec |
| `adc-001` | adc | static_analysis | uses_adc_dt_spec |
| `adc-001` | adc | static_analysis | uses_adc_dt_spec |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `sample_buffer_nonzero` | 4 | adc-002, adc-002, adc-002, adc-002 |
| `uses_adc_dt_spec` | 3 | adc-001, adc-001, adc-001 |
| `device_ready_check` | 1 | adc-001 |

## TC Improvement Suggestions

