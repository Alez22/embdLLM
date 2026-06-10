# EmbedEval Leaderboard

<!-- SCHEMA_VERSION: 1 -->


## Model Comparison

| Model | pass@1 (full) | pass@1 (quality) | check coverage | avg time | 95% CI | pass@5 | Passed | Quality | Total | Samples |
|-------|---------------|------------------|----------------|----------|--------|--------|--------|---------|-------|---------|
| groq/openai/gpt-oss-120b | 80.0% | 83.3% | 90.3% | 1.1s | [57.1%, 92.3%] | 83.3% | 15 | 15 | 18 | n=5 |
| groq/llama-3.3-70b-versatile | 44.4% | 44.4% | 44.4% | 0.0s | [24.6%, 66.3%] | 44.4% | 8 | 8 | 18 | n=1 |
| groq/meta-llama/llama-4-scout-17b-16e-instruct | 44.4% | 44.4% | 44.4% | 0.0s | [24.6%, 66.3%] | 44.4% | 8 | 8 | 18 | n=1 |
| groq/openai/gpt-oss-20b | 66.7% | 66.7% | 66.7% | 0.0s | [43.7%, 83.7%] | 66.7% | 12 | 12 | 18 | n=1 |
| groq/qwen/qwen3-32b | 50.0% | 50.0% | 50.0% | 0.0s | [29.0%, 71.0%] | 50.0% | 9 | 9 | 18 | n=1 |
| openrouter/mistralai/mistral-small-3.2-24b-instruct | 12.5% | 12.5% | 12.5% | 0.0s | [2.2%, 47.1%] | 12.5% | 1 | 1 | 8 | n=1 |
| openrouter/qwen/qwen3-30b-a3b | 0.0% | 0.0% | 0.0% | 0.0s | [0.0%, 32.4%] | 0.0% | 0 | 0 | 8 | n=1 |

*pass@1 (full) = all layers must pass. pass@1 (quality) = L0+L3 only (code quality, ignoring build/runtime).*

## Tier Breakdown

| Tier | pass@1 | Passed | Total |
|------|--------|--------|-------|
| Sanity (not scored) | 100.0% | 2 | 2 |
| Core | 77.8% | 7 | 9 |
| Challenge | 85.7% | 6 | 7 |
| Sanity (not scored) | 0.0% | 0 | 2 |
| Core | 33.3% | 3 | 9 |
| Challenge | 71.4% | 5 | 7 |
| Sanity (not scored) | 50.0% | 1 | 2 |
| Core | 33.3% | 3 | 9 |
| Challenge | 57.1% | 4 | 7 |
| Sanity (not scored) | 50.0% | 1 | 2 |
| Core | 66.7% | 6 | 9 |
| Challenge | 71.4% | 5 | 7 |
| Sanity (not scored) | 0.0% | 0 | 2 |
| Core | 66.7% | 6 | 9 |
| Challenge | 42.9% | 3 | 7 |
| Sanity (not scored) | 50.0% | 1 | 2 |
| Core | 0.0% | 0 | 3 |
| Challenge | 0.0% | 0 | 3 |
| Sanity (not scored) | 0.0% | 0 | 2 |
| Core | 0.0% | 0 | 3 |
| Challenge | 0.0% | 0 | 3 |

## Reasoning Type Breakdown

| Reasoning Type | pass@1 | Cases | LLM Reliability |
|----------------|--------|-------|-----------------|
| L1 API Recall | 83.3% | 18 | Review recommended |
| L2 Rule Application | 83.3% | 18 | Review recommended |
| L1 API Recall | 44.4% | 18 | Expert review required |
| L2 Rule Application | 44.4% | 18 | Expert review required |
| L1 API Recall | 44.4% | 18 | Expert review required |
| L2 Rule Application | 44.4% | 18 | Expert review required |
| L1 API Recall | 66.7% | 18 | Expert review required |
| L2 Rule Application | 66.7% | 18 | Expert review required |
| L1 API Recall | 50.0% | 18 | Expert review required |
| L2 Rule Application | 50.0% | 18 | Expert review required |
| L1 API Recall | 12.5% | 8 | Expert review required |
| L2 Rule Application | 12.5% | 8 | Expert review required |
| L1 API Recall | 0.0% | 8 | Expert review required |
| L2 Rule Application | 0.0% | 8 | Expert review required |

