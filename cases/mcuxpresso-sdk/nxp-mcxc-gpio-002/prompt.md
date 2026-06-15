Write a bare-metal C application for NXP MCXC144 (Cortex-M0+) using the MCUXpresso SDK that detects a button press on PTC3 and toggles an LED on PTE24.

Requirements:
1. Configure PTC3 as a digital input with a falling-edge interrupt
2. Configure PTE24 as a digital output (LED)
3. In the interrupt handler, toggle the LED and clear the interrupt flag
4. The main loop does nothing (all logic in the ISR)

Use the MCUXpresso SDK (fsl_gpio.h, fsl_port.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Configure pins, clocks and peripherals with the SDK driver APIs within this file. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`).

Output ONLY the complete C source file.
