Write a bare-metal C application for NXP i.MX RT1170 (Cortex-M7) using the MCUXpresso SDK that plays a continuous 1 kHz sine tone through an external audio DAC over I2S.

Audio output:
1. Use SAI1 in I2S mode as bit-clock and frame-sync master: pads GPIO_AD_21 (TX_DATA00), GPIO_AD_22 (TX_BCLK), GPIO_AD_23 (TX_SYNC)
2. 48 kHz sample rate, 16-bit, stereo (same signal on both channels)
3. Stream one period of the sine wave from a lookup table (48 samples per period at 48 kHz) in an endless loop

DAC control interface (from the DAC datasheet — the device has no MCLK input and clocks itself from BCLK):
4. The DAC is controlled via I2C on LPI2C1, pads GPIO_AD_08 (SCL) and GPIO_AD_09 (SDA), 400 kHz, 7-bit address 0x18
5. Power-up sequence, one byte per register write: register 0x02 = 0x01 (DAC power on), register 0x04 = 0x00 (I2S slave, 16-bit), register 0x06 = 0x3F (output volume)

Use the MCUXpresso SDK (fsl_sai.h, fsl_lpi2c.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Configure pins, clocks and peripherals with the SDK driver APIs within this file. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`).

Output ONLY the complete C source file.
