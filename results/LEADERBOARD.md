# EmbedEval Leaderboard

<!-- SCHEMA_VERSION: 1 -->


## Model Comparison

| Model | pass@1 (full) | pass@1 (quality) | check coverage | avg time | 95% CI | pass@5 | Passed | Quality | Total | Samples |
|-------|---------------|------------------|----------------|----------|--------|--------|--------|---------|-------|---------|
| openrouter/z-ai/glm-5.2 | 6.7% | 87.5% | 51.7% | 76.2s | [1.6%, 23.7%] | 12.5% | 3 | 21 | 24 | n=5 |
| openrouter/anthropic/claude-opus-4.8 | 66.7% | 83.3% | 66.7% | 0.0s | [30.0%, 90.3%] | 66.7% | 4 | 5 | 6 | n=1 |
| openrouter/anthropic/claude-sonnet-4.6 | 0.0% | 70.8% | 0.0% | 0.0s | [0.0%, 13.8%] | 0.0% | 0 | 17 | 24 | n=1 |
| openrouter/deepseek/deepseek-v4-flash | 0.0% | 58.3% | 0.0% | 0.0s | [0.0%, 13.8%] | 0.0% | 0 | 14 | 24 | n=1 |
| openrouter/deepseek/deepseek-v4-pro | 4.2% | 58.3% | 4.2% | 0.0s | [0.7%, 20.2%] | 4.2% | 1 | 14 | 24 | n=1 |
| openrouter/google/gemma-4-31b-it | 0.0% | 33.3% | 0.0% | 0.0s | [0.0%, 13.8%] | 0.0% | 0 | 8 | 24 | n=1 |
| openrouter/openai/gpt-oss-120b | 0.0% | 70.8% | 0.0% | 0.0s | [0.0%, 13.8%] | 0.0% | 0 | 17 | 24 | n=1 |
| openrouter/qwen/qwen3-235b-a22b-2507 | 0.0% | 70.8% | 0.0% | 0.0s | [0.0%, 13.8%] | 0.0% | 0 | 17 | 24 | n=1 |

*pass@1 (full) = all layers must pass. pass@1 (quality) = L0+L3 only (code quality, ignoring build/runtime).*

## Tier Breakdown

| Tier | pass@1 | Passed | Total |
|------|--------|--------|-------|
| Core | 12.5% | 3 | 24 |
| Core | 66.7% | 4 | 6 |
| Core | 0.0% | 0 | 24 |
| Core | 0.0% | 0 | 24 |
| Core | 4.2% | 1 | 24 |
| Core | 0.0% | 0 | 24 |
| Core | 0.0% | 0 | 24 |
| Core | 0.0% | 0 | 24 |

## Reasoning Type Breakdown

| Reasoning Type | pass@1 | Cases | LLM Reliability |
|----------------|--------|-------|-----------------|
| L1 API Recall | 12.5% | 24 | Expert review required |
| L2 Rule Application | 12.5% | 24 | Expert review required |
| L4 System Reasoning | 12.5% | 24 | Expert review required |
| L1 API Recall | 66.7% | 6 | Expert review required |
| L2 Rule Application | 66.7% | 6 | Expert review required |
| L4 System Reasoning | 66.7% | 6 | Expert review required |
| L1 API Recall | 0.0% | 24 | Expert review required |
| L2 Rule Application | 0.0% | 24 | Expert review required |
| L4 System Reasoning | 0.0% | 24 | Expert review required |
| L1 API Recall | 0.0% | 24 | Expert review required |
| L2 Rule Application | 0.0% | 24 | Expert review required |
| L4 System Reasoning | 0.0% | 24 | Expert review required |
| L1 API Recall | 4.2% | 24 | Expert review required |
| L2 Rule Application | 4.2% | 24 | Expert review required |
| L4 System Reasoning | 4.2% | 24 | Expert review required |
| L1 API Recall | 0.0% | 24 | Expert review required |
| L2 Rule Application | 0.0% | 24 | Expert review required |
| L4 System Reasoning | 0.0% | 24 | Expert review required |
| L1 API Recall | 0.0% | 24 | Expert review required |
| L2 Rule Application | 0.0% | 24 | Expert review required |
| L4 System Reasoning | 0.0% | 24 | Expert review required |
| L1 API Recall | 0.0% | 24 | Expert review required |
| L2 Rule Application | 0.0% | 24 | Expert review required |
| L4 System Reasoning | 0.0% | 24 | Expert review required |

## SDK Breakdown

