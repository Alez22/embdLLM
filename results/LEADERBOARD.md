# EmbedEval Leaderboard

<!-- SCHEMA_VERSION: 1 -->


## Model Comparison

| Model | pass@1 (full) | pass@1 (quality) | 95% CI | pass@5 | Passed | Quality | Total | Samples |
|-------|---------------|------------------|--------|--------|--------|---------|-------|---------|
| groq/openai/gpt-oss-20b | 8.3% | 8.3% | [1.5%, 35.4%] | 8.3% | 1 | 1 | 12 | n=1 |
| groq/llama-3.3-70b-versatile | 0.0% | 0.0% | [0.0%, 24.3%] | 0.0% | 0 | 0 | 12 | n=1 |
| groq/meta-llama/llama-4-scout-17b-16e-instruct | 0.0% | 0.0% | [0.0%, 79.3%] | 0.0% | 0 | 0 | 1 | n=1 |
| groq/openai/gpt-oss-120b | 25.0% | 25.0% | [8.9%, 53.2%] | 25.0% | 3 | 3 | 12 | n=1 |
| groq/qwen/qwen3-32b | 0.0% | 0.0% | [0.0%, 79.3%] | 0.0% | 0 | 0 | 1 | n=1 |

*pass@1 (full) = all layers must pass. pass@1 (quality) = L0+L3 only (code quality, ignoring build/runtime).*

## Tier Breakdown

| Tier | pass@1 | Passed | Total |
|------|--------|--------|-------|
| Core | 8.3% | 1 | 12 |
| Core | 0.0% | 0 | 12 |
| Core | 0.0% | 0 | 1 |
| Core | 25.0% | 3 | 12 |
| Core | 0.0% | 0 | 1 |

## Reasoning Type Breakdown

| Reasoning Type | pass@1 | Cases | LLM Reliability |
|----------------|--------|-------|-----------------|
| L1 API Recall | 8.3% | 12 | Expert review required |
| L2 Rule Application | 8.3% | 12 | Expert review required |
| L4 System Reasoning | 8.3% | 12 | Expert review required |
| L1 API Recall | 0.0% | 12 | Expert review required |
| L2 Rule Application | 0.0% | 12 | Expert review required |
| L4 System Reasoning | 0.0% | 12 | Expert review required |
| L1 API Recall | 0.0% | 1 | Expert review required |
| L2 Rule Application | 0.0% | 1 | Expert review required |
| L4 System Reasoning | 0.0% | 1 | Expert review required |
| L1 API Recall | 25.0% | 12 | Expert review required |
| L2 Rule Application | 25.0% | 12 | Expert review required |
| L4 System Reasoning | 25.0% | 12 | Expert review required |
| L1 API Recall | 0.0% | 1 | Expert review required |
| L2 Rule Application | 0.0% | 1 | Expert review required |
| L4 System Reasoning | 0.0% | 1 | Expert review required |

## SDK Breakdown

| SDK | pass@1 | Passed | Total | Notes |
|-----|--------|--------|-------|-------|
| mcuxpresso-sdk | 8.3% | 1 | 12 |  |
| mcuxpresso-sdk | 0.0% | 0 | 12 |  |
| mcuxpresso-sdk | 0.0% | 0 | 1 | thin bucket (n<8) |
| mcuxpresso-sdk | 25.0% | 3 | 12 |  |
| mcuxpresso-sdk | 0.0% | 0 | 1 | thin bucket (n<8) |

## Category Results

| Category | pass@1 | Passed | Total | Status |
|----------|--------|--------|-------|--------|
| gpio-basic | 50.0% | 1 | 2 | PARTIAL |
| isr-concurrency | 0.0% | 0 | 1 | FAIL |
| spi-i2c | 0.0% | 0 | 3 | FAIL |
| storage | 0.0% | 0 | 2 | FAIL |
| timer | 0.0% | 0 | 1 | FAIL |
| uart | 0.0% | 0 | 2 | FAIL |
| watchdog | 0.0% | 0 | 1 | FAIL |
| gpio-basic | 0.0% | 0 | 2 | FAIL |
| isr-concurrency | 0.0% | 0 | 1 | FAIL |
| spi-i2c | 0.0% | 0 | 3 | FAIL |
| storage | 0.0% | 0 | 2 | FAIL |
| timer | 0.0% | 0 | 1 | FAIL |
| uart | 0.0% | 0 | 2 | FAIL |
| watchdog | 0.0% | 0 | 1 | FAIL |
| spi-i2c | 0.0% | 0 | 1 | FAIL |
| gpio-basic | 50.0% | 1 | 2 | PARTIAL |
| isr-concurrency | 0.0% | 0 | 1 | FAIL |
| spi-i2c | 66.7% | 2 | 3 | PARTIAL |
| storage | 0.0% | 0 | 2 | FAIL |
| timer | 0.0% | 0 | 1 | FAIL |
| uart | 0.0% | 0 | 2 | FAIL |
| watchdog | 0.0% | 0 | 1 | FAIL |
| spi-i2c | 0.0% | 0 | 1 | FAIL |

## Layer Pass Rate Heatmap

| Model| L0 Static| L1 Build| L2 Runtime| L3 Heuristic| L4 Mutation| |
|-------|----------|----------|----------|----------|----------||
| groq/openai/gpt-oss-20b| 17%| 100%| 100%| 50%| 100%| |
| groq/llama-3.3-70b-versatile| 0%| -| -| -| -| |
| groq/meta-llama/llama-4-scout-17b-16e-instruct| 0%| -| -| -| -| |
| groq/openai/gpt-oss-120b| 58%| 100%| 100%| 43%| 100%| |
| groq/qwen/qwen3-32b| 0%| -| -| -| -| |

## Failure Distribution

| Layer | Failures | % of Total |
|-------|----------|-----------|
| L0 Static | 4.2 | 80% |
| L1 Build | 0.0 | 0% |
| L2 Runtime | 0.0 | 0% |
| L3 Heuristic | 1.1 | 20% |
| L4 Mutation | 0.0 | 0% |

## Category Breakdown

| Category | Pass@1 | Cases |
|----------|--------|-------|
| gpio-basic | 50% | 2 |
| isr-concurrency | 0% | 1 |
| spi-i2c | 0% | 3 |
| storage | 0% | 2 |
| timer | 0% | 1 |
| uart | 0% | 2 |
| watchdog | 0% | 1 |
| gpio-basic | 0% | 2 |
| isr-concurrency | 0% | 1 |
| spi-i2c | 0% | 3 |
| storage | 0% | 2 |
| timer | 0% | 1 |
| uart | 0% | 2 |
| watchdog | 0% | 1 |
| spi-i2c | 0% | 1 |
| gpio-basic | 50% | 2 |
| isr-concurrency | 0% | 1 |
| spi-i2c | 67% | 3 |
| storage | 0% | 2 |
| timer | 0% | 1 |
| uart | 0% | 2 |
| watchdog | 0% | 1 |
| spi-i2c | 0% | 1 |

