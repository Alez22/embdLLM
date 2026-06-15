Write a bare-metal C application for NXP i.MX RT1170 (Cortex-M7) using the MCUXpresso SDK that blinks an LED.

Requirements:
1. LED on GPIO9 pin 3, pad GPIO_AD_04
2. LED off at startup
3. Toggle the LED roughly every 500 ms using a software delay loop

Use the MCUXpresso SDK (fsl_gpio.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Configure pins, clocks and peripherals with the SDK driver APIs within this file. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`).

Output ONLY the complete C source file.
