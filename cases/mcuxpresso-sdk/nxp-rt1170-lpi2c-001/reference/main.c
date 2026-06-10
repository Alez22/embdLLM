#include <stdint.h>
#include <string.h>
#include "fsl_common.h"
#include "fsl_iomuxc.h"
#include "fsl_clock.h"
#include "fsl_lpi2c.h"

#define LPI2C_BASE        LPI2C1
#define LPI2C_BAUDRATE    400000U
#define SENSOR_ADDR       0x68U          /* 7-bit address */
#define WHO_AM_I_REG      0x75U
#define LPI2C_CLOCK_FREQ  (CLOCK_GetRootClockFreq(kCLOCK_Root_Lpi2c1))

static uint8_t s_who_am_i = 0U;

int main(void)
{
    lpi2c_master_config_t   config;
    lpi2c_master_transfer_t transfer;
    status_t                status;

    /* Clock root for LPI2C1: 24 MHz oscillator, divide by 1.
       Mux/div indices: verify against the RT1170 clock tree. */
    clock_root_config_t root_cfg = {0};
    root_cfg.mux = 0U;
    root_cfg.div = 1U;
    CLOCK_SetRootClock(kCLOCK_Root_Lpi2c1, &root_cfg);

    /* Pad mux: SION enabled (I2C needs to read back the pin state),
       open-drain pad config. Must precede LPI2C init. */
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_08_LPI2C1_SCL, 1U);
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_09_LPI2C1_SDA, 1U);
    IOMUXC_SetPinConfig(IOMUXC_GPIO_AD_08_LPI2C1_SCL, 0x10U);
    IOMUXC_SetPinConfig(IOMUXC_GPIO_AD_09_LPI2C1_SDA, 0x10U);

    LPI2C_MasterGetDefaultConfig(&config);
    config.baudRate_Hz = LPI2C_BAUDRATE;
    LPI2C_MasterInit(LPI2C_BASE, &config, LPI2C_CLOCK_FREQ);

    /* Combined write+read: register address as subaddress */
    memset(&transfer, 0, sizeof(transfer));
    transfer.slaveAddress   = SENSOR_ADDR;
    transfer.direction      = kLPI2C_Read;
    transfer.subaddress     = WHO_AM_I_REG;
    transfer.subaddressSize = 1U;
    transfer.data           = &s_who_am_i;
    transfer.dataSize       = 1U;
    transfer.flags          = kLPI2C_TransferDefaultFlag;

    status = LPI2C_MasterTransferBlocking(LPI2C_BASE, &transfer);
    if (status != kStatus_Success) {
        /* Communication error — halt */
        while (1);
    }

    (void)s_who_am_i;

    while (1);
}
