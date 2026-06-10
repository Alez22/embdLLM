Write a bare-metal C application for NXP i.MX RT1170 (Cortex-M7) using the MCUXpresso SDK that protects the main loop with a watchdog.

Requirements:
1. Use RTWDOG3 clocked from the 32.768 kHz low-power oscillator, 1 second timeout
2. The main loop performs some work (increment a counter) and then feeds the watchdog
3. If the loop stalls for any reason, the watchdog must reset the device
4. Do not disable the watchdog

Use the MCUXpresso SDK (fsl_rtwdog.h).
Output ONLY the complete C source file.
