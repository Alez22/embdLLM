# Zephyr Re-Run Candidates — full 158-case set

**Problem.** Zephyr has **158 distinct cases** on disk, but almost every model was
only ever run on a small subset (8–11 cases) — different subsets per model. This is
why the Zephyr leaderboard denominators are uneven and the numbers aren't strictly
comparable. Only `deepseek/deepseek-v4-flash` has covered the full 158.

**Goal.** Re-run the relevant **local-deploy candidate** models on the **full 158
cases** so every model shares the same denominator.

**Scope.** Frontier / non-local models are excluded per the Powersoft goal:
- all **OpenAI** models (`gpt-oss-20b`, `gpt-oss-120b`)
- all **Anthropic** models (`claude-opus-*`, `claude-sonnet-*`)
- `deepseek-v4-flash` is already at 158 → **no re-run needed**.

Cases: `cases/zephyr/` (158 cases). API keys are in `.env` at the project root.
All runs use `temperature=0.5, attempts=5` to match the existing leaderboard basis.

## Candidates (ordered by current promise)

Current numbers are from each model's *best partial* run (n = cases covered so far).

- [ ] **`openrouter/qwen/qwen3-235b-a22b`** — strongest partial (70% pass / 81% cov
  on n=8). Top local candidate; confirm it holds over 158.
- [ ] **`openrouter/z-ai/glm-4.7-flash`** — 60% / 77% on n=8. Promising, thin coverage.
- [ ] **`openrouter/qwen/qwen3-235b-a22b-2507`** — 49% / 68% on n=10.
- [ ] **`groq/qwen/qwen3-32b`** — 55% / 67% on n=8. Mid-size, good local fit.
- [ ] **`groq/llama-3.3-70b-versatile`** — 42% / 62% on n=8.
- [ ] **`openrouter/google/gemma-4-31b-it`** — 50% / 48% on n=11. Small, deployable.
- [ ] **`openrouter/z-ai/glm-5.2`** — n=10 but no single-SDK summary (metrics n/a);
  needs a clean full run to place it at all.

### Suspicious / reconfirm (current data shows 0% — likely failed or mixed runs)

- [ ] **`groq/meta-llama/llama-4-scout-17b-16e-instruct`** — 0% / 0% on n=8; other
  runs show it works (~44–48% cov), so this reading is a failed/mixed run.
- [ ] **`openrouter/mistralai/mistral-small-3.2-24b-instruct`** — 5% / 21% on n=8.
- [ ] **`openrouter/qwen/qwen3-30b-a3b`** — 0% / 0% on n=8; reconfirm.
- [ ] **`openrouter/meta-llama/llama-4-maverick`** — only n=2, 0%; needs real data.

## Command template

```bash
uv run embedeval run \
  --model <MODEL_ID> \
  --cases cases/zephyr/ \
  --attempts 5
```

Example:

```bash
uv run embedeval run \
  --model openrouter/qwen/qwen3-235b-a22b \
  --cases cases/zephyr/ \
  --attempts 5
```

After the runs, regenerate the report:

```bash
uv run python results/gen_performance_report.py
```
