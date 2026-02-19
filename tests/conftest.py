"""Pytest fixtures for benchmark tests."""

import pytest

from benchmark_zai.models import BenchmarkConfig, BenchmarkResult


@pytest.fixture
def sample_config() -> BenchmarkConfig:
    """Create a sample benchmark configuration."""
    return BenchmarkConfig(
        api_key="test-api-key",
        models=["glm-5", "glm-4.7"],
        runs=2,
        warmup_runs=1,
        max_tokens=128,
    )


@pytest.fixture
def successful_result() -> BenchmarkResult:
    """Create a successful benchmark result."""
    return BenchmarkResult(
        model="glm-5",
        ttft_ms=250.5,
        generation_speed=85.2,
        total_latency_ms=3200.0,
        prompt_tokens=50,
        completion_tokens=256,
        total_tokens=306,
        success=True,
    )


@pytest.fixture
def failed_result() -> BenchmarkResult:
    """Create a failed benchmark result."""
    return BenchmarkResult(
        model="glm-5",
        ttft_ms=0.0,
        generation_speed=0.0,
        total_latency_ms=500.0,
        prompt_tokens=0,
        completion_tokens=0,
        total_tokens=0,
        success=False,
        error="API request failed: 401",
    )


@pytest.fixture
def multiple_results(successful_result: BenchmarkResult) -> list[BenchmarkResult]:
    """Create multiple benchmark results for testing statistics."""
    return [
        successful_result,
        BenchmarkResult(
            model="glm-5",
            ttft_ms=260.0,
            generation_speed=82.0,
            total_latency_ms=3300.0,
            prompt_tokens=50,
            completion_tokens=256,
            total_tokens=306,
            success=True,
        ),
        BenchmarkResult(
            model="glm-5",
            ttft_ms=240.0,
            generation_speed=88.5,
            total_latency_ms=3100.0,
            prompt_tokens=50,
            completion_tokens=256,
            total_tokens=306,
            success=True,
        ),
    ]
