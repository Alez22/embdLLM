Write a bare-metal C application for NXP MCXC144 (Cortex-M0+) using the MCUXpresso SDK that samples a digital input in a PIT ISR and passes the result to the main loop.

Requirements:
1. Use PIT channel 0 at 10 ms period (48 MHz bus clock)
2. In the ISR, read PTC3 (digital input) and store the value
3. Signal the main loop that a new sample is ready using a flag
4. Main reads the flag and the sample value; if the pin is high, toggle PTE24 (LED)
5. The data transfer between ISR and main must be safe from race conditions

Use the MCUXpresso SDK (fsl_pit.h, fsl_gpio.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Configure pins, clocks and peripherals with the SDK driver APIs within this file. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`).

Output ONLY the complete C source file.
