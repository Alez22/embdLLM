# EmbedEval Test Results

*Last updated: 2026-07-02 00:21 UTC*

## Summary

> **98 case(s) need retesting** — run `/test <model> --retest-only`

| Model | Cases | Passed | Failed | pass@1 | Retest |
|-------|-------|--------|--------|--------|--------|
| mock | 1 | 0 | 1 | 0.0% | 1 |
| openrouter/anthropic/claude-opus-4.8 | 6 | 4 | 2 | 66.7% | 5 |
| openrouter/anthropic/claude-sonnet-4.6 | 24 | 0 | 24 | 0.0% | 23 |
| openrouter/deepseek/deepseek-v4-flash | 34 | 5 | 29 | 14.7% | 23 |
| openrouter/deepseek/deepseek-v4-pro | 24 | 1 | 23 | 4.2% | 23 |
| openrouter/google/gemma-4-31b-it | 34 | 3 | 31 | 8.8% | 23 |
| openrouter/openai/gpt-oss-120b | 34 | 6 | 28 | 17.6% | - |
| openrouter/qwen/qwen3-235b-a22b | 8 | 5 | 3 | 62.5% | - |
| openrouter/qwen/qwen3-235b-a22b-2507 | 35 | 7 | 28 | 20.0% | - |
| openrouter/z-ai/glm-5.2 | 34 | 6 | 28 | 17.6% | - |

## mock

### Needs Retest (1)

- **nxp-mcxc-gpio-001** (was FAIL, tested 2026-06-23)

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| nxp-mcxc-gpio | 1 | 0 | 0% | header_fsl_gpio_h, header_fsl_port_h, gpio_pin_init_called |

### Failed Cases (1)

| Case | Layer | Failed Checks | Tested | Status |
|------|-------|---------------|--------|--------|
| nxp-mcxc-gpio-001 | L0 | header_fsl_gpio_h, header_fsl_port_h, gpio_pin_init_called, gpio_toggle_called | 2026-06-23 | RETEST |

## openrouter/anthropic/claude-opus-4.8

### Needs Retest (5)

- **nxp-mcxc-flash-001** (was FAIL, tested 2026-06-23)
- **nxp-mcxc-gpio-001** (was PASS, tested 2026-06-23)
- **nxp-mcxc-gpio-002** (was PASS, tested 2026-06-23)
- **nxp-mcxc-i2c-001** (was PASS, tested 2026-06-23)
- **nxp-mcxc-i2c-002** (was PASS, tested 2026-06-23)

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| nxp-mcxc-flash | 2 | 0 | 0% | nxp_gcc, two_flash_slots_defined |
| nxp-mcxc-gpio | 2 | 2 | 100% | - |
| nxp-mcxc-i2c | 2 | 2 | 100% | - |

### Failed Cases (2)

| Case | Layer | Failed Checks | Tested | Status |
|------|-------|---------------|--------|--------|
| nxp-mcxc-flash-001 | L1 | nxp_gcc | 2026-06-23 | RETEST |
| nxp-mcxc-flash-002 | L0 | two_flash_slots_defined | 2026-06-23 | - |

## openrouter/anthropic/claude-sonnet-4.6

### Needs Retest (23)

- **nxp-mcxc-flash-001** (was FAIL, tested 2026-06-17)
- **nxp-mcxc-gpio-001** (was FAIL, tested 2026-06-17)
- **nxp-mcxc-gpio-002** (was FAIL, tested 2026-06-17)
- **nxp-mcxc-i2c-001** (was FAIL, tested 2026-06-17)
- **nxp-mcxc-i2c-002** (was FAIL, tested 2026-06-17)
- **nxp-mcxc-isr-001** (was FAIL, tested 2026-06-17)
- **nxp-mcxc-spi-001** (was FAIL, tested 2026-06-17)
- **nxp-mcxc-timer-001** (was FAIL, tested 2026-06-17)
- **nxp-mcxc-uart-001** (was FAIL, tested 2026-06-17)
- **nxp-mcxc-uart-002** (was FAIL, tested 2026-06-17)
- **nxp-mcxc-watchdog-001** (was FAIL, tested 2026-06-17)
- **nxp-rt1170-audio-001** (was FAIL, tested 2026-06-17)
- **nxp-rt1170-dma-001** (was FAIL, tested 2026-06-17)
- **nxp-rt1170-gpio-001** (was FAIL, tested 2026-06-17)
- **nxp-rt1170-gpio-002** (was FAIL, tested 2026-06-17)
- **nxp-rt1170-gpt-001** (was FAIL, tested 2026-06-17)
- **nxp-rt1170-isr-001** (was FAIL, tested 2026-06-17)
- **nxp-rt1170-lpi2c-001** (was FAIL, tested 2026-06-17)
- **nxp-rt1170-lpspi-001** (was FAIL, tested 2026-06-17)
- **nxp-rt1170-lpuart-001** (was FAIL, tested 2026-06-17)
- **nxp-rt1170-rtwdog-001** (was FAIL, tested 2026-06-17)
- **nxp-rt1170-sai-001** (was FAIL, tested 2026-06-17)
- **nxp-rt1170-sai-002** (was FAIL, tested 2026-06-17)

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| nxp-mcxc-flash | 2 | 0 | 0% | nxp_gcc, nxp_gcc |
| nxp-mcxc-gpio | 2 | 0 | 0% | nxp_gcc, interrupt_flag_cleared |
| nxp-mcxc-i2c | 2 | 0 | 0% | nxp_gcc, nxp_gcc |
| nxp-mcxc-isr | 1 | 0 | 0% | nxp_gcc |
| nxp-mcxc-spi | 1 | 0 | 0% | nxp_gcc |
| nxp-mcxc-timer | 1 | 0 | 0% | nxp_gcc |
| nxp-mcxc-uart | 2 | 0 | 0% | nxp_gcc, uart_isr_handler_defined |
| nxp-mcxc-watchdog | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-audio | 1 | 0 | 0% | read_and_write_api_used |
| nxp-rt1170-dma | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-gpio | 2 | 0 | 0% | nxp_gcc, nxp_gcc |
| nxp-rt1170-gpt | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-isr | 1 | 0 | 0% | critical_section_around_read |
| nxp-rt1170-lpi2c | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-lpspi | 1 | 0 | 0% | clock_root_configured |
| nxp-rt1170-lpuart | 1 | 0 | 0% | init_status_checked |
| nxp-rt1170-rtwdog | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-sai | 2 | 0 | 0% | sai_init_called, sai_write_api_used, nxp_gcc |

