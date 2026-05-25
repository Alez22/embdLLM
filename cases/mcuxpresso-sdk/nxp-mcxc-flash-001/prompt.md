Write a bare-metal C application for NXP MCXC144 (Cortex-M0+) using the MCUXpresso SDK that erases a flash sector, writes 16 bytes of data to it, and verifies the write.

Requirements:
1. Target flash address: 0x1E000 (last sector of the 128KB flash, safe for application use)
2. Erase the sector before writing
3. Write the byte array {0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10}
4. Verify the written data matches the source
5. Indicate success or failure by toggling LED on PTE24 at different rates

Use the MCUXpresso SDK (fsl_flash.h).
Output ONLY the complete C source file.
