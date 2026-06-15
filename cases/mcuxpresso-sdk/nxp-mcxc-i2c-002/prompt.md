Write a bare-metal C application for NXP MCXC144 (Cortex-M0+) using the MCUXpresso SDK that configures a sensor over I2C: first write a configuration byte to register 0x1A, then immediately read it back to verify.

Requirements:
1. Use I2C0, pins PTC8 (SCL) and PTC9 (SDA), at 400 kHz
2. Sensor 7-bit address: 0x68
3. Write 0x06 to register 0x1A
4. Read back the value from register 0x1A and store it in a variable
5. The write and the read-back must be two separate transfers
6. Check return values and halt on error

Use the MCUXpresso SDK (fsl_i2c.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`); configure pins, clocks and peripherals directly in code.

Output ONLY the complete C source file.
