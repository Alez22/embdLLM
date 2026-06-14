#include <stdint.h>
#include "fsl_cop.h"
#include "fsl_clock.h"

static volatile uint32_t g_counter = 0U;

static void do_work(void)
{
    g_counter++;
}

int main(void)
{
    cop_config_t cop_cfg;

    /* COP runs off LPO (1 kHz) — independent of core clock for reliability.
     * Longest available timeout = long mode + the 2^18-cycle setting. */
    COP_GetDefaultConfig(&cop_cfg);
    cop_cfg.clockSource    = kCOP_LpoClock;
    cop_cfg.timeoutMode    = kCOP_LongTimeoutMode;
    cop_cfg.timeoutCycles  = kCOP_2Power10CyclesOr2Power18Cycles;  /* longest */
    cop_cfg.enableStop     = false;
    cop_cfg.enableDebug    = false;
    COP_Init(SIM, &cop_cfg);

    while (1) {
        do_work();

        /* Feed watchdog — must be done within the timeout window */
        COP_Refresh(SIM);
    }
}
