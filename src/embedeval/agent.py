"""Multi-turn agent evaluation mode."""

import logging
from dataclasses import dataclass, field
from pathlib import Path

from embedeval.evaluator import evaluate
from embedeval.llm_client import call_model
from embedeval.models import EvalResult

logger = logging.getLogger(__name__)


@dataclass
class AgentResult:
    """Result of multi-turn agent evaluation."""

    case_id: str
    passed: bool
    turns_used: int
    max_turns: int
    history: list[EvalResult] = field(default_factory=list)


def evaluate_agent(
    case_dir: Path,
    model: str,
    prompt: str,
    max_turns: int = 5,
    timeout: float = 300.0,
    context_pack: str | None = None,
    start_turn: int = 1,
    initial_context: list[str] | None = None,
    prior_history: list[EvalResult] | None = None,
) -> AgentResult:
    """Evaluate a case using multi-turn agent with error feedback.

    On each turn the LLM receives the original prompt plus any accumulated
    error context from failed previous turns. Stops as soon as the case
    passes all layers or max_turns is exhausted.

    Args:
        case_dir: Path to the case directory containing checks/.
        model: Model identifier for LLM calls.
        prompt: Original task prompt.
        max_turns: Maximum number of LLM turns (default 5).
        timeout: Per-call timeout in seconds.
        context_pack: Optional run-wide context (e.g. team CLAUDE.md or
            expert pack content) prepended to every LLM call across all
            turns. See docs/CONTEXT-QUALITY-MODE.md.
        start_turn: First turn number to execute. Used by --resume to
            continue a previous agent run from turn N+1 instead of 1.
        initial_context: Accumulated error context from prior turns, used
            together with start_turn when resuming.
        prior_history: EvalResults from prior turns to prepend to the
            returned history when resuming.

    Returns:
        AgentResult with pass/fail status, turns used, and per-turn history.
    """
    context: list[str] = list(initial_context or [])
    case_id = case_dir.name
    history: list[EvalResult] = list(prior_history or [])
    # The most recent generated source, fed back so the model patches its own
    # code instead of regenerating from scratch each turn. Seeded from the
    # last prior-history turn when resuming.
    last_code: str | None = (
        history[-1].generated_code if history else None
    )

    for turn in range(start_turn, max_turns + 1):
        # Build prompt: show the model its last attempt (so errors that
        # reference line numbers are actionable) plus the accumulated error
        # history, then ask for a fix.
        if context and last_code is not None:
            full_prompt = (
                f"{prompt}\n\n"
                f"Your previous attempt:\n```c\n{last_code}\n```\n\n"
                f"Previous attempts and errors:\n"
                + "\n".join(context)
                + "\n\nFix the code above and output ONLY"
                " the complete C source file."
            )
        else:
            full_prompt = prompt

        # Generate code
        llm_response = call_model(
            model=model,
            prompt=full_prompt,
            context_pack=context_pack,
            timeout=timeout,
        )
        generated_code = llm_response.generated_code
        last_code = generated_code

        # Evaluate
        result = evaluate(
            case_dir=case_dir,
            generated_code=generated_code,
            model=model,
            attempt=turn,
            token_usage=llm_response.token_usage,
            cost_usd=llm_response.cost_usd,
        )
        history.append(result)

        if result.passed:
            logger.info("Case %s passed on turn %d/%d", case_id, turn, max_turns)
            return AgentResult(
                case_id=case_id,
                passed=True,
                turns_used=turn,
                max_turns=max_turns,
                history=history,
            )

        # Build error feedback for the next turn
        if result.failed_at_layer is not None:
            failed_layer = result.layers[result.failed_at_layer]
            error_summary = failed_layer.error or ""
            failed_checks = [
                f"- {d.check_name}: expected={d.expected}, actual={d.actual}"
                for d in failed_layer.details
                if not d.passed
            ]
            context.append(
                f"Turn {turn} failed at {failed_layer.name}:\n"
                f"{error_summary}\n"
                + "\n".join(failed_checks[:5])  # limit to 5 checks per turn
            )

        logger.info("Case %s failed on turn %d/%d", case_id, turn, max_turns)

    return AgentResult(
        case_id=case_id,
        passed=False,
        turns_used=max_turns,
        max_turns=max_turns,
        history=history,
    )
