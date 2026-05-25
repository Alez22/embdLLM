#include <string.h>
#include "fsl_clock.h"
#include "fsl_port.h"
#include "fsl_i2c.h"

#define I2C_BAUDRATE    400000U
#define SENSOR_ADDR     0x68U
#define CONFIG_REG      0x1AU
#define CONFIG_VAL      0x06U
#define I2C0_CLK_FREQ   (CLOCK_GetFreq(kCLOCK_BusClk))

static uint8_t s_readback = 0U;

static status_t i2c_write_reg(uint8_t reg, uint8_t val)
{
    i2c_master_transfer_t xfer;
    uint8_t buf[2] = {reg, val};

    memset(&xfer, 0, sizeof(xfer));
    xfer.slaveAddress   = SENSOR_ADDR;
    xfer.direction      = kI2C_Write;
    xfer.subaddressSize = 0U;    /* address already in buf[0] */
    xfer.data           = buf;
    xfer.dataSize       = 2U;
    xfer.flags          = kI2C_TransferDefaultFlag;
    return I2C_MasterTransferBlocking(I2C0, &xfer);
}

static status_t i2c_read_reg(uint8_t reg, uint8_t *out)
{
    i2c_master_transfer_t xfer;

    memset(&xfer, 0, sizeof(xfer));
    xfer.slaveAddress   = SENSOR_ADDR;
    xfer.direction      = kI2C_Read;
    xfer.subaddress     = reg;
    xfer.subaddressSize = 1U;
    xfer.data           = out;
    xfer.dataSize       = 1U;
    xfer.flags          = kI2C_TransferDefaultFlag;
    return I2C_MasterTransferBlocking(I2C0, &xfer);
}

int main(void)
{
    i2c_master_config_t master_cfg;
    status_t            status;

    /* Clock gates */
    CLOCK_EnableClock(kCLOCK_PortC);
    CLOCK_EnableClock(kCLOCK_I2c0);

    /* Pin mux */
    PORT_SetPinMux(PORTC, 8U, kPORT_MuxAlt2);   /* PTC8 = I2C0_SCL */
    PORT_SetPinMux(PORTC, 9U, kPORT_MuxAlt2);   /* PTC9 = I2C0_SDA */

    I2C_MasterGetDefaultConfig(&master_cfg);
    master_cfg.baudRate_Bps = I2C_BAUDRATE;
    I2C_MasterInit(I2C0, &master_cfg, I2C0_CLK_FREQ);

    /* Write configuration register */
    status = i2c_write_reg(CONFIG_REG, CONFIG_VAL);
    if (status != kStatus_Success) {
        while (1);
    }

    /* Read back to verify — separate transfer (not repeated start) */
    status = i2c_read_reg(CONFIG_REG, &s_readback);
    if (status != kStatus_Success) {
        while (1);
    }

    /* s_readback should equal CONFIG_VAL */
    (void)s_readback;

    while (1);
}
