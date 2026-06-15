Write a bare-metal C application for NXP i.MX RT1170 (Cortex-M7) using the MCUXpresso SDK that reads the WHO_AM_I register from an I2C sensor.

Requirements:
1. Use LPI2C1, pads GPIO_AD_08 (SCL) and GPIO_AD_09 (SDA), at 400 kHz
2. Read register 0x75 from the sensor at 7-bit address 0x68
3. Store the result in a variable

Use the MCUXpresso SDK (fsl_lpi2c.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Configure pins, clocks and peripherals with the SDK driver APIs within this file. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`).

Output ONLY the complete C source file.
