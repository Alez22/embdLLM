# Benchmark Report: openrouter/anthropic/claude-opus-4.8

**Date:** 2026-06-23 17:53 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/anthropic/claude-opus-4.8 |
| Total Cases | 2 |
| Passed | 0 |
| Failed | 2 |
| pass@1 | 0.0% |

## Failed Cases (2)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-flash-001` | storage | compile_gate | nxp_gcc |
| `nxp-mcxc-flash-002` | storage | static_analysis | two_flash_slots_defined |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `nxp_gcc` | 1 | nxp-mcxc-flash-001 |
| `two_flash_slots_defined` | 1 | nxp-mcxc-flash-002 |

## TC Improvement Suggestions

