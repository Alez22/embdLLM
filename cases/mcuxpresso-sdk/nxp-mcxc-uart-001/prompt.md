Write a bare-metal C application for NXP MCXC144 (Cortex-M0+) using the MCUXpresso SDK that sends the string "Hello\r\n" over UART0 in a loop.

Requirements:
1. Use UART0 at 115200 baud, 8N1
2. Pins: PTA1 (RX), PTA2 (TX)
3. Transmit the string blocking in each iteration of the main loop
4. 1-second software delay between transmissions

Use the MCUXpresso SDK (fsl_uart.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Configure pins, clocks and peripherals with the SDK driver APIs within this file. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`).

Output ONLY the complete C source file.
