# AGENTS.md

Guidelines for agentic coding agents working in this repository.

## Project Overview

Python CLI tool for benchmarking Z.AI Coding Plan models:
- **TTFT (Time to First Token)** - Latency until first token
- **Generation Speed** - Output tokens per second
- **Total Latency** - End-to-end request time

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Commands

### Running the CLI

```bash
benchmark-zai --api-key YOUR_KEY
python -m benchmark_zai --models glm-5,glm-4.7 --runs 5 --output json
export ZAI_API_KEY=your_key && benchmark-zai
```

### Testing

```bash
pytest                                    # Run all tests
pytest -v                                 # Verbose output
pytest tests/test_benchmark.py            # Single file
pytest tests/test_benchmark.py::test_ttft -v  # Single test
pytest -k "streaming" -v                  # Pattern match
pytest --cov=benchmark_zai --cov-report=term-missing  # With coverage
```

### Linting and Type Checking

```bash
ruff check .              # Lint
ruff check . --fix        # Auto-fix
ruff format .             # Format
mypy src/                 # Type check
```

### Build

```bash
pip install -e ".[dev]"   # Dev install
python -m build           # Build package
```

## Code Style Guidelines

### Imports

Three groups, separated by blank lines:

```python
# Standard library
import asyncio
from typing import Any

# Third-party
import httpx
from rich.console import Console

# Local imports
from .models import BenchmarkResult
```

- `from x import y` for ≤3 items, `import x` otherwise
- No `from x import *`
- Alphabetical within groups

### Formatting

- Line length: 88 characters
- Indentation: 4 spaces
- Double quotes for strings, single for dict keys/f-strings
- Trailing commas in multi-line collections

### Type Hints

All public functions must have type hints:

```python
def benchmark_model(
    client: httpx.AsyncClient,
    model: str,
    prompt: str,
    max_tokens: int = 256,
) -> BenchmarkResult:
    ...
```

- Use `list[str]`, `dict[str, Any]` (not `List`, `Dict`)
- Use `T | None` or `Optional[T]` for nullable

### Naming Conventions

```python
calculate_ttft()          # Functions: snake_case
total_latency = 0         # Variables: snake_case
DEFAULT_MAX_TOKENS = 256  # Constants: UPPER_SNAKE_CASE
class BenchmarkRunner:    # Classes: PascalCase
def _stream_response():   # Private: underscore prefix
```

### Error Handling

```python
class BenchmarkError(Exception):
    """Base exception for benchmark errors."""
    pass

def main() -> int:
    try:
        api_key = get_api_key()
    except APIKeyError as e:
        console.print(f"[red]Error:[/red] {e}")
        return 1
    return 0
```

- Catch specific exceptions, not bare `except:`
- Return exit codes from `main()`
- Use `async with` for async resources

### Docstrings

Google-style for public functions:

```python
def benchmark_model(client: httpx.AsyncClient, model: str) -> BenchmarkResult:
    """Run a benchmark for a single model.

    Args:
        client: Async HTTP client for requests.
        model: Model identifier (e.g., "glm-5").

    Returns:
        BenchmarkResult with TTFT, speed, and latency metrics.

    Raises:
        httpx.HTTPStatusError: If API request fails.
    """
    ...
```

## Project Structure

```
/Users/luigi/test/
├── AGENTS.md
├── pyproject.toml
├── README.md
├── src/benchmark_zai/
│   ├── __init__.py
│   ├── __main__.py    # Entry point
│   ├── cli.py         # CLI args
│   ├── benchmark.py   # Core logic
│   ├── models.py      # Data classes
│   └── utils.py
├── tests/
│   ├── conftest.py
│   ├── test_benchmark.py
│   ├── test_cli.py
│   └── test_utils.py
└── .venv/
```

## Important Notes

- Never commit API keys or secrets
- Run `ruff check .` and `mypy src/` after changes
- Write tests for new functionality
- Keep functions < 50 lines
- Use async/await for all API calls
