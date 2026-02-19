"""CLI argument parsing and main entry point."""

import argparse
import asyncio
import json
import os
import sys
from typing import Any, Optional

from rich.console import Console
from rich.table import Table

from .benchmark import fetch_available_models, run_benchmarks
from .models import FALLBACK_MODELS, BenchmarkConfig
from .utils import calculate_stats, format_json_output, format_table_row


class APIKeyError(Exception):
    """API key is missing or invalid."""

    pass


def get_api_key(key: Optional[str]) -> str:
    """Get API key from argument or environment.

    Args:
        key: API key from command line argument.

    Returns:
        Valid API key string.

    Raises:
        APIKeyError: If no API key is available.
    """
    if key:
        return key

    env_key = os.environ.get("ZAI_API_KEY")
    if env_key:
        return env_key

    raise APIKeyError(
        "API key required. Set ZAI_API_KEY environment variable "
        "or use --api-key argument."
    )


async def get_models(models_str: Optional[str], api_key: str) -> list[str]:
    """Get models to benchmark, fetching dynamically if not specified.

    Args:
        models_str: Comma-separated model names, or None to fetch all.
        api_key: Z.AI API key for fetching models.

    Returns:
        List of model names.
    """
    if models_str:
        models = [m.strip() for m in models_str.split(",")]
        return [m for m in models if m]

    return await fetch_available_models(api_key)


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="benchmark-zai",
        description="Benchmark Z.AI Coding Plan models for TTFT and generation speed.",
    )

    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="Z.AI API key (or set ZAI_API_KEY env var)",
    )

    parser.add_argument(
        "--models",
        type=str,
        default=None,
        help=(
            "Comma-separated list of models to benchmark (default: fetch all from API)"
        ),
    )

    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available models and exit",
    )

    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Number of benchmark runs per model (default: 3)",
    )

    parser.add_argument(
        "--warmup",
        type=int,
        default=1,
        help="Number of warmup runs per model (default: 1)",
    )

    parser.add_argument(
        "--max-tokens",
        type=int,
        default=256,
        help="Maximum tokens to generate (default: 256)",
    )

    parser.add_argument(
        "--output",
        type=str,
        choices=["table", "json"],
        default="table",
        help="Output format (default: table)",
    )

    parser.add_argument(
        "--save",
        type=str,
        default=None,
        help="Save results to JSON file",
    )

    return parser


def display_table(all_stats: list[Any], console: Console) -> None:
    """Display results as a rich table.

    Args:
        all_stats: List of ModelStats objects.
        console: Rich console for output.
    """
    table = Table(title="Z.AI Model Benchmark Results")
    table.add_column("Model", style="cyan", no_wrap=True)
    table.add_column("TTFT (ms)", justify="right")
    table.add_column("Speed (t/s)", justify="right")
    table.add_column("Latency (ms)", justify="right")
    table.add_column("Tokens", justify="right")
    table.add_column("Success", justify="right")

    for stats in all_stats:
        row = format_table_row(stats)
        table.add_row(*row)

    console.print(table)


def display_json(all_stats: list[Any], console: Console) -> None:
    """Display results as JSON.

    Args:
        all_stats: List of ModelStats objects.
        console: Rich console for output.
    """
    output = format_json_output(all_stats)
    console.print_json(json.dumps(output, indent=2))


def save_results(all_stats: list[Any], filepath: str) -> None:
    """Save results to JSON file.

    Args:
        all_stats: List of ModelStats objects.
        filepath: Path to output file.
    """
    output = format_json_output(all_stats)
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2)


def main() -> int:
    """Main entry point for the CLI.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    parser = create_parser()
    args = parser.parse_args()

    console = Console()

    try:
        api_key = get_api_key(args.api_key)
    except APIKeyError as e:
        console.print(f"[red]Error:[/red] {e}")
        return 1

    if args.list_models:
        models = asyncio.run(fetch_available_models(api_key))
        console.print("[bold]Available models:[/bold]")
        for model in models:
            console.print(f"  • {model}")
        return 0

    models = asyncio.run(get_models(args.models, api_key))

    if not models:
        console.print("[red]Error:[/red] No models found")
        console.print(f"Fallback models: {', '.join(FALLBACK_MODELS)}")
        return 1

    config = BenchmarkConfig(
        api_key=api_key,
        models=models,
        runs=args.runs,
        warmup_runs=args.warmup,
        max_tokens=args.max_tokens,
    )

    console.print(
        f"[bold]Benchmarking {len(models)} model(s), {args.runs} run(s) each[/bold]"
    )
    console.print()

    results = asyncio.run(run_benchmarks(config))

    stats_by_model: dict[str, list[Any]] = {}
    for result in results:
        if result.model not in stats_by_model:
            stats_by_model[result.model] = []
        stats_by_model[result.model].append(result)

    all_stats = [calculate_stats(r) for r in stats_by_model.values()]

    if args.output == "table":
        display_table(all_stats, console)
    else:
        display_json(all_stats, console)

    if args.save:
        save_results(all_stats, args.save)
        console.print(f"\n[green]Results saved to {args.save}[/green]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
