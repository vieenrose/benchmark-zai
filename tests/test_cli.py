"""Tests for CLI functions."""

from benchmark_zai.cli import get_api_key, get_models
from benchmark_zai.models import FALLBACK_MODELS


class TestGetApiKey:
    """Tests for get_api_key function."""

    def test_get_api_key_from_argument(self) -> None:
        """Test getting API key from argument."""
        key = get_api_key("my-test-key")
        assert key == "my-test-key"

    def test_get_api_key_from_environment(self, monkeypatch) -> None:
        """Test getting API key from environment variable."""
        monkeypatch.setenv("ZAI_API_KEY", "env-test-key")
        key = get_api_key(None)
        assert key == "env-test-key"

    def test_get_api_key_argument_overrides_environment(self, monkeypatch) -> None:
        """Test that argument key overrides environment variable."""
        monkeypatch.setenv("ZAI_API_KEY", "env-test-key")
        key = get_api_key("arg-test-key")
        assert key == "arg-test-key"

    def test_get_api_key_missing_raises_error(self, monkeypatch) -> None:
        """Test that missing API key raises error."""
        monkeypatch.delenv("ZAI_API_KEY", raising=False)
        try:
            get_api_key(None)
            raise AssertionError("Should have raised APIKeyError")
        except Exception as e:
            assert "API key required" in str(e)


class TestGetModels:
    """Tests for get_models function."""

    def test_get_models_from_string(self) -> None:
        """Test parsing models from comma-separated string."""
        import asyncio

        models = asyncio.run(get_models("glm-5,glm-4.7", "test-key"))
        assert models == ["glm-5", "glm-4.7"]

    def test_get_models_from_string_with_spaces(self) -> None:
        """Test parsing models with whitespace."""
        import asyncio

        models = asyncio.run(get_models("  glm-5 , glm-4.7  ", "test-key"))
        assert models == ["glm-5", "glm-4.7"]

    def test_get_models_returns_fallback_on_api_error(self) -> None:
        """Test that fallback models are returned on API error."""
        import asyncio

        models = asyncio.run(get_models(None, "invalid-key"))
        assert models == FALLBACK_MODELS
