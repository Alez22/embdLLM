#include "fsl_clock.h"
#include "fsl_port.h"
#include "fsl_i2c.h"

#define I2C_BAUDRATE      100000U
#define SENSOR_ADDR       0x68U          /* 7-bit address */
#define WHO_AM_I_REG      0x75U
#define I2C0_CLK_FREQ     (CLOCK_GetFreq(kCLOCK_BusClk))

static uint8_t s_who_am_i = 0;

int main(void)
{
    i2c_master_config_t masterConfig;
    i2c_master_transfer_t transfer;
    uint8_t reg = WHO_AM_I_REG;
    status_t status;

    /* Clock gate: must be enabled before any peripheral init */
    CLOCK_EnableClock(kCLOCK_PortC);
    CLOCK_EnableClock(kCLOCK_I2c0);

    /* Pin mux: must be configured before I2C init */
    PORT_SetPinMux(PORTC, 8U, kPORT_MuxAlt2);   /* PTC8 = I2C0_SCL */
    PORT_SetPinMux(PORTC, 9U, kPORT_MuxAlt2);   /* PTC9 = I2C0_SDA */

    /* I2C master init */
    I2C_MasterGetDefaultConfig(&masterConfig);
    masterConfig.baudRate_Bps = I2C_BAUDRATE;
    I2C_MasterInit(I2C0, &masterConfig, I2C0_CLK_FREQ);

    /* Write register address, then read 1 byte (combined write+read) */
    memset(&transfer, 0, sizeof(transfer));
    transfer.slaveAddress   = SENSOR_ADDR;
    transfer.direction      = kI2C_Read;
    transfer.subaddress     = WHO_AM_I_REG;
    transfer.subaddressSize = 1U;
    transfer.data           = &s_who_am_i;
    transfer.dataSize       = 1U;
    transfer.flags          = kI2C_TransferDefaultFlag;

    status = I2C_MasterTransferBlocking(I2C0, &transfer);
    if (status != kStatus_Success) {
        /* Communication error — halt */
        while (1);
    }

    /* s_who_am_i now holds the register value (0x68 for MPU-6050) */
    (void)s_who_am_i;

    while (1);
}
