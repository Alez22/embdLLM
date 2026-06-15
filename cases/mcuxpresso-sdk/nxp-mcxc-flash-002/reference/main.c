#include <stdint.h>
#include <string.h>
#include "fsl_flash.h"

#define MAGIC           0xDEADBEEFU
#define SLOT_A_ADDR     0x1E000U
#define SLOT_B_ADDR     0x1E400U
#define SECTOR_SIZE     1024U
#define FLASH_ALIGN     4U          /* minimum write unit: 4 bytes (longword) */

typedef struct {
    uint32_t magic;
    uint64_t data;
    uint32_t crc;
} config_record_t;

/* Compile-time check: record must be a multiple of flash write alignment */
typedef char _static_assert_record_size[
    (sizeof(config_record_t) % FLASH_ALIGN == 0U) ? 1 : -1
];

static flash_config_t s_flash;

static uint32_t crc32(const uint8_t *buf, uint32_t len)
{
    uint32_t crc = 0xFFFFFFFFU;
    while (len--) {
        crc ^= (uint32_t)*buf++;
        for (int i = 0; i < 8; i++) {
            crc = (crc & 1U) ? ((crc >> 1U) ^ 0xEDB88320U) : (crc >> 1U);
        }
    }
    return crc ^ 0xFFFFFFFFU;
}

static uint32_t record_crc(const config_record_t *r)
{
    /* CRC covers magic + data fields, not the stored crc field itself */
    return crc32((const uint8_t *)r, offsetof(config_record_t, crc));
}

static bool slot_valid(uint32_t addr)
{
    const config_record_t *r = (const config_record_t *)addr;
    return (r->magic == MAGIC) && (r->crc == record_crc(r));
}

static status_t write_slot(uint32_t addr, const config_record_t *rec)
{
    status_t s;

    s = FLASH_Erase(&s_flash, addr, SECTOR_SIZE, kFLASH_ApiEraseKey);
    if (s != kStatus_Success) { return s; }

    s = FLASH_Program(&s_flash, addr, (uint8_t *)rec, sizeof(*rec));
    if (s != kStatus_Success) { return s; }

    /* Verify after write — validate data integrity before declaring success */
    uint32_t fail_addr, fail_data;
    s = FLASH_VerifyProgram(&s_flash, addr, sizeof(*rec),
                            (const uint8_t *)rec,
                            kFTFx_MarginValueNormal,
                            &fail_addr, &fail_data);
    return s;
}

static void load_config(config_record_t *out)
{
    bool a_ok = slot_valid(SLOT_A_ADDR);
    bool b_ok = slot_valid(SLOT_B_ADDR);

    if (a_ok) {
        memcpy(out, (const void *)SLOT_A_ADDR, sizeof(*out));
    } else if (b_ok) {
        memcpy(out, (const void *)SLOT_B_ADDR, sizeof(*out));
    } else {
        /* Both corrupt — start with defaults */
        memset(out, 0, sizeof(*out));
        out->magic = MAGIC;
        out->data  = 0U;
        out->crc   = record_crc(out);
    }
}

static status_t save_config(const config_record_t *rec)
{
    bool a_ok = slot_valid(SLOT_A_ADDR);
    status_t s;

    /* Write-then-validate to the inactive slot first */
    if (a_ok) {
        s = write_slot(SLOT_B_ADDR, rec);
        if (s != kStatus_Success) { return s; }
        s = write_slot(SLOT_A_ADDR, rec);
    } else {
        s = write_slot(SLOT_A_ADDR, rec);
        if (s != kStatus_Success) { return s; }
        s = write_slot(SLOT_B_ADDR, rec);
    }
    return s;
}

int main(void)
{
    config_record_t cfg;

    memset(&s_flash, 0, sizeof(s_flash));
    if (FLASH_Init(&s_flash) != kStatus_Success) {
        while (1);
    }

    load_config(&cfg);

    /* Update data and persist */
    cfg.data++;
    cfg.crc = record_crc(&cfg);

    if (save_config(&cfg) != kStatus_Success) {
        while (1);
    }

    while (1);
}
