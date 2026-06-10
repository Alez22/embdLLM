# Benchmark Report: groq/openai/gpt-oss-120b

**Date:** 2026-06-07 21:00 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/openai/gpt-oss-120b |
| Total Cases | 10 |
| Passed | 5 |
| Failed | 5 |
| pass@1 | 50.0% |

## Failed Cases (5)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `adc-001` | adc | static_analysis | adc_sequence_defined |
| `adc-001` | adc | static_analysis | adc_sequence_defined |
| `adc-001` | adc | static_heuristic | periodic_sampling_loop |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `adc_sequence_defined` | 2 | adc-001, adc-001 |
| `sample_buffer_nonzero` | 2 | adc-002, adc-002 |
| `periodic_sampling_loop` | 1 | adc-001 |

## TC Improvement Suggestions

