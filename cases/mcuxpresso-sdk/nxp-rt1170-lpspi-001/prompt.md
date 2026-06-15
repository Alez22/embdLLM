Write a bare-metal C application for NXP i.MX RT1170 (Cortex-M7) using the MCUXpresso SDK that identifies an external SPI NOR flash chip.

Requirements:
1. Use LPSPI1 as master: pads GPIO_AD_28 (SCK), GPIO_AD_29 (PCS0), GPIO_AD_30 (SDO), GPIO_AD_31 (SDI)
2. 10 MHz clock, SPI mode 0, chip select on PCS0
3. Send the JEDEC ID command 0x9F and read the 3 ID bytes (manufacturer, type, capacity) into a buffer

Use the MCUXpresso SDK (fsl_lpspi.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`); configure pins, clocks and peripherals directly in code.

Output ONLY the complete C source file.
