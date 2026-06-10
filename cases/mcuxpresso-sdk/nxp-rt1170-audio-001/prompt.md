Write a bare-metal C application for NXP i.MX RT1170 (Cortex-M7) using the MCUXpresso SDK that implements an audio pass-through (I2S in → I2S out).

Requirements:
1. SAI1 TX in I2S mode as bit-clock and frame-sync master, 48 kHz, 16-bit, stereo: pads GPIO_AD_21 (TX_DATA00), GPIO_AD_22 (TX_BCLK), GPIO_AD_23 (TX_SYNC)
2. SAI1 RX captures from an external ADC on pad GPIO_AD_17 (RX_DATA00), same format; on the board the ADC and the DAC are wired to the same bit clock and frame sync lines
3. In the main loop, read a small block of samples and immediately write it back out

Use the MCUXpresso SDK (fsl_sai.h).
Output ONLY the complete C source file.