### Failed Cases (24)

| Case | Layer | Failed Checks | Tested | Status |
|------|-------|---------------|--------|--------|
| nxp-mcxc-flash-001 | L1 | nxp_gcc | 2026-06-17 | RETEST |
| nxp-mcxc-flash-002 | L1 | nxp_gcc | 2026-06-17 | - |
| nxp-mcxc-gpio-001 | L1 | nxp_gcc | 2026-06-17 | RETEST |
| nxp-mcxc-gpio-002 | L0 | interrupt_flag_cleared | 2026-06-17 | RETEST |
| nxp-mcxc-i2c-001 | L1 | nxp_gcc | 2026-06-17 | RETEST |
| nxp-mcxc-i2c-002 | L1 | nxp_gcc | 2026-06-17 | RETEST |
| nxp-mcxc-isr-001 | L1 | nxp_gcc | 2026-06-17 | RETEST |
| nxp-mcxc-spi-001 | L1 | nxp_gcc | 2026-06-17 | RETEST |
| nxp-mcxc-timer-001 | L1 | nxp_gcc | 2026-06-17 | RETEST |
| nxp-mcxc-uart-001 | L1 | nxp_gcc | 2026-06-17 | RETEST |
| nxp-mcxc-uart-002 | L0 | uart_isr_handler_defined | 2026-06-17 | RETEST |
| nxp-mcxc-watchdog-001 | L1 | nxp_gcc | 2026-06-17 | RETEST |
| nxp-rt1170-audio-001 | L0 | read_and_write_api_used | 2026-06-17 | RETEST |
| nxp-rt1170-dma-001 | L1 | nxp_gcc | 2026-06-17 | RETEST |
| nxp-rt1170-gpio-001 | L1 | nxp_gcc | 2026-06-17 | RETEST |
| nxp-rt1170-gpio-002 | L1 | nxp_gcc | 2026-06-17 | RETEST |
| nxp-rt1170-gpt-001 | L1 | nxp_gcc | 2026-06-17 | RETEST |
| nxp-rt1170-isr-001 | L3 | critical_section_around_read | 2026-06-17 | RETEST |
| nxp-rt1170-lpi2c-001 | L1 | nxp_gcc | 2026-06-17 | RETEST |
| nxp-rt1170-lpspi-001 | L3 | clock_root_configured | 2026-06-17 | RETEST |
| nxp-rt1170-lpuart-001 | L3 | init_status_checked | 2026-06-17 | RETEST |
| nxp-rt1170-rtwdog-001 | L1 | nxp_gcc | 2026-06-17 | RETEST |
| nxp-rt1170-sai-001 | L0 | sai_init_called, sai_write_api_used | 2026-06-17 | RETEST |
| nxp-rt1170-sai-002 | L1 | nxp_gcc | 2026-06-17 | RETEST |

## openrouter/deepseek/deepseek-v4-flash

### Needs Retest (23)