## SDK Breakdown

| SDK | pass@1 | Passed | Total | Notes |
|-----|--------|--------|-------|-------|
| zephyr | 83.3% | 15 | 18 |  |
| zephyr | 44.4% | 8 | 18 |  |
| zephyr | 44.4% | 8 | 18 |  |
| zephyr | 66.7% | 12 | 18 |  |
| zephyr | 50.0% | 9 | 18 |  |
| zephyr | 12.5% | 1 | 8 |  |
| zephyr | 0.0% | 0 | 8 |  |

## Category Results

| Category | pass@1 | Passed | Total | Status |
|----------|--------|--------|-------|--------|
| adc | 100.0% | 2 | 2 | PASS |
| device-tree | 87.5% | 7 | 8 | PASS |
| kconfig | 75.0% | 6 | 8 | PARTIAL |
| adc | 0.0% | 0 | 2 | FAIL |
| device-tree | 62.5% | 5 | 8 | PARTIAL |
| kconfig | 37.5% | 3 | 8 | FAIL |
| adc | 0.0% | 0 | 2 | FAIL |
| device-tree | 50.0% | 4 | 8 | PARTIAL |
| kconfig | 50.0% | 4 | 8 | PARTIAL |
| adc | 50.0% | 1 | 2 | PARTIAL |
| device-tree | 75.0% | 6 | 8 | PARTIAL |
| kconfig | 62.5% | 5 | 8 | PARTIAL |
| adc | 0.0% | 0 | 2 | FAIL |
| device-tree | 50.0% | 4 | 8 | PARTIAL |
| kconfig | 62.5% | 5 | 8 | PARTIAL |
| kconfig | 12.5% | 1 | 8 | FAIL |
| kconfig | 0.0% | 0 | 8 | FAIL |

## Layer Pass Rate Heatmap

| Model| L0 Static| L1 Build| L2 Runtime| L3 Heuristic| L4 Mutation| |
|-------|----------|----------|----------|----------|----------||
| groq/openai/gpt-oss-120b| 92%| 100%| 100%| 87%| 100%| |
| groq/llama-3.3-70b-versatile| 67%| 100%| 100%| 67%| 100%| |
| groq/meta-llama/llama-4-scout-17b-16e-instruct| 72%| 100%| 100%| 62%| 100%| |
| groq/openai/gpt-oss-20b| 83%| 100%| 100%| 80%| 100%| |
| groq/qwen/qwen3-32b| 50%| 100%| 100%| 100%| 100%| |
| openrouter/mistralai/mistral-small-3.2-24b-instruct| 12%| 100%| 100%| 100%| 100%| |
| openrouter/qwen/qwen3-30b-a3b| 0%| -| -| -| -| |

## Failure Distribution

| Layer | Failures | % of Total |
|-------|----------|-----------|
| L0 Static | 3.2 | 76% |
| L1 Build | 0.0 | 0% |
| L2 Runtime | 0.0 | 0% |
| L3 Heuristic | 1.0 | 24% |
| L4 Mutation | 0.0 | 0% |

## Category Breakdown

| Category | Pass@1 | Cases |
|----------|--------|-------|
| adc | 100% | 2 |
| device-tree | 88% | 8 |
| kconfig | 75% | 8 |
| adc | 0% | 2 |
| device-tree | 62% | 8 |
| kconfig | 38% | 8 |
| adc | 0% | 2 |
| device-tree | 50% | 8 |
| kconfig | 50% | 8 |
| adc | 50% | 2 |
| device-tree | 75% | 8 |
| kconfig | 62% | 8 |
| adc | 0% | 2 |
| device-tree | 50% | 8 |
| kconfig | 62% | 8 |
| kconfig | 12% | 8 |
| kconfig | 0% | 8 |

