Write a bare-metal C application for NXP MCXC144 (Cortex-M0+) using the MCUXpresso SDK that stores a 12-byte configuration record in flash safely against power loss.

Requirements:
1. The configuration record is a struct with a uint32_t magic, uint64_t data, and uint32_t crc
2. Use flash address 0x1E000 as the primary slot and 0x1E400 as the backup slot
3. On boot: validate both slots by checking magic (0xDEADBEEF) and CRC32; load the valid one
4. On write: write-then-validate pattern — write to the inactive slot first, verify CRC after write, then update the primary slot
5. If both slots are corrupt on boot, initialize with default values

Use the MCUXpresso SDK (fsl_flash.h). Implement a simple CRC32 without external libraries.
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Configure pins, clocks and peripherals with the SDK driver APIs within this file. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`).

Output ONLY the complete C source file.
