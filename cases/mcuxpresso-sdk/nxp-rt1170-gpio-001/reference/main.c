#include <stdint.h>
#include "fsl_common.h"
#include "fsl_iomuxc.h"
#include "fsl_gpio.h"

#define LED_GPIO    GPIO9
#define LED_PIN     3U

static void delay(volatile uint32_t count)
{
    while (count--) {
        __asm volatile("nop");
    }
}

int main(void)
{
    /* i.MX RT igpio config: 'direction' field, not Kinetis 'pinDirection' */
    gpio_pin_config_t led_config = {
        .direction     = kGPIO_DigitalOutput,
        .outputLogic   = 0U,
        .interruptMode = kGPIO_NoIntmode,
    };

    /* Pad mux + electrical config: must precede GPIO init.
       On RT1170 pads are routed via IOMUXC, not the Kinetis PORT module. */
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_04_GPIO9_IO03, 0U);
    IOMUXC_SetPinConfig(IOMUXC_GPIO_AD_04_GPIO9_IO03, 0x02U);

    GPIO_PinInit(LED_GPIO, LED_PIN, &led_config);

    while (1) {
        GPIO_PortToggle(LED_GPIO, 1U << LED_PIN);
        delay(5000000U);
    }
}
