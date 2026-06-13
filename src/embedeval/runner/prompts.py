"""Prompt loading and context assembly for a case."""

from pathlib import Path

from embedeval.models import CaseMetadata


def _load_prompt(case_dir: Path) -> str:
    """Load the prompt file from a case directory."""
    prompt_file = case_dir / "prompt.md"
    if prompt_file.is_file():
        return prompt_file.read_text(encoding="utf-8")

    prompt_txt = case_dir / "prompt.txt"
    if prompt_txt.is_file():
        return prompt_txt.read_text(encoding="utf-8")

    return f"Generate Zephyr RTOS code for case: {case_dir.name}"


def _collect_context_files(case_dir: Path) -> list[str]:
    """Collect context files from the case directory."""
    context_dir = case_dir / "context"
    if not context_dir.is_dir():
        return []
    return [str(f) for f in sorted(context_dir.iterdir()) if f.is_file()]


def _inject_board_target(prompt: str, meta: CaseMetadata) -> str:
    """Inject build target board information into the prompt.

    Adds a target board line so the LLM knows which board to write code for.
    """
    board = meta.build_board or "native_sim"
    return prompt.rstrip() + "\n\nTarget board: " + board + "\n"
