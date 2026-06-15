Write a bare-metal C application for NXP i.MX RT1170 (Cortex-M7) using the MCUXpresso SDK that toggles an LED on each button press.

Requirements:
1. Button on GPIO13 pin 0, pad WAKEUP (active low, external pull-up present)
2. LED on GPIO9 pin 3, pad GPIO_AD_04
3. Toggle the LED on each falling edge of the button, using an interrupt (no polling)
4. Count the number of presses in a variable

Use the MCUXpresso SDK (fsl_gpio.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Configure pins, clocks and peripherals with the SDK driver APIs within this file. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`).

Output ONLY the complete C source file.