- **nxp-mcxc-flash-001** (was FAIL, tested 2026-06-23)
- **nxp-mcxc-gpio-001** (was FAIL, tested 2026-06-23)
- **nxp-mcxc-gpio-002** (was FAIL, tested 2026-06-23)
- **nxp-mcxc-i2c-001** (was FAIL, tested 2026-06-23)
- **nxp-mcxc-i2c-002** (was FAIL, tested 2026-06-23)
- **nxp-mcxc-isr-001** (was FAIL, tested 2026-06-23)
- **nxp-mcxc-spi-001** (was FAIL, tested 2026-06-23)
- **nxp-mcxc-timer-001** (was FAIL, tested 2026-06-23)
- **nxp-mcxc-uart-001** (was FAIL, tested 2026-06-23)
- **nxp-mcxc-uart-002** (was FAIL, tested 2026-06-23)
- **nxp-mcxc-watchdog-001** (was FAIL, tested 2026-06-23)
- **nxp-rt1170-audio-001** (was FAIL, tested 2026-06-23)
- **nxp-rt1170-dma-001** (was FAIL, tested 2026-06-23)
- **nxp-rt1170-gpio-001** (was FAIL, tested 2026-06-23)
- **nxp-rt1170-gpio-002** (was FAIL, tested 2026-06-23)
- **nxp-rt1170-gpt-001** (was FAIL, tested 2026-06-23)
- **nxp-rt1170-isr-001** (was FAIL, tested 2026-06-23)
- **nxp-rt1170-lpi2c-001** (was FAIL, tested 2026-06-23)
- **nxp-rt1170-lpspi-001** (was FAIL, tested 2026-06-23)
- **nxp-rt1170-lpuart-001** (was FAIL, tested 2026-06-23)
- **nxp-rt1170-rtwdog-001** (was FAIL, tested 2026-06-23)
- **nxp-rt1170-sai-001** (was FAIL, tested 2026-06-23)
- **nxp-rt1170-sai-002** (was FAIL, tested 2026-06-23)

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| adc | 1 | 1 | 100% | - |
| boot | 1 | 1 | 100% | - |
| device-tree | 1 | 0 | 0% | interrupt_gpio_present |
| dma | 1 | 0 | 0% | output_validation |
| gpio-basic | 1 | 1 | 100% | - |
| isr-concurrency | 1 | 0 | 0% | west_build |
| kconfig | 1 | 1 | 100% | - |
| memory-opt | 1 | 0 | 0% | output_validation |
| nxp-mcxc-flash | 2 | 0 | 0% | nxp_gcc, nxp_gcc |
| nxp-mcxc-gpio | 2 | 0 | 0% | header_fsl_clock_h, interrupt_flag_cleared |
| nxp-mcxc-i2c | 2 | 0 | 0% | nxp_gcc, nxp_gcc |
| nxp-mcxc-isr | 1 | 0 | 0% | header_fsl_clock_h |
| nxp-mcxc-spi | 1 | 0 | 0% | header_fsl_port_h, header_fsl_clock_h |
| nxp-mcxc-timer | 1 | 0 | 0% | header_fsl_clock_h |
| nxp-mcxc-uart | 2 | 0 | 0% | nxp_gcc, uart_isr_handler_defined |
| nxp-mcxc-watchdog | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-audio | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-dma | 1 | 0 | 0% | edma_transfer_prepared |
| nxp-rt1170-gpio | 2 | 0 | 0% | nxp_gcc, isr_handler_defined, falling_edge_configured |
| nxp-rt1170-gpt | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-isr | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-lpi2c | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-lpspi | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-lpuart | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-rtwdog | 1 | 0 | 0% | rtwdog_init_called, rtwdog_refresh_used |
| nxp-rt1170-sai | 2 | 0 | 0% | sai_init_called, sai_write_api_used, nxp_gcc |
| spi-i2c | 1 | 1 | 100% | - |
| storage | 1 | 0 | 0% | west_build |

### Failed Cases (29)

