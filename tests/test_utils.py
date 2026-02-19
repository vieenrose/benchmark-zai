"""Tests for utility functions."""

from benchmark_zai.models import BenchmarkResult, ModelStats
from benchmark_zai.utils import calculate_stats, format_table_row


class TestCalculateStats:
    """Tests for calculate_stats function."""

    def test_calculate_stats_with_successful_results(
        self, multiple_results: list[BenchmarkResult]
    ) -> None:
        """Test statistics calculation with successful results."""
        stats = calculate_stats(multiple_results)

        assert stats.model == "glm-5"
        assert stats.runs == 3
        assert stats.successful_runs == 3
        assert stats.ttft_avg > 0
        assert stats.speed_avg > 0
        assert stats.latency_avg > 0
        assert stats.tokens_avg == 256

    def test_calculate_stats_with_single_result(
        self, successful_result: BenchmarkResult
    ) -> None:
        """Test statistics calculation with single result."""
        stats = calculate_stats([successful_result])

        assert stats.model == "glm-5"
        assert stats.runs == 1
        assert stats.successful_runs == 1
        assert stats.ttft_std == 0.0
        assert stats.speed_std == 0.0

    def test_calculate_stats_with_all_failures(
        self, failed_result: BenchmarkResult
    ) -> None:
        """Test statistics calculation with all failed results."""
        stats = calculate_stats([failed_result, failed_result])

        assert stats.model == "glm-5"
        assert stats.runs == 2
        assert stats.successful_runs == 0
        assert stats.ttft_avg == 0.0
        assert stats.speed_avg == 0.0

    def test_calculate_stats_with_mixed_results(
        self, successful_result: BenchmarkResult, failed_result: BenchmarkResult
    ) -> None:
        """Test statistics calculation with mixed results."""
        stats = calculate_stats([successful_result, failed_result])

        assert stats.model == "glm-5"
        assert stats.runs == 2
        assert stats.successful_runs == 1
        assert stats.ttft_avg == successful_result.ttft_ms


class TestFormatTableRow:
    """Tests for format_table_row function."""

    def test_format_table_row(self) -> None:
        """Test table row formatting."""
        stats = ModelStats(
            model="glm-5",
            ttft_avg=250.5,
            ttft_std=10.2,
            speed_avg=85.3,
            speed_std=3.1,
            latency_avg=3200.0,
            latency_std=100.0,
            tokens_avg=256.0,
            runs=3,
            successful_runs=3,
        )

        row = format_table_row(stats)

        assert row[0] == "glm-5"
        assert "250.5" in row[1]
        assert "85.3" in row[2]
        assert "3/3" in row[5]
