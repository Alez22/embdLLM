# Benchmark Report: mock

**Date:** 2026-06-17 17:20 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | mock |
| Total Cases | 1 |
| Passed | 0 |
| Failed | 1 |
| pass@1 | 0.0% |

## Failed Cases (1)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `nxp-mcxc-gpio-001` | gpio-basic | static_analysis | header_fsl_gpio_h, header_fsl_port_h, header_fsl_clock_h, gpio_pin_init_called, gpio_toggle_called, no_cross_platform_hallucination |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `header_fsl_gpio_h` | 1 | nxp-mcxc-gpio-001 |
| `header_fsl_port_h` | 1 | nxp-mcxc-gpio-001 |
| `header_fsl_clock_h` | 1 | nxp-mcxc-gpio-001 |
| `gpio_pin_init_called` | 1 | nxp-mcxc-gpio-001 |
| `gpio_toggle_called` | 1 | nxp-mcxc-gpio-001 |
| `no_cross_platform_hallucination` | 1 | nxp-mcxc-gpio-001 |

## TC Improvement Suggestions

