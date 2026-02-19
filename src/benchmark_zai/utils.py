"""Utility functions for benchmark calculations."""

import statistics
from typing import Any

from .models import BenchmarkResult, ModelStats


def calculate_stats(results: list[BenchmarkResult]) -> ModelStats:
    """Calculate aggregate statistics from benchmark results.

    Args:
        results: List of benchmark results for a single model.

    Returns:
        ModelStats with averaged metrics and standard deviations.
    """
    successful = [r for r in results if r.success]

    if not successful:
        return ModelStats(
            model=results[0].model if results else "unknown",
            ttft_avg=0.0,
            ttft_std=0.0,
            speed_avg=0.0,
            speed_std=0.0,
            latency_avg=0.0,
            latency_std=0.0,
            tokens_avg=0.0,
            runs=len(results),
            successful_runs=0,
        )

    ttfts = [r.ttft_ms for r in successful]
    speeds = [r.generation_speed for r in successful]
    latencies = [r.total_latency_ms for r in successful]
    tokens = [r.completion_tokens for r in successful]

    return ModelStats(
        model=results[0].model,
        ttft_avg=statistics.mean(ttfts),
        ttft_std=statistics.stdev(ttfts) if len(ttfts) > 1 else 0.0,
        speed_avg=statistics.mean(speeds),
        speed_std=statistics.stdev(speeds) if len(speeds) > 1 else 0.0,
        latency_avg=statistics.mean(latencies),
        latency_std=statistics.stdev(latencies) if len(latencies) > 1 else 0.0,
        tokens_avg=statistics.mean(tokens),
        runs=len(results),
        successful_runs=len(successful),
    )


def format_table_row(stats: ModelStats) -> list[str]:
    """Format model stats as a table row.

    Args:
        stats: Model statistics to format.

    Returns:
        List of formatted string values for table columns.
    """
    return [
        stats.model,
        f"{stats.ttft_avg:.1f} ± {stats.ttft_std:.1f}",
        f"{stats.speed_avg:.1f} ± {stats.speed_std:.1f}",
        f"{stats.latency_avg:.1f} ± {stats.latency_std:.1f}",
        f"{stats.tokens_avg:.0f}",
        f"{stats.successful_runs}/{stats.runs}",
    ]


def format_json_output(all_stats: list[ModelStats]) -> dict[str, Any]:
    """Format all stats as JSON output.

    Args:
        all_stats: List of model statistics.

    Returns:
        Dictionary suitable for JSON serialization.
    """
    return {
        "results": [s.to_dict() for s in all_stats],
        "summary": {
            "total_models": len(all_stats),
            "successful_models": sum(1 for s in all_stats if s.successful_runs > 0),
        },
    }