| SDK | pass@1 | Passed | Total | Notes |
|-----|--------|--------|-------|-------|
| mcuxpresso-sdk | 12.5% | 3 | 24 |  |
| mcuxpresso-sdk | 66.7% | 4 | 6 | thin bucket (n<8) |
| mcuxpresso-sdk | 0.0% | 0 | 24 |  |
| mcuxpresso-sdk | 0.0% | 0 | 24 |  |
| mcuxpresso-sdk | 4.2% | 1 | 24 |  |
| mcuxpresso-sdk | 0.0% | 0 | 24 |  |
| mcuxpresso-sdk | 0.0% | 0 | 24 |  |
| mcuxpresso-sdk | 0.0% | 0 | 24 |  |

## Category Results

| Category | pass@1 | Passed | Total | Status |
|----------|--------|--------|-------|--------|
| audio | 0.0% | 0 | 3 | FAIL |
| dma | 0.0% | 0 | 1 | FAIL |
| gpio-basic | 25.0% | 1 | 4 | FAIL |
| isr-concurrency | 50.0% | 1 | 2 | PARTIAL |
| spi-i2c | 0.0% | 0 | 5 | FAIL |
| storage | 0.0% | 0 | 2 | FAIL |
| timer | 50.0% | 1 | 2 | PARTIAL |
| uart | 0.0% | 0 | 3 | FAIL |
| watchdog | 0.0% | 0 | 2 | FAIL |
| gpio-basic | 100.0% | 2 | 2 | PASS |
| spi-i2c | 100.0% | 2 | 2 | PASS |
| storage | 0.0% | 0 | 2 | FAIL |
| audio | 0.0% | 0 | 3 | FAIL |
| dma | 0.0% | 0 | 1 | FAIL |
| gpio-basic | 0.0% | 0 | 4 | FAIL |
| isr-concurrency | 0.0% | 0 | 2 | FAIL |
| spi-i2c | 0.0% | 0 | 5 | FAIL |
| storage | 0.0% | 0 | 2 | FAIL |
| timer | 0.0% | 0 | 2 | FAIL |
| uart | 0.0% | 0 | 3 | FAIL |
| watchdog | 0.0% | 0 | 2 | FAIL |
| audio | 0.0% | 0 | 3 | FAIL |
| dma | 0.0% | 0 | 1 | FAIL |
| gpio-basic | 0.0% | 0 | 4 | FAIL |
| isr-concurrency | 0.0% | 0 | 2 | FAIL |
| spi-i2c | 0.0% | 0 | 5 | FAIL |
| storage | 0.0% | 0 | 2 | FAIL |
| timer | 0.0% | 0 | 2 | FAIL |
| uart | 0.0% | 0 | 3 | FAIL |
| watchdog | 0.0% | 0 | 2 | FAIL |
| audio | 0.0% | 0 | 3 | FAIL |
| dma | 0.0% | 0 | 1 | FAIL |
| gpio-basic | 0.0% | 0 | 4 | FAIL |
| isr-concurrency | 50.0% | 1 | 2 | PARTIAL |
| spi-i2c | 0.0% | 0 | 5 | FAIL |
| storage | 0.0% | 0 | 2 | FAIL |
| timer | 0.0% | 0 | 2 | FAIL |
| uart | 0.0% | 0 | 3 | FAIL |
| watchdog | 0.0% | 0 | 2 | FAIL |
| audio | 0.0% | 0 | 3 | FAIL |
| dma | 0.0% | 0 | 1 | FAIL |
| gpio-basic | 0.0% | 0 | 4 | FAIL |
| isr-concurrency | 0.0% | 0 | 2 | FAIL |
| spi-i2c | 0.0% | 0 | 5 | FAIL |
| storage | 0.0% | 0 | 2 | FAIL |
| timer | 0.0% | 0 | 2 | FAIL |
| uart | 0.0% | 0 | 3 | FAIL |
| watchdog | 0.0% | 0 | 2 | FAIL |
| audio | 0.0% | 0 | 3 | FAIL |
| dma | 0.0% | 0 | 1 | FAIL |
| gpio-basic | 0.0% | 0 | 4 | FAIL |
| isr-concurrency | 0.0% | 0 | 2 | FAIL |
| spi-i2c | 0.0% | 0 | 5 | FAIL |
| storage | 0.0% | 0 | 2 | FAIL |
| timer | 0.0% | 0 | 2 | FAIL |
| uart | 0.0% | 0 | 3 | FAIL |
| watchdog | 0.0% | 0 | 2 | FAIL |
| audio | 0.0% | 0 | 3 | FAIL |
| dma | 0.0% | 0 | 1 | FAIL |
| gpio-basic | 0.0% | 0 | 4 | FAIL |
| isr-concurrency | 0.0% | 0 | 2 | FAIL |
| spi-i2c | 0.0% | 0 | 5 | FAIL |
| storage | 0.0% | 0 | 2 | FAIL |
| timer | 0.0% | 0 | 2 | FAIL |
| uart | 0.0% | 0 | 3 | FAIL |
| watchdog | 0.0% | 0 | 2 | FAIL |

