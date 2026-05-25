Write a bare-metal C application for NXP MCXC144 (Cortex-M0+) using the MCUXpresso SDK that reads the WHO_AM_I register from an I2C sensor.

Requirements:
1. Use I2C0, pins PTC8 (SCL) and PTC9 (SDA), at 100 kHz
2. Read register 0x75 from the sensor at 7-bit address 0x68
3. Store the result in a variable
4. Handle communication errors

Use the MCUXpresso SDK (fsl_i2c.h).
Output ONLY the complete C source file.