| Case | Layer | Failed Checks | Tested | Status |
|------|-------|---------------|--------|--------|
| device-tree-001 | L3 | interrupt_gpio_present | 2026-07-01 | - |
| dma-001 | L2 | output_validation | 2026-07-01 | - |
| isr-concurrency-001 | L1 | west_build | 2026-07-01 | - |
| memory-opt-001 | L2 | output_validation | 2026-07-01 | - |
| nxp-mcxc-flash-001 | L1 | nxp_gcc | 2026-06-23 | RETEST |
| nxp-mcxc-flash-002 | L1 | nxp_gcc | 2026-06-23 | - |
| nxp-mcxc-gpio-001 | L0 | header_fsl_clock_h | 2026-06-23 | RETEST |
| nxp-mcxc-gpio-002 | L0 | interrupt_flag_cleared | 2026-06-23 | RETEST |
| nxp-mcxc-i2c-001 | L1 | nxp_gcc | 2026-06-23 | RETEST |
| nxp-mcxc-i2c-002 | L1 | nxp_gcc | 2026-06-23 | RETEST |
| nxp-mcxc-isr-001 | L0 | header_fsl_clock_h | 2026-06-23 | RETEST |
| nxp-mcxc-spi-001 | L0 | header_fsl_port_h, header_fsl_clock_h | 2026-06-23 | RETEST |
| nxp-mcxc-timer-001 | L0 | header_fsl_clock_h | 2026-06-23 | RETEST |
| nxp-mcxc-uart-001 | L1 | nxp_gcc | 2026-06-23 | RETEST |
| nxp-mcxc-uart-002 | L0 | uart_isr_handler_defined | 2026-06-23 | RETEST |
| nxp-mcxc-watchdog-001 | L1 | nxp_gcc | 2026-06-23 | RETEST |
| nxp-rt1170-audio-001 | L1 | nxp_gcc | 2026-06-23 | RETEST |
| nxp-rt1170-dma-001 | L0 | edma_transfer_prepared | 2026-06-23 | RETEST |
| nxp-rt1170-gpio-001 | L1 | nxp_gcc | 2026-06-23 | RETEST |
| nxp-rt1170-gpio-002 | L0 | isr_handler_defined, falling_edge_configured | 2026-06-23 | RETEST |
| nxp-rt1170-gpt-001 | L1 | nxp_gcc | 2026-06-23 | RETEST |
| nxp-rt1170-isr-001 | L1 | nxp_gcc | 2026-06-23 | RETEST |
| nxp-rt1170-lpi2c-001 | L1 | nxp_gcc | 2026-06-23 | RETEST |
| nxp-rt1170-lpspi-001 | L1 | nxp_gcc | 2026-06-23 | RETEST |
| nxp-rt1170-lpuart-001 | L1 | nxp_gcc | 2026-06-23 | RETEST |
| nxp-rt1170-rtwdog-001 | L0 | rtwdog_init_called, rtwdog_refresh_used | 2026-06-23 | RETEST |
| nxp-rt1170-sai-001 | L0 | sai_init_called, sai_write_api_used | 2026-06-23 | RETEST |
| nxp-rt1170-sai-002 | L1 | nxp_gcc | 2026-06-23 | RETEST |
| storage-006 | L1 | west_build | 2026-07-01 | - |

## openrouter/deepseek/deepseek-v4-pro

### Needs Retest (23)

- **nxp-mcxc-flash-001** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-gpio-001** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-gpio-002** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-i2c-001** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-i2c-002** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-isr-001** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-spi-001** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-timer-001** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-uart-001** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-uart-002** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-watchdog-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-audio-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-dma-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-gpio-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-gpio-002** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-gpt-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-isr-001** (was PASS, tested 2026-06-24)
- **nxp-rt1170-lpi2c-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-lpspi-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-lpuart-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-rtwdog-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-sai-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-sai-002** (was FAIL, tested 2026-06-24)

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| nxp-mcxc-flash | 2 | 0 | 0% | flash_verify_program_called, two_flash_slots_defined |
| nxp-mcxc-gpio | 2 | 0 | 0% | header_fsl_port_h, interrupt_flag_cleared |
| nxp-mcxc-i2c | 2 | 0 | 0% | i2c_blocking_transfer_used, nxp_gcc |
| nxp-mcxc-isr | 1 | 0 | 0% | nxp_gcc |
| nxp-mcxc-spi | 1 | 0 | 0% | nxp_gcc |
| nxp-mcxc-timer | 1 | 0 | 0% | nxp_gcc |
| nxp-mcxc-uart | 2 | 0 | 0% | nxp_gcc, uart_isr_handler_defined |
| nxp-mcxc-watchdog | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-audio | 1 | 0 | 0% | read_and_write_api_used |
| nxp-rt1170-dma | 1 | 0 | 0% | edma_transfer_started |
| nxp-rt1170-gpio | 2 | 0 | 0% | nxp_gcc, nxp_gcc |
| nxp-rt1170-gpt | 1 | 0 | 0% | isr_handler_defined |
| nxp-rt1170-isr | 1 | 1 | 100% | - |
| nxp-rt1170-lpi2c | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-lpspi | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-lpuart | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-rtwdog | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-sai | 2 | 0 | 0% | sai_write_api_used, nxp_gcc |

### Failed Cases (23)

| Case | Layer | Failed Checks | Tested | Status |
|------|-------|---------------|--------|--------|
| nxp-mcxc-flash-001 | L0 | flash_verify_program_called | 2026-06-24 | RETEST |
| nxp-mcxc-flash-002 | L0 | two_flash_slots_defined | 2026-06-24 | - |
| nxp-mcxc-gpio-001 | L0 | header_fsl_port_h | 2026-06-24 | RETEST |
| nxp-mcxc-gpio-002 | L0 | interrupt_flag_cleared | 2026-06-24 | RETEST |
| nxp-mcxc-i2c-001 | L0 | i2c_blocking_transfer_used | 2026-06-24 | RETEST |
| nxp-mcxc-i2c-002 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-mcxc-isr-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-mcxc-spi-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-mcxc-timer-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-mcxc-uart-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-mcxc-uart-002 | L0 | uart_isr_handler_defined | 2026-06-24 | RETEST |
| nxp-mcxc-watchdog-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-rt1170-audio-001 | L0 | read_and_write_api_used | 2026-06-24 | RETEST |
| nxp-rt1170-dma-001 | L0 | edma_transfer_started | 2026-06-24 | RETEST |
| nxp-rt1170-gpio-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-rt1170-gpio-002 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-rt1170-gpt-001 | L0 | isr_handler_defined | 2026-06-24 | RETEST |
| nxp-rt1170-lpi2c-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-rt1170-lpspi-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-rt1170-lpuart-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-rt1170-rtwdog-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-rt1170-sai-001 | L0 | sai_write_api_used | 2026-06-24 | RETEST |
| nxp-rt1170-sai-002 | L1 | nxp_gcc | 2026-06-24 | RETEST |

