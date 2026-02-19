---
name: zai-benchmark
description: Run Z.AI model benchmarks to measure TTFT, generation speed, and latency
license: MIT
compatibility: opencode
---

## Z.AI Model Benchmark

This skill provides tools to benchmark Z.AI Coding Plan models.

### Available Tools

1. **zai-benchmark** - Run a full benchmark on Z.AI models
2. **zai-models** - List available models

### Prerequisites

Before running benchmarks, set your Z.AI API key:

```bash
export ZAI_API_KEY=your_api_key
```

### Usage Examples

**List available models:**
```
Use zai-models to show me available Z.AI models
```

**Run benchmark on all models:**
```
Run zai-benchmark to benchmark all Z.AI models
```

**Run benchmark on specific models:**
```
Run zai-benchmark with models "glm-5,glm-4.7" for 5 runs
```

**Get JSON output:**
```
Run zai-benchmark with output "json" and save the results
```

### Metrics Explained

| Metric | Description |
|--------|-------------|
| **TTFT** | Time to First Token - latency until first token arrives |
| **Speed** | Generation speed in tokens per second |
| **Latency** | Total end-to-end request time |
| **Success** | Successful runs / total runs |

### Model Recommendations

Based on benchmark results:

- **Fastest overall**: `glm-4.6` - Best TTFT and generation speed
- **Best value**: `glm-4.5-air` - Fast with potentially lower cost
- **Complex tasks**: `glm-5` - Deep reasoning (slower but higher quality)

### When to Use

Use this skill when:
- You need to compare Z.AI model performance
- You want to find the fastest model for a task
- You're optimizing for latency or throughput
- You need to benchmark new Z.AI models
