#include "fsl_clock.h"
#include "fsl_port.h"
#include "fsl_gpio.h"

#define LED_PORT    PORTE
#define LED_GPIO    GPIOE
#define LED_PIN     24U

static void delay(volatile uint32_t count)
{
    while (count--) {
        __asm volatile("nop");
    }
}

int main(void)
{
    gpio_pin_config_t led_config = {
        .pinDirection = kGPIO_DigitalOutput,
        .outputLogic  = 0U,
    };

    /* Clock gate: must be enabled before any PORT/GPIO access */
    CLOCK_EnableClock(kCLOCK_PortE);

    /* Pin mux: must be configured before GPIO init */
    PORT_SetPinMux(LED_PORT, LED_PIN, kPORT_MuxAsGpio);

    GPIO_PinInit(LED_GPIO, LED_PIN, &led_config);

    while (1) {
        GPIO_PortToggle(LED_GPIO, 1U << LED_PIN);
        delay(500000U);
    }
}