## openrouter/google/gemma-4-31b-it

### Needs Retest (23)

- **nxp-mcxc-flash-001** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-gpio-001** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-gpio-002** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-i2c-001** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-i2c-002** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-isr-001** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-spi-001** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-timer-001** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-uart-001** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-uart-002** (was FAIL, tested 2026-06-24)
- **nxp-mcxc-watchdog-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-audio-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-dma-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-gpio-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-gpio-002** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-gpt-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-isr-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-lpi2c-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-lpspi-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-lpuart-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-rtwdog-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-sai-001** (was FAIL, tested 2026-06-24)
- **nxp-rt1170-sai-002** (was FAIL, tested 2026-06-24)

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| adc | 1 | 1 | 100% | - |
| boot | 1 | 0 | 0% | img_manager_enabled |
| device-tree | 1 | 0 | 0% | interrupt_gpio_present |
| dma | 1 | 0 | 0% | west_build |
| gpio-basic | 1 | 1 | 100% | - |
| isr-concurrency | 1 | 0 | 0% | no_printk, uses_atomic_operations |
| kconfig | 1 | 0 | 0% | spi_dma_enabled |
| memory-opt | 1 | 0 | 0% | west_build |
| nxp-mcxc-flash | 2 | 0 | 0% | flash_init_called, flash_verify_program_called, crc_function_implemented, full_flash_sequence_present |
| nxp-mcxc-gpio | 2 | 0 | 0% | header_fsl_port_h, pin_interrupt_configured, isr_handler_defined |
| nxp-mcxc-i2c | 2 | 0 | 0% | nxp_gcc, header_fsl_port_h, both_write_and_read_transfers, two_separate_transfers |
| nxp-mcxc-isr | 1 | 0 | 0% | pit_isr_defined |
| nxp-mcxc-spi | 1 | 0 | 0% | header_fsl_port_h |
| nxp-mcxc-timer | 1 | 0 | 0% | pit_period_set, pit_isr_defined |
| nxp-mcxc-uart | 2 | 0 | 0% | uart_write_blocking_used, uart_isr_handler_defined |
| nxp-mcxc-watchdog | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-audio | 1 | 0 | 0% | read_and_write_api_used |
| nxp-rt1170-dma | 1 | 0 | 0% | edma_init_called, edma_transfer_prepared, edma_transfer_started |
| nxp-rt1170-gpio | 2 | 0 | 0% | nxp_gcc, isr_handler_defined, interrupt_flag_cleared, falling_edge_configured |
| nxp-rt1170-gpt | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-isr | 1 | 0 | 0% | interrupt_flag_cleared |
| nxp-rt1170-lpi2c | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-lpspi | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-lpuart | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-rtwdog | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-sai | 2 | 0 | 0% | header_fsl_iomuxc_h, sai_tx_configured, sai_write_api_used, header_fsl_iomuxc_h |
| spi-i2c | 1 | 1 | 100% | - |
| storage | 1 | 0 | 0% | success_printed |

### Failed Cases (31)

