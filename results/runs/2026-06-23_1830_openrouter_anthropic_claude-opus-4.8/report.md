# Benchmark Report: openrouter/anthropic/claude-opus-4.8

**Date:** 2026-06-23 18:30 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/anthropic/claude-opus-4.8 |
| Total Cases | 2 |
| Passed | 1 |
| Failed | 1 |
| pass@1 | 50.0% |

## Failed Cases (1)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-gpio-002` | gpio-basic | static_heuristic | nvic_interrupt_enabled, isr_shared_variable_volatile |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `nvic_interrupt_enabled` | 1 | nxp-mcxc-gpio-002 |
| `isr_shared_variable_volatile` | 1 | nxp-mcxc-gpio-002 |

## TC Improvement Suggestions

