"""Core benchmark logic for measuring model performance."""

import json
import time
from collections.abc import AsyncIterator
from typing import Optional

import httpx

from .models import FALLBACK_MODELS, BenchmarkConfig, BenchmarkResult, StreamChunk


class BenchmarkError(Exception):
    """Base exception for benchmark errors."""

    pass


class APIError(BenchmarkError):
    """API request failed."""

    pass


class StreamingError(BenchmarkError):
    """Streaming response parsing failed."""

    pass


async def fetch_available_models(api_key: str, timeout: float = 10.0) -> list[str]:
    """Fetch available models from the API.

    Args:
        api_key: Z.AI API key.
        timeout: Request timeout in seconds.

    Returns:
        List of available model IDs.

    Raises:
        APIError: If the API request fails.
    """
    base_url = "https://api.z.ai/api/coding/paas/v4"
    models_url = f"{base_url}/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(models_url, headers=headers, timeout=timeout)
            response.raise_for_status()
            data = response.json()

            models = []
            for model in data.get("data", []):
                model_id = model.get("id", "")
                if model_id:
                    models.append(model_id)

            return sorted(models) if models else FALLBACK_MODELS.copy()

        except (httpx.HTTPStatusError, httpx.RequestError, json.JSONDecodeError):
            return FALLBACK_MODELS.copy()


async def _parse_stream_chunk(line: bytes) -> Optional[StreamChunk]:
    """Parse a single SSE line into a StreamChunk.

    Args:
        line: Raw bytes from the stream.

    Returns:
        StreamChunk if valid data, None if skip line.
    """
    line_str = line.decode("utf-8", errors="replace").strip()

    if not line_str or line_str == "data: [DONE]":
        return None

    if not line_str.startswith("data: "):
        return None

    json_str = line_str[6:]
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return None

    chunk = StreamChunk()

    if data.get("choices"):
        choice = data["choices"][0]
        delta = choice.get("delta", {})
        # Include both content and reasoning_content for thinking models
        content = delta.get("content", "")
        reasoning = delta.get("reasoning_content", "")
        chunk.content = content + reasoning
        chunk.finish_reason = choice.get("finish_reason")

    if "usage" in data:
        usage = data["usage"]
        chunk.prompt_tokens = usage.get("prompt_tokens", 0)
        chunk.completion_tokens = usage.get("completion_tokens", 0)
        chunk.total_tokens = usage.get("total_tokens", 0)

    return chunk


async def stream_response(
    client: httpx.AsyncClient,
    config: BenchmarkConfig,
    model: str,
) -> AsyncIterator[StreamChunk]:
    """Stream response from the API.

    Args:
        client: Async HTTP client.
        config: Benchmark configuration.
        model: Model to test.

    Yields:
        StreamChunk objects as they arrive.

    Raises:
        APIError: If the API request fails.
    """
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": config.prompt}],
        "max_tokens": config.max_tokens,
        "stream": True,
    }
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with client.stream(
            "POST",
            config.endpoint,
            json=payload,
            headers=headers,
            timeout=config.timeout,
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.strip():
                    chunk = await _parse_stream_chunk(line.encode())
                    if chunk:
                        yield chunk
    except httpx.HTTPStatusError as e:
        raise APIError(f"API request failed: {e.response.status_code}") from e
    except httpx.RequestError as e:
        raise APIError(f"Request error: {e}") from e


async def benchmark_model(
    client: httpx.AsyncClient,
    config: BenchmarkConfig,
    model: str,
) -> BenchmarkResult:
    """Run a single benchmark for a model.

    Args:
        client: Async HTTP client.
        config: Benchmark configuration.
        model: Model to benchmark.

    Returns:
        BenchmarkResult with timing metrics.
    """
    start_time = time.perf_counter()
    ttft_time: Optional[float] = None
    completion_tokens = 0
    prompt_tokens = 0
    total_tokens = 0
    content_length = 0  # Track content length for token estimation

    try:
        async for chunk in stream_response(client, config, model):
            if chunk.content and ttft_time is None:
                ttft_time = time.perf_counter()

            if chunk.content:
                content_length += len(chunk.content)

            if chunk.prompt_tokens:
                prompt_tokens = chunk.prompt_tokens
            if chunk.completion_tokens:
                completion_tokens = chunk.completion_tokens
            if chunk.total_tokens:
                total_tokens = chunk.total_tokens

        end_time = time.perf_counter()

        if ttft_time is None:
            ttft_time = end_time

        ttft_ms = (ttft_time - start_time) * 1000
        total_latency_ms = (end_time - start_time) * 1000

        generation_time = (
            (end_time - ttft_time) if ttft_time else (end_time - start_time)
        )

        # Estimate tokens if API didn't provide them (~4 chars per token)
        if completion_tokens == 0 and content_length > 0:
            completion_tokens = max(1, content_length // 4)

        if generation_time > 0:
            generation_speed = completion_tokens / generation_time
        else:
            generation_speed = 0.0

        return BenchmarkResult(
            model=model,
            ttft_ms=ttft_ms,
            generation_speed=generation_speed,
            total_latency_ms=total_latency_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            success=True,
        )

    except (APIError, StreamingError) as e:
        end_time = time.perf_counter()
        return BenchmarkResult(
            model=model,
            ttft_ms=0.0,
            generation_speed=0.0,
            total_latency_ms=(end_time - start_time) * 1000,
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
            success=False,
            error=str(e),
        )


async def warmup(
    client: httpx.AsyncClient,
    config: BenchmarkConfig,
    model: str,
) -> None:
    """Run warmup requests to prime the model.

    Args:
        client: Async HTTP client.
        config: Benchmark configuration.
        model: Model to warm up.
    """
    for _ in range(config.warmup_runs):
        try:
            async for _ in stream_response(client, config, model):
                pass
        except APIError:
            pass


async def run_benchmarks(config: BenchmarkConfig) -> list[BenchmarkResult]:
    """Run benchmarks for all configured models.

    Args:
        config: Benchmark configuration.

    Returns:
        List of all benchmark results.
    """
    results: list[BenchmarkResult] = []

    async with httpx.AsyncClient() as client:
        for model in config.models:
            await warmup(client, config, model)

            for _run in range(config.runs):
                result = await benchmark_model(client, config, model)
                results.append(result)

    return results