| Case | Layer | Failed Checks | Tested | Status |
|------|-------|---------------|--------|--------|
| boot-001 | L0 | img_manager_enabled | 2026-07-01 | - |
| device-tree-001 | L3 | interrupt_gpio_present | 2026-07-01 | - |
| dma-001 | L1 | west_build | 2026-07-01 | - |
| isr-concurrency-001 | L0 | no_printk, uses_atomic_operations | 2026-07-01 | - |
| kconfig-001 | L0 | spi_dma_enabled | 2026-07-01 | - |
| memory-opt-001 | L1 | west_build | 2026-07-01 | - |
| nxp-mcxc-flash-001 | L0 | flash_init_called, flash_verify_program_called | 2026-06-24 | RETEST |
| nxp-mcxc-flash-002 | L0 | crc_function_implemented, full_flash_sequence_present | 2026-06-24 | - |
| nxp-mcxc-gpio-001 | L0 | header_fsl_port_h | 2026-06-24 | RETEST |
| nxp-mcxc-gpio-002 | L0 | pin_interrupt_configured, isr_handler_defined | 2026-06-24 | RETEST |
| nxp-mcxc-i2c-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-mcxc-i2c-002 | L0 | header_fsl_port_h, both_write_and_read_transfers, two_separate_transfers | 2026-06-24 | RETEST |
| nxp-mcxc-isr-001 | L0 | pit_isr_defined | 2026-06-24 | RETEST |
| nxp-mcxc-spi-001 | L0 | header_fsl_port_h | 2026-06-24 | RETEST |
| nxp-mcxc-timer-001 | L0 | pit_period_set, pit_isr_defined | 2026-06-24 | RETEST |
| nxp-mcxc-uart-001 | L0 | uart_write_blocking_used | 2026-06-24 | RETEST |
| nxp-mcxc-uart-002 | L0 | uart_isr_handler_defined | 2026-06-24 | RETEST |
| nxp-mcxc-watchdog-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-rt1170-audio-001 | L0 | read_and_write_api_used | 2026-06-24 | RETEST |
| nxp-rt1170-dma-001 | L0 | edma_init_called, edma_transfer_prepared, edma_transfer_started | 2026-06-24 | RETEST |
| nxp-rt1170-gpio-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-rt1170-gpio-002 | L0 | isr_handler_defined, interrupt_flag_cleared, falling_edge_configured | 2026-06-24 | RETEST |
| nxp-rt1170-gpt-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-rt1170-isr-001 | L0 | interrupt_flag_cleared | 2026-06-24 | RETEST |
| nxp-rt1170-lpi2c-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-rt1170-lpspi-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-rt1170-lpuart-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-rt1170-rtwdog-001 | L1 | nxp_gcc | 2026-06-24 | RETEST |
| nxp-rt1170-sai-001 | L0 | header_fsl_iomuxc_h, sai_tx_configured, sai_write_api_used, lpi2c_blocking_transfer_used | 2026-06-24 | RETEST |
| nxp-rt1170-sai-002 | L0 | header_fsl_iomuxc_h | 2026-06-24 | RETEST |
| storage-006 | L3 | success_printed | 2026-07-01 | - |

## openrouter/openai/gpt-oss-120b

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| adc | 1 | 1 | 100% | - |
| boot | 1 | 0 | 0% | img_manager_enabled |
| device-tree | 1 | 1 | 100% | - |
| dma | 1 | 0 | 0% | dma_header_included |
| gpio-basic | 1 | 1 | 100% | - |
| isr-concurrency | 1 | 0 | 0% | zephyr_headers_included |
| kconfig | 1 | 1 | 100% | - |
| memory-opt | 1 | 0 | 0% | west_build |
| nxp-mcxc-flash | 2 | 0 | 0% | flash_verify_program_called, nxp_gcc |
| nxp-mcxc-gpio | 2 | 0 | 0% | nxp_gcc, pin_interrupt_configured, interrupt_flag_cleared |
| nxp-mcxc-i2c | 2 | 0 | 0% | nxp_gcc, nxp_gcc |
| nxp-mcxc-isr | 1 | 0 | 0% | nxp_gcc |
| nxp-mcxc-spi | 1 | 0 | 0% | nxp_gcc |
| nxp-mcxc-timer | 1 | 0 | 0% | nxp_gcc |
| nxp-mcxc-uart | 2 | 0 | 0% | nxp_gcc, uart_isr_handler_defined |
| nxp-mcxc-watchdog | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-audio | 1 | 0 | 0% | read_and_write_api_used |
| nxp-rt1170-dma | 1 | 0 | 0% | edma_transfer_prepared |
| nxp-rt1170-gpio | 2 | 0 | 0% | nxp_gcc, falling_edge_configured |
| nxp-rt1170-gpt | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-isr | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-lpi2c | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-lpspi | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-lpuart | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-rtwdog | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-sai | 2 | 0 | 0% | sai_init_called, sai_write_api_used, nxp_gcc |
| spi-i2c | 1 | 1 | 100% | - |
| storage | 1 | 1 | 100% | - |

### Failed Cases (28)

| Case | Layer | Failed Checks | Tested |
|------|-------|---------------|--------|
| boot-001 | L0 | img_manager_enabled | 2026-07-01 |
| dma-001 | L0 | dma_header_included | 2026-07-01 |
| isr-concurrency-001 | L0 | zephyr_headers_included | 2026-07-01 |
| memory-opt-001 | L1 | west_build | 2026-07-01 |
| nxp-mcxc-flash-001 | L0 | flash_verify_program_called | 2026-07-01 |
| nxp-mcxc-flash-002 | L1 | nxp_gcc | 2026-07-01 |
| nxp-mcxc-gpio-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-mcxc-gpio-002 | L0 | pin_interrupt_configured, interrupt_flag_cleared | 2026-07-01 |
| nxp-mcxc-i2c-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-mcxc-i2c-002 | L1 | nxp_gcc | 2026-07-01 |
| nxp-mcxc-isr-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-mcxc-spi-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-mcxc-timer-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-mcxc-uart-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-mcxc-uart-002 | L0 | uart_isr_handler_defined | 2026-07-01 |
| nxp-mcxc-watchdog-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-audio-001 | L0 | read_and_write_api_used | 2026-07-01 |
| nxp-rt1170-dma-001 | L0 | edma_transfer_prepared | 2026-07-01 |
| nxp-rt1170-gpio-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-gpio-002 | L0 | falling_edge_configured | 2026-07-01 |
| nxp-rt1170-gpt-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-isr-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-lpi2c-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-lpspi-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-lpuart-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-rtwdog-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-sai-001 | L0 | sai_init_called, sai_write_api_used | 2026-07-01 |
| nxp-rt1170-sai-002 | L1 | nxp_gcc | 2026-07-01 |

