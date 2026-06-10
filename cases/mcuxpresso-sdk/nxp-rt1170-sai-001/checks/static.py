"""Static checks for nxp-rt1170-sai-001.

L0: pattern matching on generated source text, no compilation needed.
"""

import re

from embedeval.check_utils import scoped_contains, strip_comments
from embedeval.check_utils_nxp import no_nxp_hallucination
from embedeval.models import CheckDetail


def run_checks(generated_code: str) -> list[CheckDetail]:
    """Validate RT1170 SAI I2S + codec control code structure."""
    details: list[CheckDetail] = []
    stripped = strip_comments(generated_code)

    for header in ("fsl_sai.h", "fsl_lpi2c.h", "fsl_iomuxc.h"):
        present = scoped_contains(generated_code, header, scope="code_only")
        details.append(CheckDetail(
            check_name=f"header_{header.replace('.', '_')}",
            passed=present,
            expected=f"{header} included",
            actual="present" if present else "missing",
            check_type="exact_match",
        ))

    has_sai_init = scoped_contains(generated_code, "SAI_Init", scope="stripped")
    details.append(CheckDetail(
        check_name="sai_init_called",
        passed=has_sai_init,
        expected="SAI_Init called",
        actual="present" if has_sai_init else "missing",
        check_type="exact_match",
    ))

    # Any current-API TX configuration path is accepted
    has_sai_config = bool(re.search(
        r"\b(SAI_TxSetConfig|SAI_GetClassicI2SConfig|SAI_TxInit)\s*\(", stripped
    ))
    details.append(CheckDetail(
        check_name="sai_tx_configured",
        passed=has_sai_config,
        expected="SAI TX configured (SAI_TxSetConfig / SAI_GetClassicI2SConfig)",
        actual="present" if has_sai_config else "missing",
        check_type="exact_match",
    ))

    # Streaming API present (blocking or transactional)
    has_sai_write = bool(re.search(
        r"\b(SAI_WriteBlocking|SAI_TransferSendBlocking|"
        r"SAI_TransferSendNonBlocking|SAI_WriteNonBlocking)\s*\(", stripped
    ))
    details.append(CheckDetail(
        check_name="sai_write_api_used",
        passed=has_sai_write,
        expected="SAI write/stream API called",
        actual="present" if has_sai_write else "missing",
        check_type="exact_match",
    ))

    has_i2c_transfer = scoped_contains(
        generated_code, "LPI2C_MasterTransferBlocking", scope="stripped"
    )
    details.append(CheckDetail(
        check_name="lpi2c_blocking_transfer_used",
        passed=has_i2c_transfer,
        expected="LPI2C_MasterTransferBlocking used for codec register writes",
        actual="present" if has_i2c_transfer else "missing",
        check_type="exact_match",
    ))

    foreign = no_nxp_hallucination(generated_code)
    details.append(CheckDetail(
        check_name="no_cross_platform_hallucination",
        passed=len(foreign) == 0,
        expected="Only NXP MCUXpresso SDK APIs used",
        actual="clean" if not foreign else f"found: {foreign}",
        check_type="constraint",
    ))

    return details
