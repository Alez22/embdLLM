Write a bare-metal C application for NXP i.MX RT1170 (Cortex-M7) using the MCUXpresso SDK that plays a continuous 1 kHz sine tone over I2S without blocking the main loop.

Audio output:
1. Use SAI1 in I2S mode as bit-clock and frame-sync master: pads GPIO_AD_21 (TX_DATA00), GPIO_AD_22 (TX_BCLK), GPIO_AD_23 (TX_SYNC)
2. 48 kHz sample rate, 16-bit, stereo (same signal on both channels)
3. Take samples from a lookup table with one period of the sine wave (48 samples per period at 48 kHz)

Architecture:
4. Feed the transmit FIFO from the SAI interrupt handler, not from the main loop
5. The main loop must stay free for other work (it may idle)

Use the MCUXpresso SDK (fsl_sai.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Configure pins, clocks and peripherals with the SDK driver APIs within this file. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`).

Output ONLY the complete C source file.
