"""Tests for benchmark core functions."""

import pytest

from benchmark_zai.benchmark import _parse_stream_chunk


class TestParseStreamChunk:
    """Tests for _parse_stream_chunk function."""

    @pytest.mark.asyncio
    async def test_parse_valid_chunk(self) -> None:
        """Test parsing a valid SSE chunk."""
        line = b'data: {"choices":[{"delta":{"content":"Hello"},"finish_reason":null}]}'

        chunk = await _parse_stream_chunk(line)

        assert chunk is not None
        assert chunk.content == "Hello"
        assert chunk.finish_reason is None

    @pytest.mark.asyncio
    async def test_parse_chunk_with_usage(self) -> None:
        """Test parsing chunk with token usage."""
        line = (
            b'data: {"choices":[{"delta":{},"finish_reason":"stop"}],'
            b'"usage":{"prompt_tokens":10,"completion_tokens":20,"total_tokens":30}}'
        )

        chunk = await _parse_stream_chunk(line)

        assert chunk is not None
        assert chunk.finish_reason == "stop"
        assert chunk.prompt_tokens == 10
        assert chunk.completion_tokens == 20
        assert chunk.total_tokens == 30

    @pytest.mark.asyncio
    async def test_parse_done_signal(self) -> None:
        """Test parsing the [DONE] signal."""
        line = b"data: [DONE]"

        chunk = await _parse_stream_chunk(line)

        assert chunk is None

    @pytest.mark.asyncio
    async def test_parse_empty_line(self) -> None:
        """Test parsing empty line."""
        chunk = await _parse_stream_chunk(b"")
        assert chunk is None

    @pytest.mark.asyncio
    async def test_parse_invalid_json(self) -> None:
        """Test parsing invalid JSON."""
        line = b"data: {invalid json}"

        chunk = await _parse_stream_chunk(line)

        assert chunk is None

    @pytest.mark.asyncio
    async def test_parse_non_data_line(self) -> None:
        """Test parsing line without data prefix."""
        chunk = await _parse_stream_chunk(b"some other text")
        assert chunk is None
