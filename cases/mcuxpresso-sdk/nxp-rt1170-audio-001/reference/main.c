#include <stdint.h>
#include "fsl_common.h"
#include "fsl_iomuxc.h"
#include "fsl_clock.h"
#include "fsl_sai.h"

#define SAI_BASE          SAI1
#define SAMPLE_RATE_HZ    48000U
#define BIT_WIDTH         16U
#define SAI_CLOCK_FREQ    (CLOCK_GetRootClockFreq(kCLOCK_Root_Sai1))

#define FRAMES_PER_CHUNK  16U

/* Interleaved stereo working buffer: 16 frames keeps latency < 0.5 ms */
static int16_t s_chunk[FRAMES_PER_CHUNK * 2U];

int main(void)
{
    sai_transceiver_t tx_config;
    sai_transceiver_t rx_config;

    /* Clock root: audio-capable PLL root for SAI.
       Mux/div indices: verify against the RT1170 clock tree. */
    clock_root_config_t sai_root_cfg = {0};
    sai_root_cfg.mux = 4U;
    sai_root_cfg.div = 16U;
    CLOCK_SetRootClock(kCLOCK_Root_Sai1, &sai_root_cfg);

    /* Pad mux: must precede peripheral init.
       RX_DATA00 macro: verify against the part's pad table. */
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_21_SAI1_TX_DATA00, 0U);
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_22_SAI1_TX_BCLK, 0U);
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_23_SAI1_TX_SYNC, 0U);
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_17_SAI1_RX_DATA00, 0U);

    SAI_Init(SAI_BASE);

    /* TX: async I2S master — owns BCLK and SYNC */
    SAI_GetClassicI2SConfig(&tx_config, kSAI_WordWidth16bits, kSAI_Stereo,
                            1U << 0U);
    tx_config.masterSlave = kSAI_Master;
    SAI_TxSetConfig(SAI_BASE, &tx_config);
    SAI_TxSetBitClockRate(SAI_BASE, SAI_CLOCK_FREQ, SAMPLE_RATE_HZ,
                          BIT_WIDTH, 2U);

    /* RX: sync mode — borrows the TX bit clock and frame sync, so both
       directions stay sample-locked and RX needs no divider of its own */
    SAI_GetClassicI2SConfig(&rx_config, kSAI_WordWidth16bits, kSAI_Stereo,
                            1U << 0U);
    rx_config.masterSlave = kSAI_Master;
    rx_config.syncMode = kSAI_ModeSync;
    SAI_RxSetConfig(SAI_BASE, &rx_config);

    SAI_TxEnable(SAI_BASE, true);
    SAI_RxEnable(SAI_BASE, true);

    while (1) {
        SAI_ReadBlocking(SAI_BASE, 0U, BIT_WIDTH,
                         (uint8_t *)s_chunk, sizeof(s_chunk));
        SAI_WriteBlocking(SAI_BASE, 0U, BIT_WIDTH,
                          (uint8_t *)s_chunk, sizeof(s_chunk));
    }
}
