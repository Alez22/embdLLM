#include <stdint.h>
#include "fsl_common.h"
#include "fsl_clock.h"
#include "fsl_gpt.h"

#define TICK_GPT       GPT1
#define TICK_GPT_IRQ   GPT1_IRQn
#define TICK_GPT_FREQ  (CLOCK_GetRootClockFreq(kCLOCK_Root_Gpt1))

/* volatile: shared between ISR and main — never optimise away */
static volatile uint32_t g_ms_ticks = 0U;

void GPT1_IRQHandler(void)
{
    /* Clear the compare flag first to avoid immediate re-entry */
    GPT_ClearStatusFlags(TICK_GPT, kGPT_OutputCompare1Flag);
    g_ms_ticks++;
}

int main(void)
{
    gpt_config_t config;

    /* Clock root: 24 MHz oscillator, divide-by-1.
       Mux/div indices: verify against the RT1170 clock tree. */
    clock_root_config_t gpt_root_cfg = {0};
    gpt_root_cfg.mux = 0U;
    gpt_root_cfg.div = 1U;
    CLOCK_SetRootClock(kCLOCK_Root_Gpt1, &gpt_root_cfg);

    /* Default config: restart mode — counter resets on channel 1 match,
       which is exactly what a periodic tick needs */
    GPT_GetDefaultConfig(&config);
    GPT_Init(TICK_GPT, &config);

    /* 1 ms period: compare value counts from zero, hence the -1 */
    GPT_SetOutputCompareValue(TICK_GPT, kGPT_OutputCompare_Channel1,
                              (TICK_GPT_FREQ / 1000U) - 1U);
    GPT_EnableInterrupts(TICK_GPT, kGPT_OutputCompare1InterruptEnable);

    EnableIRQ(TICK_GPT_IRQ);
    GPT_StartTimer(TICK_GPT);

    while (1) {
        __asm volatile("wfi");
    }
}
