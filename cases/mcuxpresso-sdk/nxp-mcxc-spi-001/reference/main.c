#include "fsl_clock.h"
#include "fsl_port.h"
#include "fsl_spi.h"
#include "fsl_gpio.h"

#define SPI_BASE        SPI0
#define SPI_CLK_FREQ    (CLOCK_GetFreq(kCLOCK_BusClk))
#define SPI_BAUDRATE    1000000U

#define CS_PORT         PORTC
#define CS_GPIO         GPIOC
#define CS_PIN          5U

static uint8_t s_tx_buf[2] = {0x9FU, 0x00U};
static uint8_t s_rx_buf[2] = {0};

static inline void cs_assert(void)   { GPIO_PinWrite(CS_GPIO, CS_PIN, 0U); }
static inline void cs_deassert(void) { GPIO_PinWrite(CS_GPIO, CS_PIN, 1U); }

int main(void)
{
    spi_master_config_t spi_config;
    spi_transfer_t      transfer;
    gpio_pin_config_t   cs_cfg = {
        .pinDirection = kGPIO_DigitalOutput,
        .outputLogic  = 1U,   /* CS idle high */
    };

    /* Clock gates: must be enabled before any PORT/SPI access */
    CLOCK_EnableClock(kCLOCK_PortC);
    CLOCK_EnableClock(kCLOCK_Spi0);

    /* Pin mux: SPI alternate function for SCK, MOSI, MISO */
    PORT_SetPinMux(CS_PORT,  CS_PIN,  kPORT_MuxAsGpio);   /* CS: GPIO */
    PORT_SetPinMux(PORTC,    6U,      kPORT_MuxAlt2);      /* SCK  */
    PORT_SetPinMux(PORTC,    7U,      kPORT_MuxAlt2);      /* MOSI */
    PORT_SetPinMux(PORTC,    4U,      kPORT_MuxAlt2);      /* MISO */

    GPIO_PinInit(CS_GPIO, CS_PIN, &cs_cfg);

    SPI_MasterGetDefaultConfig(&spi_config);
    spi_config.baudRate_Bps          = SPI_BAUDRATE;
    spi_config.polarity              = kSPI_ClockPolarityActiveHigh;  /* CPOL=0 */
    spi_config.phase                 = kSPI_ClockPhaseFirstEdge;      /* CPHA=0 */
    spi_config.direction             = kSPI_MsbFirst;
    spi_config.outputMode            = kSPI_SlaveSelectAsGpio;  /* manual CS */
    SPI_MasterInit(SPI_BASE, &spi_config, SPI_CLK_FREQ);

    /* Transfer: assert CS before, deassert after — SDK does NOT do this */
    cs_assert();
    transfer.txData   = s_tx_buf;
    transfer.rxData   = s_rx_buf;
    transfer.dataSize = sizeof(s_tx_buf);
    SPI_MasterTransferBlocking(SPI_BASE, &transfer);
    cs_deassert();

    while (1);
}
