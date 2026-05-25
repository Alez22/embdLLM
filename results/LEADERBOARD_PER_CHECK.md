# EmbedEval Per-Check Metrics

<!-- SCHEMA_VERSION: 1 -->

**Run ID:** `nxp-phase2`

Per-(TC, check_name, model) pass_rate. Sorted by pass_rate ascending — the most-failed checks are at the top.

| TC ID | Category | Check | Model | pass_rate | passed/samples |
|-------|----------|-------|-------|-----------|----------------|
| nxp-mcxc-flash-001 | storage | flash_erase_sector_called | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-flash-001 | storage | flash_init_called | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-flash-001 | storage | flash_program_called | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-flash-001 | storage | flash_verify_program_called | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-flash-002 | storage | crc_function_implemented | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-flash-002 | storage | full_flash_sequence_present | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-gpio-002 | gpio-basic | header_fsl_clock_h | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-gpio-002 | gpio-basic | interrupt_flag_cleared | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-i2c-001 | spi-i2c | header_fsl_clock_h | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-i2c-001 | spi-i2c | header_fsl_port_h | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-i2c-001 | spi-i2c | i2c_blocking_transfer_used | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-i2c-001 | spi-i2c | i2c_master_init_called | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-i2c-002 | spi-i2c | both_write_and_read_transfers | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-i2c-002 | spi-i2c | header_fsl_port_h | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-i2c-002 | spi-i2c | i2c_master_init_called | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-i2c-002 | spi-i2c | two_separate_transfers | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-isr-001 | isr-concurrency | gpio_pin_read_in_code | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-isr-001 | isr-concurrency | pit_isr_defined | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-isr-001 | isr-concurrency | volatile_shared_data | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-spi-001 | spi-i2c | header_fsl_clock_h | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-spi-001 | spi-i2c | header_fsl_gpio_h | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-spi-001 | spi-i2c | header_fsl_port_h | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-spi-001 | spi-i2c | header_fsl_spi_h | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-spi-001 | spi-i2c | spi_blocking_transfer_used | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-spi-001 | spi-i2c | spi_master_init_called | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-timer-001 | timer | header_fsl_clock_h | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-timer-001 | timer | header_fsl_pit_h | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-timer-001 | timer | pit_init_called | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-timer-001 | timer | pit_isr_defined | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-timer-001 | timer | pit_period_set | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-timer-001 | timer | pit_timer_started | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-uart-001 | uart | uart_tx_enabled_in_config | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-uart-002 | uart | header_fsl_clock_h | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-uart-002 | uart | header_fsl_port_h | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-uart-002 | uart | header_fsl_uart_h | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-uart-002 | uart | ring_buffer_array_declared | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-uart-002 | uart | uart_isr_handler_defined | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-uart-002 | uart | uart_rx_interrupt_enabled | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-watchdog-001 | watchdog | cop_refresh_called | groq/openai/gpt-oss-20b | 0.000 | 0/1 |
| nxp-mcxc-flash-001 | storage | header_fsl_flash_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-flash-001 | storage | no_cross_platform_hallucination | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-flash-002 | storage | header_fsl_flash_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-flash-002 | storage | magic_constant_defined | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-flash-002 | storage | no_cross_platform_hallucination | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-flash-002 | storage | two_flash_slots_defined | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-gpio-001 | gpio-basic | build_env | groq/openai/gpt-oss-20b | 1.000 | 2/2 |
| nxp-mcxc-gpio-001 | gpio-basic | clock_gate_before_gpio_init | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-gpio-001 | gpio-basic | gpio_mux_enum_used | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-gpio-001 | gpio-basic | gpio_pin_init_called | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-gpio-001 | gpio-basic | gpio_toggle_called | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-gpio-001 | gpio-basic | header_fsl_clock_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-gpio-001 | gpio-basic | header_fsl_gpio_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-gpio-001 | gpio-basic | header_fsl_port_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-gpio-001 | gpio-basic | no_cross_platform_hallucination | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-gpio-001 | gpio-basic | output_direction_configured | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-gpio-001 | gpio-basic | pinmux_as_gpio_before_init | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-gpio-002 | gpio-basic | header_fsl_gpio_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-gpio-002 | gpio-basic | header_fsl_port_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-gpio-002 | gpio-basic | isr_handler_defined | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-gpio-002 | gpio-basic | no_cross_platform_hallucination | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-gpio-002 | gpio-basic | pin_interrupt_configured | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-i2c-001 | spi-i2c | header_fsl_i2c_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-i2c-001 | spi-i2c | no_cross_platform_hallucination | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-i2c-002 | spi-i2c | header_fsl_clock_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-i2c-002 | spi-i2c | header_fsl_i2c_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-i2c-002 | spi-i2c | no_cross_platform_hallucination | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-isr-001 | isr-concurrency | header_fsl_clock_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-isr-001 | isr-concurrency | header_fsl_gpio_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-isr-001 | isr-concurrency | header_fsl_pit_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-isr-001 | isr-concurrency | no_cross_platform_hallucination | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-spi-001 | spi-i2c | no_cross_platform_hallucination | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-timer-001 | timer | no_cross_platform_hallucination | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-uart-001 | uart | build_env | groq/openai/gpt-oss-20b | 1.000 | 2/2 |
| nxp-mcxc-uart-001 | uart | clock_gate_before_uart_init | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-uart-001 | uart | header_fsl_clock_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-uart-001 | uart | header_fsl_port_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-uart-001 | uart | header_fsl_uart_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-uart-001 | uart | no_cross_platform_hallucination | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-uart-001 | uart | pinmux_before_uart_init | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-uart-001 | uart | uart_init_called | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-uart-001 | uart | uart_write_blocking_used | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-uart-002 | uart | no_cross_platform_hallucination | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-watchdog-001 | watchdog | cop_init_called | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-watchdog-001 | watchdog | header_fsl_cop_h | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
| nxp-mcxc-watchdog-001 | watchdog | no_cross_platform_hallucination | groq/openai/gpt-oss-20b | 1.000 | 1/1 |
