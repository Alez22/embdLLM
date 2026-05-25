#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "fsl_clock.h"
#include "fsl_port.h"
#include "fsl_uart.h"

#define UART_BASE       UART0
#define UART_CLK_FREQ   (CLOCK_GetFreq(kCLOCK_CoreSysClk))
#define UART_BAUDRATE   115200U
#define RX_BUF_SIZE     64U

/* Ring buffer — head/tail accessed from both ISR and main */
static volatile uint8_t  s_rx_buf[RX_BUF_SIZE];
static volatile uint32_t s_rx_head = 0U;
static volatile uint32_t s_rx_tail = 0U;

static inline bool ring_empty(void)
{
    return s_rx_head == s_rx_tail;
}

static inline bool ring_full(void)
{
    return ((s_rx_head + 1U) % RX_BUF_SIZE) == s_rx_tail;
}

static inline void ring_push(uint8_t byte)
{
    if (!ring_full()) {
        s_rx_buf[s_rx_head] = byte;
        s_rx_head = (s_rx_head + 1U) % RX_BUF_SIZE;
    }
}

static inline uint8_t ring_pop(void)
{
    uint8_t b = s_rx_buf[s_rx_tail];
    s_rx_tail = (s_rx_tail + 1U) % RX_BUF_SIZE;
    return b;
}

void UART0_IRQHandler(void)
{
    /* Check RX data register full flag */
    if (UART_GetStatusFlags(UART_BASE) & kUART_RxDataRegFullFlag) {
        ring_push(UART_ReadByte(UART_BASE));
    }
}

int main(void)
{
    uart_config_t config;
    uint8_t       line_buf[RX_BUF_SIZE];
    uint32_t      line_len = 0U;

    /* Clock gate: must be enabled before PORT and UART access */
    CLOCK_EnableClock(kCLOCK_PortA);
    CLOCK_EnableClock(kCLOCK_Uart0);

    /* Pin mux: alternate function for UART0 TX/RX */
    PORT_SetPinMux(PORTA, 1U, kPORT_MuxAlt2);   /* PTA1 = UART0_RX */
    PORT_SetPinMux(PORTA, 2U, kPORT_MuxAlt2);   /* PTA2 = UART0_TX */

    UART_GetDefaultConfig(&config);
    config.baudRate_Bps = UART_BAUDRATE;
    config.enableTx     = true;
    config.enableRx     = true;
    UART_Init(UART_BASE, &config, UART_CLK_FREQ);

    /* Enable RX interrupt in UART and NVIC */
    UART_EnableInterrupts(UART_BASE, kUART_RxDataRegFullInterruptEnable);
    EnableIRQ(UART0_IRQn);

    while (1) {
        while (!ring_empty()) {
            uint8_t b = ring_pop();
            if (line_len < (RX_BUF_SIZE - 1U)) {
                line_buf[line_len++] = b;
            }
            if (b == '\n') {
                UART_WriteBlocking(UART_BASE, line_buf, line_len);
                line_len = 0U;
            }
        }
    }
}
