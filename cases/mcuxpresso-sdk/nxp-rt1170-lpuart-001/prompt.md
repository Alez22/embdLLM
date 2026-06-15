Write a bare-metal C application for NXP i.MX RT1170 (Cortex-M7) using the MCUXpresso SDK that echoes serial input.

Requirements:
1. Use LPUART1: pads GPIO_AD_24 (TX) and GPIO_AD_25 (RX)
2. 115200 baud, 8 data bits, no parity, 1 stop bit
3. In the main loop, read one byte at a time and write it back immediately

Use the MCUXpresso SDK (fsl_lpuart.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Configure pins, clocks and peripherals with the SDK driver APIs within this file. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`).

Output ONLY the complete C source file.
