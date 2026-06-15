Write a bare-metal C application for NXP i.MX RT1170 (Cortex-M7) using the MCUXpresso SDK that maintains a millisecond tick counter.

Requirements:
1. Use GPT1 to generate an interrupt every 1 ms
2. In the interrupt handler, increment a 32-bit tick counter
3. The main loop does nothing but wait

Use the MCUXpresso SDK (fsl_gpt.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Configure pins, clocks and peripherals with the SDK driver APIs within this file. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`).

Output ONLY the complete C source file.
