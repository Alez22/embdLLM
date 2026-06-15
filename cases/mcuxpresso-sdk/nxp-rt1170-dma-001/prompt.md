Write a bare-metal C application for NXP i.MX RT1170 (Cortex-M7) using the MCUXpresso SDK that copies a memory buffer using eDMA.

Requirements:
1. Copy a 512-byte source buffer to a destination buffer using eDMA channel 0 on DMA0, memory-to-memory
2. Fill the source buffer with the byte pattern (index & 0xFF) before the transfer
3. Wait for the transfer to complete
4. Compare destination and source; halt in an infinite loop on mismatch

Use the MCUXpresso SDK (fsl_edma.h).
Self-contained: include only MCUXpresso SDK driver headers (`fsl_*.h`) and CMSIS. Do not rely on config-tool-generated board files (`board.h`, `pin_mux.h`, `clock_config.h`, `fsl_debug_console.h`); configure pins, clocks and peripherals directly in code.

Output ONLY the complete C source file.
