"""Data models for benchmark results."""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class BenchmarkResult:
    """Result of a single benchmark run."""

    model: str
    ttft_ms: float
    generation_speed: float
    total_latency_ms: float
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    success: bool = True
    error: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "model": self.model,
            "ttft_ms": self.ttft_ms,
            "generation_speed": self.generation_speed,
            "total_latency_ms": self.total_latency_ms,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "success": self.success,
            "error": self.error,
        }


@dataclass
class ModelStats:
    """Aggregated statistics for a model across multiple runs."""

    model: str
    ttft_avg: float
    ttft_std: float
    speed_avg: float
    speed_std: float
    latency_avg: float
    latency_std: float
    tokens_avg: float
    runs: int
    successful_runs: int

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "model": self.model,
            "ttft_avg_ms": self.ttft_avg,
            "ttft_std_ms": self.ttft_std,
            "speed_avg_tokens_per_sec": self.speed_avg,
            "speed_std_tokens_per_sec": self.speed_std,
            "latency_avg_ms": self.latency_avg,
            "latency_std_ms": self.latency_std,
            "tokens_avg": self.tokens_avg,
            "runs": self.runs,
            "successful_runs": self.successful_runs,
        }


@dataclass
class BenchmarkConfig:
    """Configuration for benchmark runs."""

    api_key: str
    models: list[str]
    runs: int = 3
    warmup_runs: int = 1
    max_tokens: int = 256
    prompt: str = (
        "Write a Python function that implements a binary search tree "
        "with insert, delete, and search operations. Include proper "
        "type hints and docstrings."
    )
    endpoint: str = "https://api.z.ai/api/coding/paas/v4/chat/completions"
    timeout: float = 60.0


@dataclass
class StreamChunk:
    """A chunk from the streaming response."""

    content: str = ""
    finish_reason: Optional[str] = None
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


FALLBACK_MODELS: list[str] = [
    "glm-5",
    "glm-4.7",
    "glm-4.7-flash",
    "glm-4.6",
    "glm-4.6-air",
    "glm-4.5",
    "glm-4.5-air",
]
