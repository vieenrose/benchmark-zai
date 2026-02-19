# OpenCode Plugin for Z.AI Benchmark

This directory contains OpenCode integration for the Z.AI Model Benchmark CLI.

## Files

```
.opencode/
├── tools/
│   ├── zai-benchmark.ts    # Run benchmarks
│   └── zai-models.ts       # List available models
└── skills/
    └── zai-benchmark/
        └── SKILL.md        # Usage instructions
```

## Installation

The tools and skills are automatically loaded when you run OpenCode in this project.

## Usage in OpenCode

### List Available Models

```
Use zai-models to show me available Z.AI models
```

### Run Benchmark

```
Run zai-benchmark to benchmark all Z.AI models
```

### Run Benchmark on Specific Models

```
Run zai-benchmark with models "glm-5,glm-4.7" for 5 runs
```

### Get JSON Output

```
Run zai-benchmark with output "json" and save the results
```

## Prerequisites

Before running benchmarks, set your Z.AI API key:

```bash
export ZAI_API_KEY=your_api_key
```

## Tool Arguments

### zai-benchmark

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `models` | string | all | Comma-separated model list |
| `runs` | number | 3 | Benchmark runs per model |
| `max_tokens` | number | 256 | Maximum tokens to generate |
| `output` | string | "table" | Output format: "table" or "json" |

### zai-models

No arguments required.