## Layer Pass Rate Heatmap

| Model| L0 Static| L1 Build| L2 Runtime| L3 Heuristic| L4 Mutation| |
|-------|----------|----------|----------|----------|----------||
| openrouter/z-ai/glm-5.2| 77%| 13%| 100%| 67%| 75%| |
| openrouter/anthropic/claude-opus-4.8| 83%| 80%| 100%| 100%| 100%| |
| openrouter/anthropic/claude-sonnet-4.6| 83%| 15%| 100%| 0%| -| |
| openrouter/deepseek/deepseek-v4-flash| 58%| 0%| -| -| -| |
| openrouter/deepseek/deepseek-v4-pro| 58%| 7%| 100%| 100%| 100%| |
| openrouter/google/gemma-4-31b-it| 33%| 0%| -| -| -| |
| openrouter/openai/gpt-oss-120b| 71%| 0%| -| -| -| |
| openrouter/qwen/qwen3-235b-a22b-2507| 71%| 0%| -| -| -| |

## Failure Distribution

| Layer | Failures | % of Total |
|-------|----------|-----------|
| L0 Static | 2.6 | 24% |
| L1 Build | 6.8 | 62% |
| L2 Runtime | 0.0 | 0% |
| L3 Heuristic | 1.3 | 12% |
| L4 Mutation | 0.2 | 2% |

## Category Breakdown

| Category | Pass@1 | Cases |
|----------|--------|-------|
| audio | 0% | 3 |
| dma | 0% | 1 |
| gpio-basic | 25% | 4 |
| isr-concurrency | 50% | 2 |
| spi-i2c | 0% | 5 |
| storage | 0% | 2 |
| timer | 50% | 2 |
| uart | 0% | 3 |
| watchdog | 0% | 2 |
| gpio-basic | 100% | 2 |
| spi-i2c | 100% | 2 |
| storage | 0% | 2 |
| audio | 0% | 3 |
| dma | 0% | 1 |
| gpio-basic | 0% | 4 |
| isr-concurrency | 0% | 2 |
| spi-i2c | 0% | 5 |
| storage | 0% | 2 |
| timer | 0% | 2 |
| uart | 0% | 3 |
| watchdog | 0% | 2 |
| audio | 0% | 3 |
| dma | 0% | 1 |
| gpio-basic | 0% | 4 |
| isr-concurrency | 0% | 2 |
| spi-i2c | 0% | 5 |
| storage | 0% | 2 |
| timer | 0% | 2 |
| uart | 0% | 3 |
| watchdog | 0% | 2 |
| audio | 0% | 3 |
| dma | 0% | 1 |
| gpio-basic | 0% | 4 |
| isr-concurrency | 50% | 2 |
| spi-i2c | 0% | 5 |
| storage | 0% | 2 |
| timer | 0% | 2 |
| uart | 0% | 3 |
| watchdog | 0% | 2 |
| audio | 0% | 3 |
| dma | 0% | 1 |
| gpio-basic | 0% | 4 |
| isr-concurrency | 0% | 2 |
| spi-i2c | 0% | 5 |
| storage | 0% | 2 |
| timer | 0% | 2 |
| uart | 0% | 3 |
| watchdog | 0% | 2 |
| audio | 0% | 3 |
| dma | 0% | 1 |
| gpio-basic | 0% | 4 |
| isr-concurrency | 0% | 2 |
| spi-i2c | 0% | 5 |
| storage | 0% | 2 |
| timer | 0% | 2 |
| uart | 0% | 3 |
| watchdog | 0% | 2 |
| audio | 0% | 3 |
| dma | 0% | 1 |
| gpio-basic | 0% | 4 |
| isr-concurrency | 0% | 2 |
| spi-i2c | 0% | 5 |
| storage | 0% | 2 |
| timer | 0% | 2 |
| uart | 0% | 3 |
| watchdog | 0% | 2 |
