#include <stdint.h>
#include <string.h>
#include "fsl_common.h"
#include "fsl_iomuxc.h"
#include "fsl_clock.h"
#include "fsl_lpspi.h"

#define FLASH_SPI          LPSPI1
#define SPI_BAUDRATE       10000000U
#define SPI_CLOCK_FREQ     (CLOCK_GetRootClockFreq(kCLOCK_Root_Lpspi1))
#define CMD_READ_JEDEC_ID  0x9FU

int main(void)
{
    lpspi_master_config_t config;
    lpspi_transfer_t xfer;
    uint8_t tx_buf[4] = {CMD_READ_JEDEC_ID, 0U, 0U, 0U};
    uint8_t rx_buf[4] = {0U};

    /* Clock root: 24 MHz oscillator is not enough for 10 MHz SCK with
       margin; use a PLL-derived root. Mux/div indices: verify against
       the RT1170 clock tree. */
    clock_root_config_t spi_root_cfg = {0};
    spi_root_cfg.mux = 1U;
    spi_root_cfg.div = 5U;
    CLOCK_SetRootClock(kCLOCK_Root_Lpspi1, &spi_root_cfg);

    /* Pad mux: must precede peripheral init */
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_28_LPSPI1_SCK, 0U);
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_29_LPSPI1_PCS0, 0U);
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_30_LPSPI1_SOUT, 0U);
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_31_LPSPI1_SIN, 0U);

    /* Mode 0 = CPOL 0, CPHA 0 — the SDK default; set explicitly anyway */
    LPSPI_MasterGetDefaultConfig(&config);
    config.baudRate = SPI_BAUDRATE;
    config.cpol     = kLPSPI_ClockPolarityActiveHigh;
    config.cpha     = kLPSPI_ClockPhaseFirstEdge;
    config.whichPcs = kLPSPI_Pcs0;
    LPSPI_MasterInit(FLASH_SPI, &config, SPI_CLOCK_FREQ);

    memset(&xfer, 0, sizeof(xfer));
    xfer.txData   = tx_buf;
    xfer.rxData   = rx_buf;
    xfer.dataSize = sizeof(tx_buf);
    /* PCS must stay asserted across command + ID bytes: a per-byte
       PCS toggle would abort the JEDEC read after the opcode */
    xfer.configFlags = kLPSPI_MasterPcs0 | kLPSPI_MasterPcsContinuous;

    if (LPSPI_MasterTransferBlocking(FLASH_SPI, &xfer) != kStatus_Success) {
        /* Bus error: stop here rather than report a bogus ID */
        while (1) {
        }
    }

    /* rx_buf[1..3] now hold manufacturer, type, capacity */
    while (1) {
        __asm volatile("wfi");
    }
}
