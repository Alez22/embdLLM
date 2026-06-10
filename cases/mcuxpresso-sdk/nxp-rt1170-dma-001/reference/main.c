#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "fsl_common.h"
#include "fsl_edma.h"

#define DMA_CHANNEL     0U
#define BUF_SIZE        512U

/* DMA buffers: 32-byte aligned to match the Cortex-M7 D-cache line size.
   Partial cache lines shared with other data would be corrupted by
   clean/invalidate operations. */
SDK_ALIGN(static uint8_t s_src[BUF_SIZE], 32U);
SDK_ALIGN(static uint8_t s_dst[BUF_SIZE], 32U);

/* volatile: written in DMA callback (interrupt context), read in main */
static volatile bool s_transfer_done = false;

static edma_handle_t s_dma_handle;

static void dma_callback(edma_handle_t *handle, void *user_data,
                         bool transfer_done, uint32_t tcds)
{
    (void)handle;
    (void)user_data;
    (void)tcds;
    if (transfer_done) {
        s_transfer_done = true;
    }
}

int main(void)
{
    edma_config_t          dma_config;
    edma_transfer_config_t transfer_config;

    for (uint32_t i = 0U; i < BUF_SIZE; i++) {
        s_src[i] = (uint8_t)(i & 0xFFU);
    }
    memset(s_dst, 0, BUF_SIZE);

    /* D-cache coherency: the CPU writes above landed in cache — push the
       source to RAM so the DMA engine reads real data; clean+invalidate
       the destination so no dirty line is evicted over the DMA result. */
    SCB_CleanDCache_by_Addr((uint32_t *)s_src, (int32_t)BUF_SIZE);
    SCB_CleanInvalidateDCache_by_Addr((uint32_t *)s_dst, (int32_t)BUF_SIZE);

    EDMA_GetDefaultConfig(&dma_config);
    EDMA_Init(DMA0, &dma_config);
    EDMA_CreateHandle(&s_dma_handle, DMA0, DMA_CHANNEL);
    EDMA_SetCallback(&s_dma_handle, dma_callback, NULL);

    /* Channel 0 completion interrupt — shared vector with channel 16 */
    EnableIRQ(DMA0_DMA16_IRQn);

    EDMA_PrepareTransfer(&transfer_config,
                         s_src, sizeof(uint32_t),
                         s_dst, sizeof(uint32_t),
                         32U,          /* bytes per minor loop */
                         BUF_SIZE,     /* total bytes */
                         kEDMA_MemoryToMemory);
    EDMA_SubmitTransfer(&s_dma_handle, &transfer_config);
    EDMA_StartTransfer(&s_dma_handle);

    while (!s_transfer_done) {
    }

    /* Invalidate destination lines so the CPU reads RAM, not stale cache */
    SCB_InvalidateDCache_by_Addr((uint32_t *)s_dst, (int32_t)BUF_SIZE);

    if (memcmp(s_src, s_dst, BUF_SIZE) != 0) {
        /* Copy mismatch — halt */
        while (1);
    }

    while (1);
}
