#include <stdint.h>
#include "fsl_common.h"
#include "fsl_iomuxc.h"
#include "fsl_clock.h"
#include "fsl_sai.h"

#define SAI_BASE        SAI1
#define SAI_IRQ         SAI1_IRQn
#define SAMPLE_RATE_HZ  48000U
#define BIT_WIDTH       16U
#define SAI_CLOCK_FREQ  (CLOCK_GetRootClockFreq(kCLOCK_Root_Sai1))

#define SINE_SAMPLES    48U              /* one 1 kHz period at 48 kHz */

/* One period of a 1 kHz sine, 16-bit signed, ~ -0.2 dBFS */
static const int16_t s_sine_table[SINE_SAMPLES] = {
         0,   3916,   7765,  11480,  15000,  18263,  21213,  23801,
     25981,  27716,  28978,  29743,  30000,  29743,  28978,  27716,
     25981,  23801,  21213,  18263,  15000,  11480,   7765,   3916,
         0,  -3916,  -7765, -11480, -15000, -18263, -21213, -23801,
    -25981, -27716, -28978, -29743, -30000, -29743, -28978, -27716,
    -25981, -23801, -21213, -18263, -15000, -11480,  -7765,  -3916,
};

/* volatile: advanced only in the ISR, but must survive optimisation
   across interrupt entries */
static volatile uint32_t s_sample_index = 0U;

void SAI1_IRQHandler(void)
{
    /* Underrun recovery: a FIFO error stops the transmitter until the
       flag is cleared — without this the tone dies on the first glitch */
    if ((SAI_BASE->TCSR & (uint32_t)kSAI_FIFOErrorFlag) != 0U) {
        SAI_TxClearStatusFlags(SAI_BASE, kSAI_FIFOErrorFlag);
    }

    /* One stereo frame per FIFO request: same sample left and right */
    uint32_t sample = (uint32_t)(uint16_t)s_sine_table[s_sample_index];
    SAI_WriteData(SAI_BASE, 0U, sample);   /* left  */
    SAI_WriteData(SAI_BASE, 0U, sample);   /* right */
    s_sample_index = (s_sample_index + 1U) % SINE_SAMPLES;
}

int main(void)
{
    sai_transceiver_t sai_config;

    /* Clock root: audio-capable PLL root for SAI.
       Mux/div indices: verify against the RT1170 clock tree. */
    clock_root_config_t sai_root_cfg = {0};
    sai_root_cfg.mux = 4U;
    sai_root_cfg.div = 16U;
    CLOCK_SetRootClock(kCLOCK_Root_Sai1, &sai_root_cfg);

    /* Pad mux: must precede peripheral init */
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_21_SAI1_TX_DATA00, 0U);
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_22_SAI1_TX_BCLK, 0U);
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_23_SAI1_TX_SYNC, 0U);

    /* SAI: init first, then I2S transceiver config, then bit clock rate */
    SAI_Init(SAI_BASE);
    SAI_GetClassicI2SConfig(&sai_config, kSAI_WordWidth16bits, kSAI_Stereo,
                            1U << 0U);
    sai_config.masterSlave = kSAI_Master;
    SAI_TxSetConfig(SAI_BASE, &sai_config);
    SAI_TxSetBitClockRate(SAI_BASE, SAI_CLOCK_FREQ, SAMPLE_RATE_HZ,
                          BIT_WIDTH, 2U);

    /* FIFO request fires when the FIFO drains to the watermark; the error
       interrupt covers underruns */
    SAI_TxEnableInterrupts(SAI_BASE, kSAI_FIFORequestInterruptEnable |
                                     kSAI_FIFOErrorInterruptEnable);
    EnableIRQ(SAI_IRQ);
    SAI_TxEnable(SAI_BASE, true);

    while (1) {
        /* Main loop free: all streaming happens in the ISR */
        __asm volatile("wfi");
    }
}
