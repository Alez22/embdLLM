"""Negative tests for nxp-mcxc-flash-001 (flash erase + write + verify).

Reference: cases/mcuxpresso-sdk/nxp-mcxc-flash-001/reference/main.c
Checks:    static.py + behavior.py

Each mutation seeds a realistic MCXC144 bare-metal bug into the reference
and asserts the corresponding L0/L3 check detects it.
"""

import re

_ERASE_BLOCK = (
    "    /* Erase sector: must be done before write — flash bits can only go 1→0 */\n"
    "    status = FLASH_Erase(&flash_cfg, FLASH_TARGET_ADDR, FLASH_SECTOR_SIZE,\n"
    "                         kFLASH_ApiEraseKey);\n"
    "    if (status != kStatus_Success) {\n"
    "        blink_forever(100000U);  /* medium blink = erase error */\n"
    "    }\n"
    "\n"
)

_VERIFY_BLOCK = (
    "    /* Verify written data matches source */\n"
    "    status = FLASH_VerifyProgram(&flash_cfg, FLASH_TARGET_ADDR, sizeof(s_data),\n"
    "                                 (const uint8_t *)s_data,\n"
    "                                 kFTFx_MarginValueNormal,\n"
    "                                 &fail_addr, &fail_data);\n"
    "    (void)fail_addr;\n"
    "    (void)fail_data;\n"
    "    (void)fail_expected;\n"
    "\n"
    "    if (status != kStatus_Success) {\n"
    "        blink_forever(300000U);  /* very slow blink = verify error */\n"
    "    }\n"
    "\n"
)

_INIT_BLOCK = (
    "    memset(&flash_cfg, 0, sizeof(flash_cfg));\n"
    "    status = FLASH_Init(&flash_cfg);\n"
    "    if (status != kStatus_Success) {\n"
    "        blink_forever(50000U);  /* fast blink = init error */\n"
    "    }\n"
    "\n"
)

_PROGRAM_TAIL = (
    "    if (status != kStatus_Success) {\n"
    "        blink_forever(200000U);  /* slow blink = write error */\n"
    "    }\n"
)


def _remove_lines(code: str, pattern: str) -> str:
    """Remove all lines containing *pattern*."""
    return "\n".join(line for line in code.splitlines() if pattern not in line)


def _drop_status_checks(code: str) -> str:
    """Remove every 'if (status != kStatus_Success) {...}' block."""
    return re.sub(
        r"if \(status != kStatus_Success\) \{[^{}]*\}", "(void)status;", code
    )


NEGATIVES = [
    {
        "name": "write_without_erase",
        "description": "Erase removed — programming non-blank flash fails (bits only go 1→0)",
        "mutation": lambda code: code.replace(_ERASE_BLOCK, ""),
        "must_fail": [
            "erase_before_write",
            "flash_erase_sector_called",
            "flash_erase_key_used",
        ],
    },
    {
        "name": "erase_after_program",
        "description": "Erase moved after program — write hits stale data, then erase destroys it",
        "mutation": lambda code: (
            code
            .replace(_ERASE_BLOCK, "")
            .replace(_PROGRAM_TAIL, _PROGRAM_TAIL + "\n" + _ERASE_BLOCK)
        ),
        "must_fail": ["erase_before_write"],
    },
    {
        "name": "no_verify",
        "description": "Verify removed — silent write corruption goes undetected",
        "mutation": lambda code: code.replace(_VERIFY_BLOCK, ""),
        "must_fail": ["verify_after_write", "flash_verify_program_called"],
    },
    {
        "name": "status_ignored",
        "description": "All flash return values ignored — errors silently swallowed",
        "mutation": _drop_status_checks,
        "must_fail": ["flash_return_value_checked"],
    },
    {
        "name": "wrong_erase_key",
        "description": "Magic number instead of kFLASH_ApiEraseKey — erase command rejected",
        "mutation": lambda code: code.replace("kFLASH_ApiEraseKey", "0xA5A5A5A5U"),
        "must_fail": ["flash_erase_key_used"],
    },
    {
        "name": "missing_flash_init",
        "description": "FLASH_Init removed — driver state uninitialised, operations undefined",
        "mutation": lambda code: code.replace(_INIT_BLOCK, ""),
        "must_fail": ["flash_init_called"],
    },
    {
        "name": "missing_flash_header",
        "description": "fsl_flash.h include removed — relies on transitive includes",
        "mutation": lambda code: _remove_lines(code, '#include "fsl_flash.h"'),
        "must_fail": ["header_fsl_flash_h"],
    },
    {
        "name": "stm32_flash_write",
        "description": "STM32-style HAL flash call used instead of MCUXpresso FLASH_Program",
        # Replace any FLASH_Program(...) call with the STM32 HAL_FLASH_Write
        # call, regardless of arguments/spacing: removes FLASH_Program (fails
        # flash_program_called) and injects HAL_ (fails the hallucination
        # check). The literal whole-statement replace missed every model that
        # spelled the args differently.
        "mutation": lambda code: re.sub(
            r"\bFLASH_Program\s*\([^;]*\)",
            "HAL_FLASH_Write(FLASH_TARGET_ADDR, (uint8_t *)s_data, sizeof(s_data))",
            code,
        ),
        "must_fail": ["flash_program_called", "no_cross_platform_hallucination"],
    },
]
