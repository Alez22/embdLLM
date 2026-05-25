#include "fsl_clock.h"
#include "fsl_port.h"
#include "fsl_gpio.h"

#define BTN_PORT    PORTC
#define BTN_GPIO    GPIOC
#define BTN_PIN     3U
#define BTN_IRQ     PORTC_PORTD_IRQn

#define LED_PORT    PORTE
#define LED_GPIO    GPIOE
#define LED_PIN     24U

/* volatile: shared between ISR and main — never optimise away */
static volatile uint32_t g_btn_press_count = 0;

void PORTC_PORTD_IRQHandler(void)
{
    /* Clear interrupt flag before any other action to avoid re-entry */
    GPIO_PortClearInterruptFlags(BTN_GPIO, 1U << BTN_PIN);

    GPIO_PortToggle(LED_GPIO, 1U << LED_PIN);
    g_btn_press_count++;
}

int main(void)
{
    gpio_pin_config_t btn_config = {
        .pinDirection = kGPIO_DigitalInput,
        .outputLogic  = 0U,
    };
    gpio_pin_config_t led_config = {
        .pinDirection = kGPIO_DigitalOutput,
        .outputLogic  = 0U,
    };

    /* Clock gates: must be enabled before any PORT/GPIO access */
    CLOCK_EnableClock(kCLOCK_PortC);
    CLOCK_EnableClock(kCLOCK_PortE);

    /* Button pin mux: GPIO function + falling-edge interrupt */
    PORT_SetPinMux(BTN_PORT, BTN_PIN, kPORT_MuxAsGpio);
    PORT_SetPinInterruptConfig(BTN_PORT, BTN_PIN, kPORT_InterruptFallingEdge);

    /* LED pin mux: GPIO function */
    PORT_SetPinMux(LED_PORT, LED_PIN, kPORT_MuxAsGpio);

    GPIO_PinInit(BTN_GPIO, BTN_PIN, &btn_config);
    GPIO_PinInit(LED_GPIO, LED_PIN, &led_config);

    /* Enable PORT interrupt in NVIC — implicit: prompt never mentions this */
    EnableIRQ(BTN_IRQ);

    while (1) {
        /* All work done in ISR */
        __asm volatile("wfi");
    }
}
