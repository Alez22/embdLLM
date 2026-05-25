#include <stdint.h>
#include <stdbool.h>
#include "fsl_clock.h"
#include "fsl_port.h"
#include "fsl_gpio.h"
#include "fsl_pit.h"

#define PIT_CH          kPIT_Chnl_0
#define BUS_CLK_HZ      48000000U
#define PIT_PERIOD_MS   10U

#define INPUT_GPIO      GPIOC
#define INPUT_PORT      PORTC
#define INPUT_PIN       3U

#define LED_GPIO        GPIOE
#define LED_PORT        PORTE
#define LED_PIN         24U

/* ISR writes, main reads — both fields volatile to prevent optimisation */
static volatile bool     g_sample_ready = false;
static volatile uint32_t g_sample_value = 0U;

void PIT_IRQHandler(void)
{
    PIT_ClearStatusFlags(PIT, PIT_CH, kPIT_TimerFlag);

    /* Read input and store atomically — uint32_t write is atomic on Cortex-M0+ */
    g_sample_value = GPIO_PinRead(INPUT_GPIO, INPUT_PIN);
    /* Set ready flag last so main never sees stale data */
    g_sample_ready = true;
}

int main(void)
{
    pit_config_t    pit_cfg;
    gpio_pin_config_t input_cfg = { .pinDirection = kGPIO_DigitalInput,  .outputLogic = 0U };
    gpio_pin_config_t led_cfg   = { .pinDirection = kGPIO_DigitalOutput, .outputLogic = 0U };

    /* Clock gates */
    CLOCK_EnableClock(kCLOCK_PortC);
    CLOCK_EnableClock(kCLOCK_PortE);
    CLOCK_EnableClock(kCLOCK_Pit0);

    /* Pin mux */
    PORT_SetPinMux(INPUT_PORT, INPUT_PIN, kPORT_MuxAsGpio);
    PORT_SetPinMux(LED_PORT,   LED_PIN,   kPORT_MuxAsGpio);

    GPIO_PinInit(INPUT_GPIO, INPUT_PIN, &input_cfg);
    GPIO_PinInit(LED_GPIO,   LED_PIN,   &led_cfg);

    /* PIT */
    PIT_GetDefaultConfig(&pit_cfg);
    PIT_Init(PIT, &pit_cfg);
    PIT_SetTimerPeriod(PIT, PIT_CH,
        USEC_TO_COUNT(PIT_PERIOD_MS * 1000U, BUS_CLK_HZ));
    PIT_EnableInterrupts(PIT, PIT_CH, kPIT_TimerInterruptEnable);
    EnableIRQ(PIT_IRQn);
    PIT_StartTimer(PIT, PIT_CH);

    while (1) {
        if (g_sample_ready) {
            /* Clear flag before reading value to avoid missing the next sample */
            g_sample_ready = false;
            if (g_sample_value) {
                GPIO_PortToggle(LED_GPIO, 1U << LED_PIN);
            }
        }
    }
}
