#include <stdint.h>
#include <stdbool.h>
#include "fsl_common.h"
#include "fsl_iomuxc.h"
#include "fsl_clock.h"
#include "fsl_lpuart.h"

#define UART_BASE        LPUART1
#define UART_BAUDRATE    115200U
#define UART_CLOCK_FREQ  (CLOCK_GetRootClockFreq(kCLOCK_Root_Lpuart1))

int main(void)
{
    lpuart_config_t config;

    /* Clock root: 24 MHz oscillator is enough for 115200 baud.
       Mux/div indices: verify against the RT1170 clock tree. */
    clock_root_config_t uart_root_cfg = {0};
    uart_root_cfg.mux = 0U;
    uart_root_cfg.div = 1U;
    CLOCK_SetRootClock(kCLOCK_Root_Lpuart1, &uart_root_cfg);

    /* Pad mux: must precede peripheral init */
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_24_LPUART1_TXD, 0U);
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_25_LPUART1_RXD, 0U);

    LPUART_GetDefaultConfig(&config);
    config.baudRate_Bps = UART_BAUDRATE;
    /* Default config leaves both directions disabled */
    config.enableTx = true;
    config.enableRx = true;

    if (LPUART_Init(UART_BASE, &config, UART_CLOCK_FREQ) != kStatus_Success) {
        /* Requested baud rate not achievable from this clock root */
        while (1) {
        }
    }

    while (1) {
        uint8_t ch;
        LPUART_ReadBlocking(UART_BASE, &ch, 1U);
        LPUART_WriteBlocking(UART_BASE, &ch, 1U);
    }
}
