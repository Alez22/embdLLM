# Benchmark Report: openrouter/qwen/qwen3-235b-a22b-2507

**Date:** 2026-06-13 20:50 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/qwen/qwen3-235b-a22b-2507 |
| Total Cases | 10 |
| Passed | 8 |
| Failed | 2 |
| pass@1 | 80.0% |

## Failed Cases (2)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `sample_buffer_nonzero` | 2 | adc-002, adc-002 |

## TC Improvement Suggestions

