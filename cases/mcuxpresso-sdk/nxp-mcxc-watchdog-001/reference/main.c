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

    /* COP runs off LPO (1 kHz) — independent of core clock for reliability */
    COP_GetDefaultConfig(&cop_cfg);
    cop_cfg.enableCop      = true;
    cop_cfg.clockSource    = kCOP_LpoClock;
    cop_cfg.timeout        = kCOP_Timeout_2Power18LpoClock;  /* longest timeout */
    cop_cfg.enableStop     = false;
    cop_cfg.enableDebug    = false;
    COP_Init(SIM, &cop_cfg);

    while (1) {
        do_work();

        /* Feed watchdog — must be done within the timeout window */
        COP_Refresh(SIM);
    }
}
