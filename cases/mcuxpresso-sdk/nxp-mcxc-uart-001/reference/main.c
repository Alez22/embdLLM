#include <stdint.h>
#include <string.h>
#include "fsl_clock.h"
#include "fsl_port.h"
#include "fsl_uart.h"

#define UART_BASE       UART0
#define UART_CLK_FREQ   (CLOCK_GetFreq(kCLOCK_CoreSysClk))
#define UART_BAUDRATE   115200U

static const uint8_t s_msg[] = "Hello\r\n";

static void delay_ms(uint32_t ms)
{
    /* Approximate: assumes ~48 MHz core, adjust if needed */
    volatile uint32_t i;
    for (; ms > 0U; ms--) {
        for (i = 0U; i < 6000U; i++) {
            __asm volatile("nop");
        }
    }
}

int main(void)
{
    uart_config_t config;

    /* Clock gate: must be enabled before PORT and UART access */
    CLOCK_EnableClock(kCLOCK_PortA);
    CLOCK_EnableClock(kCLOCK_Uart0);

    /* Pin mux: alternate function for UART0 TX/RX */
    PORT_SetPinMux(PORTA, 1U, kPORT_MuxAlt2);   /* PTA1 = UART0_RX */
    PORT_SetPinMux(PORTA, 2U, kPORT_MuxAlt2);   /* PTA2 = UART0_TX */

    UART_GetDefaultConfig(&config);
    config.baudRate_Bps = UART_BAUDRATE;
    config.enableTx     = true;
    config.enableRx     = false;
    UART_Init(UART_BASE, &config, UART_CLK_FREQ);

    while (1) {
        UART_WriteBlocking(UART_BASE, s_msg, strlen((const char *)s_msg));
        delay_ms(1000U);
    }
}
