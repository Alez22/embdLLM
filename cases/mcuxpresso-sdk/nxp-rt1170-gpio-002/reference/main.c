#include <stdint.h>
#include "fsl_common.h"
#include "fsl_iomuxc.h"
#include "fsl_gpio.h"

#define BTN_GPIO    GPIO13
#define BTN_PIN     0U
#define BTN_IRQ     GPIO13_Combined_0_31_IRQn

#define LED_GPIO    GPIO9
#define LED_PIN     3U

/* volatile: shared between ISR and main — never optimise away */
static volatile uint32_t g_btn_press_count = 0U;

void GPIO13_Combined_0_31_IRQHandler(void)
{
    /* Clear interrupt flag before any other action to avoid re-entry */
    GPIO_PortClearInterruptFlags(BTN_GPIO, 1U << BTN_PIN);

    GPIO_PortToggle(LED_GPIO, 1U << LED_PIN);
    g_btn_press_count++;
}

int main(void)
{
    gpio_pin_config_t btn_config = {
        .direction     = kGPIO_DigitalInput,
        .outputLogic   = 0U,
        .interruptMode = kGPIO_IntFallingEdge,
    };
    gpio_pin_config_t led_config = {
        .direction     = kGPIO_DigitalOutput,
        .outputLogic   = 0U,
        .interruptMode = kGPIO_NoIntmode,
    };

    /* Pad mux: WAKEUP pad to GPIO13_IO00 (verify macro against the part),
       LED pad to GPIO9_IO03. Must precede GPIO init. */
    IOMUXC_SetPinMux(IOMUXC_WAKEUP_DIG_GPIO13_IO00, 0U);
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_04_GPIO9_IO03, 0U);
    IOMUXC_SetPinConfig(IOMUXC_GPIO_AD_04_GPIO9_IO03, 0x02U);

    GPIO_PinInit(BTN_GPIO, BTN_PIN, &btn_config);
    GPIO_PinInit(LED_GPIO, LED_PIN, &led_config);

    /* IGPIO needs an explicit interrupt-enable step after init —
       interruptMode in the config alone does not unmask the pin */
    GPIO_PortEnableInterrupts(BTN_GPIO, 1U << BTN_PIN);
    EnableIRQ(BTN_IRQ);

    while (1) {
        /* All work done in ISR */
        __asm volatile("wfi");
    }
}
