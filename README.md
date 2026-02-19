# Z.AI Model Benchmark CLI

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python CLI tool for benchmarking Z.AI Coding Plan models. Measure TTFT (Time to First Token), generation speed, and total latency across all available models.

## Features

- **Dynamic Model Discovery** - Automatically fetches available models from Z.AI API
- **Comprehensive Metrics** - TTFT, generation speed (tokens/sec), and total latency
- **Thinking Model Support** - Handles both regular and reasoning models (glm-4.7, glm-5)
- **Multiple Output Formats** - Rich table or JSON
- **Reliable Measurements** - Configurable warmup runs for consistent results
- **Cross-Platform** - Works on Windows, macOS, and Linux

## Installation

```bash
# Clone the repository
git clone https://github.com/vieenrose/benchmark-zai.git
cd benchmark-zai

# Create virtual environment and install
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Usage

```bash
# Basic usage (set API key via environment variable)
export ZAI_API_KEY=your_key
benchmark-zai

# Or pass API key directly
benchmark-zai --api-key YOUR_KEY

# List available models
benchmark-zai --list-models

# Specify models and options
benchmark-zai --models glm-5,glm-4.7 --runs 5 --output json

# Save results to file
benchmark-zai --save results.json
```

## CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--api-key` | env `ZAI_API_KEY` | Z.AI API key |
| `--models` | fetch from API | Comma-separated model list |
| `--runs` | 3 | Benchmark runs per model |
| `--warmup` | 1 | Warmup runs per model |
| `--max-tokens` | 256 | Max tokens to generate |
| `--output` | table | Output format (table/json) |
| `--save` | - | Save results to JSON file |
| `--list-models` | - | List available models and exit |

## Example Output

```
Benchmarking 5 model(s), 3 run(s) each

                          Z.AI Model Benchmark Results                          
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
┃ Model       ┃     TTFT (ms) ┃  Speed (t/s) ┃ Latency (ms) ┃ Tokens ┃ Success ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
│ glm-4.6     │      1610.5 ± │ 138.2 ± 14.4 │     3476.6 ± │    256 │     3/3 │
│             │         204.0 │              │         35.4 │        │         │
│ glm-4.5-air │      1899.1 ± │ 136.1 ± 18.8 │     3803.8 ± │    256 │     3/3 │
│             │         326.4 │              │        346.5 │        │         │
│ glm-4.7     │      2118.1 ± │ 132.5 ± 40.0 │     4169.4 ± │    256 │     3/3 │
│             │         506.9 │              │       1106.6 │        │         │
│ glm-4.5     │      2258.2 ± │   93.4 ± 2.5 │     5000.6 ± │    256 │     3/3 │
│             │         246.6 │              │        294.9 │        │         │
│ glm-5       │     14764.7 ± │   52.7 ± 0.9 │    19623.4 ± │    256 │     2/3 │
│             │       16229.8 │              │      16146.9 │        │         │
└─────────────┴───────────────┴──────────────┴──────────────┴────────┴─────────┘
```

## Performance Comparison

Based on benchmark results (3 runs each, 256 max tokens):

| Model | TTFT (ms) | Speed (t/s) | Latency (ms) | Best For |
|-------|-----------|-------------|--------------|----------|
| **glm-4.6** | ~1,610 | **~138** | ~3,477 | ⚡ Fastest overall |
| **glm-4.5-air** | ~1,899 | ~136 | ~3,804 | 💨 Speed + efficiency |
| **glm-4.7** | ~2,118 | ~133 | ~4,169 | 🧠 Balanced reasoning |
| **glm-4.5** | ~2,258 | ~93 | ~5,001 | 📝 General purpose |
| **glm-5** | ~14,765 | ~53 | ~19,623 | 🎯 Deep reasoning tasks |

### Recommendations

- **Fastest response**: `glm-4.6` - Best TTFT and generation speed
- **Best value**: `glm-4.5-air` - Nearly as fast with potentially lower cost
- **Complex tasks**: `glm-5` - Slower but designed for deep reasoning

## Metrics Explained

| Metric | Description |
|--------|-------------|
| **TTFT** | Time to First Token - latency until the first token arrives |
| **Speed** | Generation speed in tokens per second |
| **Latency** | Total end-to-end request time |
| **Tokens** | Number of tokens generated |
| **Success** | Successful runs / total runs |

## OpenCode Integration

This project includes built-in [OpenCode](https://opencode.ai) tools and skills for running benchmarks directly from your AI coding agent.

### Available Tools

- **`zai-benchmark`** - Run Z.AI model benchmarks
- **`zai-models`** - List available models

### Usage in OpenCode

```
# List available models
Use zai-models to show me available Z.AI models

# Run benchmark on all models
Run zai-benchmark to benchmark all Z.AI models

# Run benchmark on specific models
Run zai-benchmark with models "glm-5,glm-4.7" for 5 runs
```

### Prerequisites

```bash
export ZAI_API_KEY=your_api_key
```

## Development

```bash
# Run tests
pytest -v

# Run tests with coverage
pytest --cov=benchmark_zai --cov-report=term-missing

# Run linting
ruff check .

# Run type checking
mypy src/
```

## Requirements

- Python 3.9+
- httpx >= 0.25.0
- rich >= 13.0.0

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