## openrouter/qwen/qwen3-235b-a22b

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| device-tree | 8 | 5 | 62% | gpio_active_low, pwm_polarity_specified, transceiver_nested_in_can0 |

### Failed Cases (3)

| Case | Layer | Failed Checks | Tested |
|------|-------|---------------|--------|
| device-tree-001 | L3 | gpio_active_low | 2026-06-13 |
| device-tree-003 | L3 | pwm_polarity_specified | 2026-06-13 |
| device-tree-004 | L3 | transceiver_nested_in_can0 | 2026-06-13 |

## openrouter/qwen/qwen3-235b-a22b-2507

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| adc | 2 | 2 | 100% | - |
| boot | 1 | 1 | 100% | - |
| device-tree | 1 | 1 | 100% | - |
| dma | 1 | 0 | 0% | llm_call |
| gpio-basic | 1 | 1 | 100% | - |
| isr-concurrency | 1 | 0 | 0% | no_printk |
| kconfig | 1 | 1 | 100% | - |
| memory-opt | 1 | 0 | 0% | mem_slab_defined, slab_alloc_called, slab_free_called |
| nxp-mcxc-flash | 2 | 0 | 0% | flash_verify_program_called, nxp_gcc |
| nxp-mcxc-gpio | 2 | 0 | 0% | nxp_gcc, header_fsl_clock_h, pin_interrupt_configured, interrupt_flag_cleared |
| nxp-mcxc-i2c | 2 | 0 | 0% | nxp_gcc, nxp_gcc |
| nxp-mcxc-isr | 1 | 0 | 0% | pit_isr_defined, gpio_pin_read_in_code |
| nxp-mcxc-spi | 1 | 0 | 0% | header_fsl_port_h, spi_master_init_called, spi_blocking_transfer_used |
| nxp-mcxc-timer | 1 | 0 | 0% | nxp_gcc |
| nxp-mcxc-uart | 2 | 0 | 0% | nxp_gcc, uart_isr_handler_defined |
| nxp-mcxc-watchdog | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-audio | 1 | 0 | 0% | read_and_write_api_used |
| nxp-rt1170-dma | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-gpio | 2 | 0 | 0% | nxp_gcc, nxp_gcc |
| nxp-rt1170-gpt | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-isr | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-lpi2c | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-lpspi | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-lpuart | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-rtwdog | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-sai | 2 | 0 | 0% | sai_tx_configured, lpi2c_blocking_transfer_used, nxp_gcc |
| spi-i2c | 1 | 1 | 100% | - |
| storage | 1 | 0 | 0% | west_build |

### Failed Cases (28)

| Case | Layer | Failed Checks | Tested |
|------|-------|---------------|--------|
| dma-001 | L0 | llm_call | 2026-07-01 |
| isr-concurrency-001 | L0 | no_printk | 2026-07-01 |
| memory-opt-001 | L0 | mem_slab_defined, slab_alloc_called, slab_free_called | 2026-07-01 |
| nxp-mcxc-flash-001 | L0 | flash_verify_program_called | 2026-07-01 |
| nxp-mcxc-flash-002 | L1 | nxp_gcc | 2026-07-01 |
| nxp-mcxc-gpio-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-mcxc-gpio-002 | L0 | header_fsl_clock_h, pin_interrupt_configured, interrupt_flag_cleared | 2026-07-01 |
| nxp-mcxc-i2c-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-mcxc-i2c-002 | L1 | nxp_gcc | 2026-07-01 |
| nxp-mcxc-isr-001 | L0 | pit_isr_defined, gpio_pin_read_in_code | 2026-07-01 |
| nxp-mcxc-spi-001 | L0 | header_fsl_port_h, spi_master_init_called, spi_blocking_transfer_used | 2026-07-01 |
| nxp-mcxc-timer-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-mcxc-uart-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-mcxc-uart-002 | L0 | uart_isr_handler_defined | 2026-07-01 |
| nxp-mcxc-watchdog-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-audio-001 | L0 | read_and_write_api_used | 2026-07-01 |
| nxp-rt1170-dma-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-gpio-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-gpio-002 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-gpt-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-isr-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-lpi2c-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-lpspi-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-lpuart-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-rtwdog-001 | L1 | nxp_gcc | 2026-07-01 |
| nxp-rt1170-sai-001 | L0 | sai_tx_configured, lpi2c_blocking_transfer_used | 2026-07-01 |
| nxp-rt1170-sai-002 | L1 | nxp_gcc | 2026-07-01 |
| storage-006 | L1 | west_build | 2026-07-01 |

