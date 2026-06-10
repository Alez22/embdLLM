#include <stdint.h>
#include <string.h>
#include "fsl_common.h"
#include "fsl_iomuxc.h"
#include "fsl_clock.h"
#include "fsl_lpi2c.h"
#include "fsl_sai.h"

#define CODEC_I2C         LPI2C1
#define CODEC_ADDR        0x18U          /* 7-bit address */
#define I2C_BAUDRATE      400000U
#define LPI2C_CLOCK_FREQ  (CLOCK_GetRootClockFreq(kCLOCK_Root_Lpi2c1))

#define SAI_BASE          SAI1
#define SAMPLE_RATE_HZ    48000U
#define BIT_WIDTH         16U
#define SAI_CLOCK_FREQ    (CLOCK_GetRootClockFreq(kCLOCK_Root_Sai1))

#define SINE_SAMPLES      48U            /* one 1 kHz period at 48 kHz */

/* One period of a 1 kHz sine, 16-bit signed, ~ -0.2 dBFS */
static const int16_t s_sine_table[SINE_SAMPLES] = {
         0,   3916,   7765,  11480,  15000,  18263,  21213,  23801,
     25981,  27716,  28978,  29743,  30000,  29743,  28978,  27716,
     25981,  23801,  21213,  18263,  15000,  11480,   7765,   3916,
         0,  -3916,  -7765, -11480, -15000, -18263, -21213, -23801,
    -25981, -27716, -28978, -29743, -30000, -29743, -28978, -27716,
    -25981, -23801, -21213, -18263, -15000, -11480,  -7765,  -3916,
};

/* Interleaved stereo frame buffer: L and R carry the same signal */
static int16_t s_audio_buf[SINE_SAMPLES * 2U];

static status_t codec_write_reg(uint8_t reg, uint8_t val)
{
    lpi2c_master_transfer_t xfer;
    uint8_t buf[2] = {reg, val};

    memset(&xfer, 0, sizeof(xfer));
    xfer.slaveAddress   = CODEC_ADDR;
    xfer.direction      = kLPI2C_Write;
    xfer.subaddressSize = 0U;            /* register address in buf[0] */
    xfer.data           = buf;
    xfer.dataSize       = 2U;
    xfer.flags          = kLPI2C_TransferDefaultFlag;
    return LPI2C_MasterTransferBlocking(CODEC_I2C, &xfer);
}

static status_t codec_power_up(void)
{
    status_t status;

    status = codec_write_reg(0x02U, 0x01U);   /* DAC power on */
    if (status != kStatus_Success) { return status; }
    status = codec_write_reg(0x04U, 0x00U);   /* I2S slave, 16-bit */
    if (status != kStatus_Success) { return status; }
    return codec_write_reg(0x06U, 0x3FU);     /* output volume */
}

int main(void)
{
    lpi2c_master_config_t i2c_config;
    sai_transceiver_t     sai_config;

    /* Clock roots: 24 MHz oscillator for LPI2C, audio-capable root for SAI.
       Mux/div indices: verify against the RT1170 clock tree. */
    clock_root_config_t i2c_root_cfg = {0};
    i2c_root_cfg.mux = 0U;
    i2c_root_cfg.div = 1U;
    CLOCK_SetRootClock(kCLOCK_Root_Lpi2c1, &i2c_root_cfg);

    clock_root_config_t sai_root_cfg = {0};
    sai_root_cfg.mux = 4U;
    sai_root_cfg.div = 16U;
    CLOCK_SetRootClock(kCLOCK_Root_Sai1, &sai_root_cfg);

    /* Pad mux: I2C with SION + open-drain, SAI TX signals.
       Must precede peripheral init. */
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_08_LPI2C1_SCL, 1U);
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_09_LPI2C1_SDA, 1U);
    IOMUXC_SetPinConfig(IOMUXC_GPIO_AD_08_LPI2C1_SCL, 0x10U);
    IOMUXC_SetPinConfig(IOMUXC_GPIO_AD_09_LPI2C1_SDA, 0x10U);
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_21_SAI1_TX_DATA00, 0U);
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_22_SAI1_TX_BCLK, 0U);
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_23_SAI1_TX_SYNC, 0U);

    /* I2C master for codec control */
    LPI2C_MasterGetDefaultConfig(&i2c_config);
    i2c_config.baudRate_Hz = I2C_BAUDRATE;
    LPI2C_MasterInit(CODEC_I2C, &i2c_config, LPI2C_CLOCK_FREQ);

    /* SAI: init first, then I2S transceiver config, then bit clock rate */
    SAI_Init(SAI_BASE);
    SAI_GetClassicI2SConfig(&sai_config, kSAI_WordWidth16bits, kSAI_Stereo,
                            1U << 0U);
    sai_config.masterSlave = kSAI_Master;
    SAI_TxSetConfig(SAI_BASE, &sai_config);
    SAI_TxSetBitClockRate(SAI_BASE, SAI_CLOCK_FREQ, SAMPLE_RATE_HZ,
                          BIT_WIDTH, 2U);

    /* Codec must be configured before streaming starts: it has to lock to
       BCLK and be powered before the first valid frame. */
    if (codec_power_up() != kStatus_Success) {
        while (1);
    }

    /* Build the interleaved stereo buffer once */
    for (uint32_t i = 0U; i < SINE_SAMPLES; i++) {
        s_audio_buf[2U * i]      = s_sine_table[i];   /* left  */
        s_audio_buf[2U * i + 1U] = s_sine_table[i];   /* right */
    }

    while (1) {
        SAI_WriteBlocking(SAI_BASE, 0U, BIT_WIDTH,
                          (uint8_t *)s_audio_buf, sizeof(s_audio_buf));
    }
}
