import pytest

from app.config import DEFAULT_ALLOWED_MCP_TOOLS, Settings, _get_float_env, _split_tools


def test_settings_builds_remote_mcp_tool_config() -> None:
    settings = Settings(openai_api_key="openai-key", telegram_bot_token="telegram-token")

    tool = settings.mcp_tool_config()

    assert tool["type"] == "mcp"
    assert tool["server_label"] == "vkusvill"
    assert tool["server_url"] == "https://mcp.vkusvill.ru/mcp"
    assert tool["allowed_tools"] == list(DEFAULT_ALLOWED_MCP_TOOLS)
    assert tool["require_approval"] == "never"


def test_split_tools_uses_defaults_for_empty_value() -> None:
    assert _split_tools("") == DEFAULT_ALLOWED_MCP_TOOLS


def test_split_tools_parses_comma_separated_tools() -> None:
    assert _split_tools("search, details,cart") == ("search", "details", "cart")


def test_get_float_env_uses_default_for_missing_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TELEGRAM_READ_TIMEOUT", raising=False)

    assert _get_float_env("TELEGRAM_READ_TIMEOUT", 30.0) == 30.0


def test_get_float_env_parses_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TELEGRAM_READ_TIMEOUT", "45.5")

    assert _get_float_env("TELEGRAM_READ_TIMEOUT", 30.0) == 45.5
