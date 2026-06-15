Write a bare-metal C application for NXP MCXC144 (Cortex-M0+) using the MCUXpresso SDK that fires a PIT (Periodic Interrupt Timer) interrupt every 100 ms and increments a counter.

Requirements:
1. Use PIT channel 0 with a 100 ms period (assume 48 MHz bus clock)
2. Increment a global counter in the PIT ISR
3. In main, print the counter value over UART0 (115200 baud, PTA2 TX) every second

Use the MCUXpresso SDK (fsl_pit.h, fsl_uart.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`); configure pins, clocks and peripherals directly in code.

Output ONLY the complete C source file.
