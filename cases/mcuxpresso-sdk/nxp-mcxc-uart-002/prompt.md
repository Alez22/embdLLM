Write a bare-metal C application for NXP MCXC144 (Cortex-M0+) using the MCUXpresso SDK that receives bytes over UART0 using interrupts and stores them in a ring buffer.

Requirements:
1. Use UART0 at 115200 baud, 8N1, pins PTA1 (RX) and PTA2 (TX)
2. Enable the UART RX interrupt; accumulate received bytes in a 64-byte ring buffer
3. In main, when a complete line (terminated by '\n') is available in the buffer, echo it back over UART TX
4. Ring buffer must be safe for use between the ISR and main

Use the MCUXpresso SDK (fsl_uart.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Configure pins, clocks and peripherals with the SDK driver APIs within this file. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`).

Output ONLY the complete C source file.
