#include <stdint.h>
#include "fsl_common.h"
#include "fsl_clock.h"
#include "fsl_gpt.h"

#define UPTIME_GPT       GPT2
#define UPTIME_GPT_IRQ   GPT2_IRQn
#define UPTIME_GPT_FREQ  (CLOCK_GetRootClockFreq(kCLOCK_Root_Gpt2))

/* volatile: shared between ISR and main — never optimise away */
static volatile uint64_t g_uptime_ms = 0U;

void GPT2_IRQHandler(void)
{
    /* Clear the compare flag first to avoid immediate re-entry */
    GPT_ClearStatusFlags(UPTIME_GPT, kGPT_OutputCompare1Flag);
    g_uptime_ms++;
}

uint64_t uptime_ms(void)
{
    /* A 64-bit load on Cortex-M is two 32-bit reads: the ISR could fire
       between them and tear the value. Read inside a critical section. */
    uint32_t primask = DisableGlobalIRQ();
    uint64_t now = g_uptime_ms;
    EnableGlobalIRQ(primask);
    return now;
}

int main(void)
{
    gpt_config_t config;

    /* Clock root: 24 MHz oscillator, divide-by-1.
       Mux/div indices: verify against the RT1170 clock tree. */
    clock_root_config_t gpt_root_cfg = {0};
    gpt_root_cfg.mux = 0U;
    gpt_root_cfg.div = 1U;
    CLOCK_SetRootClock(kCLOCK_Root_Gpt2, &gpt_root_cfg);

    /* Default config: restart mode — counter resets on channel 1 match */
    GPT_GetDefaultConfig(&config);
    GPT_Init(UPTIME_GPT, &config);

    /* 1 ms period: compare value counts from zero, hence the -1 */
    GPT_SetOutputCompareValue(UPTIME_GPT, kGPT_OutputCompare_Channel1,
                              (UPTIME_GPT_FREQ / 1000U) - 1U);
    GPT_EnableInterrupts(UPTIME_GPT, kGPT_OutputCompare1InterruptEnable);

    EnableIRQ(UPTIME_GPT_IRQ);
    GPT_StartTimer(UPTIME_GPT);

    while (1) {
        uint64_t now = uptime_ms();
        (void)now;
        __asm volatile("wfi");
    }
}
