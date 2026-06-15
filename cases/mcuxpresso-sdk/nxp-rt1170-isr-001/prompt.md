Write a bare-metal C application for NXP i.MX RT1170 (Cortex-M7) using the MCUXpresso SDK that tracks system uptime.

Requirements:
1. Use GPT2 to generate an interrupt every 1 ms
2. In the interrupt handler, increment a 64-bit uptime counter (milliseconds since boot)
3. Implement a function `uint64_t uptime_ms(void)` that returns the current uptime, called from the main loop
4. The main loop repeatedly reads the uptime

Use the MCUXpresso SDK (fsl_gpt.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`); configure pins, clocks and peripherals directly in code.

Output ONLY the complete C source file.
