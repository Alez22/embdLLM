#include <stdint.h>
#include <stdio.h>
#include "fsl_clock.h"
#include "fsl_port.h"
#include "fsl_pit.h"
#include "fsl_uart.h"

#define PIT_CH          kPIT_Chnl_0
#define BUS_CLK_HZ      48000000U
#define PIT_PERIOD_MS   100U

#define UART_BASE       UART2
#define UART_CLK_FREQ   (CLOCK_GetFreq(kCLOCK_CoreSysClk))
#define UART_BAUDRATE   115200U

/* volatile: written in ISR, read in main */
static volatile uint32_t g_tick_count = 0U;

void PIT_IRQHandler(void)
{
    /* Clear interrupt flag before any other action */
    PIT_ClearStatusFlags(PIT, PIT_CH, kPIT_TimerFlag);
    g_tick_count++;
}

int main(void)
{
    pit_config_t    pit_cfg;
    uart_config_t   uart_cfg;
    char            buf[32];
    uint32_t        last_print = 0U;

    /* Clock gates */
    CLOCK_EnableClock(kCLOCK_Pit0);
    CLOCK_EnableClock(kCLOCK_PortA);
    CLOCK_EnableClock(kCLOCK_Uart2);

    /* UART: TX only on PTA2 */
    PORT_SetPinMux(PORTA, 2U, kPORT_MuxAlt2);
    UART_GetDefaultConfig(&uart_cfg);
    uart_cfg.baudRate_Bps = UART_BAUDRATE;
    uart_cfg.enableTx     = true;
    UART_Init(UART_BASE, &uart_cfg, UART_CLK_FREQ);

    /* PIT init */
    PIT_GetDefaultConfig(&pit_cfg);
    pit_cfg.enableRunInDebug = false;
    PIT_Init(PIT, &pit_cfg);

    /* Period = bus_clk * period_ms / 1000 - 1 */
    PIT_SetTimerPeriod(PIT, PIT_CH,
        USEC_TO_COUNT(PIT_PERIOD_MS * 1000U, BUS_CLK_HZ));

    PIT_EnableInterrupts(PIT, PIT_CH, kPIT_TimerInterruptEnable);
    EnableIRQ(PIT_IRQn);
    PIT_StartTimer(PIT, PIT_CH);

    while (1) {
        uint32_t now = g_tick_count;
        /* Print every 10 ticks = 1 second */
        if ((now - last_print) >= 10U) {
            last_print = now;
            int len = snprintf(buf, sizeof(buf), "tick=%lu\r\n",
                               (unsigned long)now);
            if (len > 0) {
                UART_WriteBlocking(UART_BASE, (uint8_t *)buf, (uint32_t)len);
            }
        }
    }
}
