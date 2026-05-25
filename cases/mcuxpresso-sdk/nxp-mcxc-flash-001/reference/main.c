#include <stdint.h>
#include <string.h>
#include "fsl_clock.h"
#include "fsl_port.h"
#include "fsl_gpio.h"
#include "fsl_flash.h"

#define FLASH_TARGET_ADDR   0x1E000U
#define FLASH_SECTOR_SIZE   1024U       /* MCXC144: 1 KB sectors */

#define LED_PORT    PORTE
#define LED_GPIO    GPIOE
#define LED_PIN     24U

static const uint8_t s_data[16] = {
    0x01U, 0x02U, 0x03U, 0x04U, 0x05U, 0x06U, 0x07U, 0x08U,
    0x09U, 0x0AU, 0x0BU, 0x0CU, 0x0DU, 0x0EU, 0x0FU, 0x10U,
};

static void delay(volatile uint32_t n) { while (n--) { __asm volatile("nop"); } }

static void blink_forever(uint32_t period_fast)
{
    while (1) {
        GPIO_PortToggle(LED_GPIO, 1U << LED_PIN);
        delay(period_fast);
    }
}

int main(void)
{
    flash_config_t flash_cfg;
    status_t       status;
    uint32_t       fail_addr, fail_data, fail_expected;
    gpio_pin_config_t led_cfg = { .pinDirection = kGPIO_DigitalOutput, .outputLogic = 0U };

    /* Clock gate and LED init */
    CLOCK_EnableClock(kCLOCK_PortE);
    PORT_SetPinMux(LED_PORT, LED_PIN, kPORT_MuxAsGpio);
    GPIO_PinInit(LED_GPIO, LED_PIN, &led_cfg);

    /* Flash init — must be called before any flash operation */
    memset(&flash_cfg, 0, sizeof(flash_cfg));
    status = FLASH_Init(&flash_cfg);
    if (status != kStatus_Success) {
        blink_forever(50000U);  /* fast blink = init error */
    }

    /* Erase sector: must be done before write — flash bits can only go 1→0 */
    status = FLASH_EraseSector(&flash_cfg, FLASH_TARGET_ADDR, FLASH_SECTOR_SIZE,
                               kFLASH_ApiEraseKey);
    if (status != kStatus_Success) {
        blink_forever(100000U);  /* medium blink = erase error */
    }

    /* Write: minimum write unit on MCXC144 is 4 bytes (longword) */
    status = FLASH_Program(&flash_cfg, FLASH_TARGET_ADDR,
                           (uint32_t *)s_data, sizeof(s_data));
    if (status != kStatus_Success) {
        blink_forever(200000U);  /* slow blink = write error */
    }

    /* Verify written data matches source */
    status = FLASH_VerifyProgram(&flash_cfg, FLASH_TARGET_ADDR, sizeof(s_data),
                                 (const uint32_t *)s_data,
                                 kFLASH_MarginValueNormal,
                                 &fail_addr, &fail_data);
    (void)fail_addr;
    (void)fail_data;
    (void)fail_expected;

    if (status != kStatus_Success) {
        blink_forever(300000U);  /* very slow blink = verify error */
    }

    /* Success: steady on */
    GPIO_PinWrite(LED_GPIO, LED_PIN, 1U);
    while (1);
}
