"""EmbedEval benchmark runner package.

Re-exports the public runner API so existing imports
(``from embedeval.runner import ...``) and test patches
(``patch("embedeval.runner.call_model")``) keep working unchanged.
"""

# call_model / evaluate are package attributes so tests can patch them as
# ``embedeval.runner.call_model`` / ``embedeval.runner.evaluate``.
# execution._run_single_case calls them through this package module, so they
# must be bound here before execution is imported.
from embedeval.evaluator import evaluate
from embedeval.llm_client import call_model
from embedeval.runner.checkpoint import _append_checkpoint, _load_checkpoint
from embedeval.runner.discovery import (
    Filters,
    discover_cases,
    filter_cases,
    iter_case_dirs,
    load_case_metadata,
)
from embedeval.runner.execution import (
    _build_result_from_grade,
    _make_error_result,
    _run_single_case,
    run_benchmark,
)
from embedeval.runner.prompts import (
    _collect_context_files,
    _inject_board_target,
    _load_prompt,
)

__all__ = [
    "Filters",
    "iter_case_dirs",
    "load_case_metadata",
    "discover_cases",
    "filter_cases",
    "_load_prompt",
    "_collect_context_files",
    "_inject_board_target",
    "_make_error_result",
    "_load_checkpoint",
    "_append_checkpoint",
    "_build_result_from_grade",
    "_run_single_case",
    "run_benchmark",
    "call_model",
    "evaluate",
]
