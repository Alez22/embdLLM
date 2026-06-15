Write a bare-metal C application for NXP MCXC144 (Cortex-M0+) using the MCUXpresso SDK that configures the COP (Computer Operating Properly) watchdog and feeds it in the main loop.

Requirements:
1. Configure the COP with the longest available timeout and LPO clock source
2. The main loop performs some work (increment a counter) and then feeds the watchdog
3. If the loop stalls for any reason, the watchdog must reset the device
4. Do not disable the watchdog

Use the MCUXpresso SDK (fsl_cop.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`); configure pins, clocks and peripherals directly in code.

Output ONLY the complete C source file.
