# Benchmark Report: groq/openai/gpt-oss-20b

**Date:** 2026-06-07 20:58 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | groq/openai/gpt-oss-20b |
| Total Cases | 10 |
| Passed | 5 |
| Failed | 5 |
| pass@1 | 50.0% |

## Failed Cases (5)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `adc-001` | adc | static_heuristic | periodic_sampling_loop |
| `adc-001` | adc | static_heuristic | device_ready_check |
| `adc-002` | adc | static_heuristic | periodic_read_with_sleep |
| `adc-002` | adc | static_heuristic | periodic_read_with_sleep |
| `adc-002` | adc | static_heuristic | periodic_read_with_sleep |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `periodic_read_with_sleep` | 3 | adc-002, adc-002, adc-002 |
| `periodic_sampling_loop` | 1 | adc-001 |
| `device_ready_check` | 1 | adc-001 |

## TC Improvement Suggestions

