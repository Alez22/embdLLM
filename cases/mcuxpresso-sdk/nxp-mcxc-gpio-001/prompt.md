Write a bare-metal C application for NXP MCXC144 (Cortex-M0+) using the MCUXpresso SDK that toggles an LED connected to PTE24.

Requirements:
1. Configure PTE24 as a digital output
2. Toggle the pin every iteration of the main loop
3. Use a simple software delay between toggles

Use the MCUXpresso SDK (fsl_gpio.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`); configure pins, clocks and peripherals directly in code.

Output ONLY the complete C source file.
