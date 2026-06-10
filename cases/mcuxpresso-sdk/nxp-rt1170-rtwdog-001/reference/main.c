#include <stdint.h>
#include "fsl_common.h"
#include "fsl_rtwdog.h"

#define WDT_BASE           RTWDOG3
/* LPO runs at 32.768 kHz: 1 s timeout in clock ticks */
#define WDT_TIMEOUT_TICKS  32768U

int main(void)
{
    rtwdog_config_t config;
    uint32_t work_counter = 0U;

    /* Default config: LPO clock source, prescaler /1, watchdog enabled.
       The SDK performs the unlock sequence inside RTWDOG_Init. */
    RTWDOG_GetDefaultConfig(&config);
    config.timeoutValue = (uint16_t)(WDT_TIMEOUT_TICKS - 1U);
    RTWDOG_Init(WDT_BASE, &config);

    while (1) {
        work_counter++;
        /* Feed last, after the work: a stall anywhere above starves it */
        RTWDOG_Refresh(WDT_BASE);
    }
}
