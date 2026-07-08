# Benchmark Report: openrouter/anthropic/claude-opus-4.8

**Date:** 2026-06-23 18:38 UTC

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
| `nxp-mcxc-gpio-002` | gpio-basic | static_analysis | llm_call |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `llm_call` | 1 | nxp-mcxc-gpio-002 |

## Failure Classification

| Type | Count | Cases |
|------|-------|-------|
| Genuine code error | 0 |  |
| LLM format failure (prose) | 1 | nxp-mcxc-gpio-002 |

*Adjusted pass@1 (excluding format failures): 100.0% (1/1)*


## TC Improvement Suggestions