## openrouter/z-ai/glm-5.2

| Category | Cases | Passed | pass@1 | Failed Checks |
|----------|-------|--------|--------|---------------|
| adc | 1 | 1 | 100% | - |
| boot | 1 | 0 | 0% | img_manager_dependency |
| device-tree | 1 | 0 | 0% | interrupt_gpio_present |
| dma | 1 | 0 | 0% | separate_src_dst_buffers |
| gpio-basic | 1 | 1 | 100% | - |
| isr-concurrency | 1 | 0 | 0% | west_build |
| kconfig | 1 | 0 | 0% | spi_dma_enabled |
| memory-opt | 1 | 0 | 0% | west_build |
| nxp-mcxc-flash | 2 | 0 | 0% | nxp_gcc, nxp_gcc |
| nxp-mcxc-gpio | 2 | 1 | 50% | interrupt_flag_cleared |
| nxp-mcxc-i2c | 2 | 0 | 0% | nxp_gcc, nxp_gcc |
| nxp-mcxc-isr | 1 | 0 | 0% | pit_isr_defined |
| nxp-mcxc-spi | 1 | 0 | 0% | nxp_gcc |
| nxp-mcxc-timer | 1 | 0 | 0% | pit_isr_defined |
| nxp-mcxc-uart | 2 | 0 | 0% | nxp_gcc, uart_isr_handler_defined |
| nxp-mcxc-watchdog | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-audio | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-dma | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-gpio | 2 | 0 | 0% | nxp_gcc, interrupt_flag_cleared |
| nxp-rt1170-gpt | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-isr | 1 | 1 | 100% | - |
| nxp-rt1170-lpi2c | 1 | 0 | 0% | clock_root_configured, transfer_return_value_checked |
| nxp-rt1170-lpspi | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-lpuart | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-rtwdog | 1 | 0 | 0% | nxp_gcc |
| nxp-rt1170-sai | 2 | 0 | 0% | sai_init_called, sai_write_api_used, nxp_gcc |
| spi-i2c | 1 | 1 | 100% | - |
| storage | 1 | 1 | 100% | - |

### Failed Cases (28)

| Case | Layer | Failed Checks | Tested |
|------|-------|---------------|--------|
| boot-001 | L3 | img_manager_dependency | 2026-07-02 |
| device-tree-001 | L3 | interrupt_gpio_present | 2026-07-02 |
| dma-001 | L3 | separate_src_dst_buffers | 2026-07-02 |
| isr-concurrency-001 | L1 | west_build | 2026-07-02 |
| kconfig-001 | L0 | spi_dma_enabled | 2026-07-02 |
| memory-opt-001 | L1 | west_build | 2026-07-02 |
| nxp-mcxc-flash-001 | L1 | nxp_gcc | 2026-07-02 |
| nxp-mcxc-flash-002 | L1 | nxp_gcc | 2026-07-02 |
| nxp-mcxc-gpio-002 | L0 | interrupt_flag_cleared | 2026-07-02 |
| nxp-mcxc-i2c-001 | L1 | nxp_gcc | 2026-07-02 |
| nxp-mcxc-i2c-002 | L1 | nxp_gcc | 2026-07-02 |
| nxp-mcxc-isr-001 | L0 | pit_isr_defined | 2026-07-02 |
| nxp-mcxc-spi-001 | L1 | nxp_gcc | 2026-07-02 |
| nxp-mcxc-timer-001 | L0 | pit_isr_defined | 2026-07-02 |
| nxp-mcxc-uart-001 | L1 | nxp_gcc | 2026-07-02 |
| nxp-mcxc-uart-002 | L0 | uart_isr_handler_defined | 2026-07-02 |
| nxp-mcxc-watchdog-001 | L1 | nxp_gcc | 2026-07-02 |
| nxp-rt1170-audio-001 | L1 | nxp_gcc | 2026-07-02 |
| nxp-rt1170-dma-001 | L1 | nxp_gcc | 2026-07-02 |
| nxp-rt1170-gpio-001 | L1 | nxp_gcc | 2026-07-02 |
| nxp-rt1170-gpio-002 | L0 | interrupt_flag_cleared | 2026-07-02 |
| nxp-rt1170-gpt-001 | L1 | nxp_gcc | 2026-07-02 |
| nxp-rt1170-lpi2c-001 | L3 | clock_root_configured, transfer_return_value_checked | 2026-07-02 |
| nxp-rt1170-lpspi-001 | L1 | nxp_gcc | 2026-07-02 |
| nxp-rt1170-lpuart-001 | L1 | nxp_gcc | 2026-07-02 |
| nxp-rt1170-rtwdog-001 | L1 | nxp_gcc | 2026-07-02 |
| nxp-rt1170-sai-001 | L0 | sai_init_called, sai_write_api_used | 2026-07-02 |
| nxp-rt1170-sai-002 | L1 | nxp_gcc | 2026-07-02 |

