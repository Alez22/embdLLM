Write a bare-metal C application for NXP MCXC144 (Cortex-M0+) using the MCUXpresso SDK that sends a 2-byte command over SPI0 to an external device.

Requirements:
1. Use SPI0 in master mode, CPOL=0 CPHA=0, 1 MHz, 8-bit frame
2. Pins: PTC6 (SCK), PTC7 (MOSI), PTC4 (MISO), PTC5 (manual CS via GPIO)
3. Assert CS low before transfer, deassert high after
4. Send the bytes {0x9F, 0x00} and store the 2 received bytes

Use the MCUXpresso SDK (fsl_spi.h, fsl_gpio.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`); configure pins, clocks and peripherals directly in code.

Output ONLY the complete C source file.
