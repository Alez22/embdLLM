"""EmbedEval 5-layer evaluation engine (facade package).

Re-exports the full evaluator API so ``from embedeval.evaluator import ...``
and the many test patches (``patch("embedeval.evaluator.subprocess")``,
``patch("embedeval.evaluator._get_build_mode")`` etc.) keep working
unchanged after the split. The patched names are bound here as package
attributes; the build/pipeline submodules call them through this package so
the patches take effect at call time.
"""

# subprocess is a package attribute so tests can patch
# embedeval.evaluator.subprocess; build.py calls _ev.subprocess.run(...).
import subprocess  # noqa: F401

from embedeval.evaluator.support import (
    _build_env_available,
    _esp_idf_env_available,
    _extract_build_errors,
    _get_build_board,
    _get_build_mode,
    _get_docker_image,
    _is_esp_idf_case,
    _is_l1_skipped,
    _is_l2_skipped,
    _is_stm32_case,
    _load_case_meta,
    _stm32_env_available,
)
from embedeval.evaluator.checks import (
    _CheckModuleError,
    _execute_check_module,
    _load_check_module,
    _load_negatives,
    _run_behavioral,
    _run_mutant_checks,
    _run_static_checks,
)
from embedeval.evaluator.build import (
    DEFAULT_TIMEOUT,
    RUNTIME_TIMEOUT,
    _prepare_build_dir,
    _run_compile_docker,
    _run_compile_esp_idf,
    _run_compile_gate,
    _run_compile_local,
    _run_compile_stm32,
    _run_runtime,
)
from embedeval.evaluator.pipeline import (
    LAYER_NAMES,
    _count_scorable_layers,
    _layer_exists_for_case,
    _run_layer,
    evaluate,
)

# Full public + internal surface re-exported by the facade. Listing every
# name in __all__ documents the contract and silences "unused import" for the
# intentional re-exports (tests import/patch several of the underscored ones).
__all__ = [
    "evaluate",
    "LAYER_NAMES",
    "DEFAULT_TIMEOUT",
    "RUNTIME_TIMEOUT",
    "subprocess",
    "_extract_build_errors",
    "_load_case_meta",
    "_is_l1_skipped",
    "_is_l2_skipped",
    "_get_build_mode",
    "_build_env_available",
    "_get_docker_image",
    "_get_build_board",
    "_esp_idf_env_available",
    "_is_esp_idf_case",
    "_is_stm32_case",
    "_stm32_env_available",
    "_run_static_checks",
    "_run_behavioral",
    "_run_mutant_checks",
    "_load_negatives",
    "_CheckModuleError",
    "_load_check_module",
    "_execute_check_module",
    "_prepare_build_dir",
    "_run_compile_gate",
    "_run_compile_docker",
    "_run_compile_local",
    "_run_compile_esp_idf",
    "_run_compile_stm32",
    "_run_runtime",
    "_run_layer",
    "_layer_exists_for_case",
    "_count_scorable_layers",
]
