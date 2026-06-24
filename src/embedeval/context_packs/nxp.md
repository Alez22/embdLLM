# NXP MCUXpresso SDK — correct header and API names

You are writing bare-metal C for NXP MCUXpresso SDK targets:
- Kinetis/MCX family: **MCXC144** (Cortex-M0+)
- i.MX RT family: **MIMXRT1176** (Cortex-M7)

Include the SDK **driver** headers, not raw device headers. The device
register definitions are pulled in transitively by the driver/clock/common
headers below. Do NOT include a raw device header such as `MCXC144.h`,
`MKV11Z4.h`, or any `*_cmsis.h` / `arm_cm*.h` / `fsl_reset.h` file — these
are not part of the build include set and will fail to compile.

## Kinetis / MCXC144 (bare-metal)

Use exactly these driver headers (verified against the SDK):
- `fsl_clock.h`   — clock gating and clock config
- `fsl_port.h`    — pin mux (PORT_SetPinMux)
- `fsl_gpio.h`    — GPIO
- `fsl_i2c.h`     — I2C master/slave
- `fsl_spi.h`     — SPI

Do not include `MCXC144.h` directly; `fsl_clock.h` brings in the device
definitions. There is no `fsl_reset.h` on this platform.

## i.MX RT1170 / MIMXRT1176 (bare-metal, Cortex-M7)

Use exactly these driver headers (verified against the SDK):
- `fsl_common.h`  — common types and device registers
- `fsl_clock.h`   — clock config
- `fsl_iomuxc.h`  — pin mux (IOMUXC_SetPinMux), NOT fsl_port.h
- `fsl_lpi2c.h`   — LPI2C (the RT I2C peripheral is LPI2C, not I2C)
- `fsl_lpspi.h`   — LPSPI (the RT SPI peripheral is LPSPI, not SPI)

Do not include `fsl_reset.h`, `fsl_lpspi_cmsis.h`, or `fsl_lpi2c_cmsis.h`.
Clocks on RT are configured via `fsl_clock.h`; there is no separate reset
header in the build include set.

## General NXP idioms (apply without being told)

- Enable the peripheral clock gate before initializing the peripheral
  (CLOCK_EnableClock before *_Init).
- Configure pin mux before using the peripheral.
- Get the default config struct (*_GetDefaultConfig), then override fields,
  then *_Init.
- Check the status_t return of operations that can fail.
- Mark ISR-shared variables volatile.
