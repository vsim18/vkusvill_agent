import pytest

from app.config import (
    DEFAULT_ALLOWED_MCP_TOOLS,
    DEFAULT_TBANK_ALLOWED_TOOLS,
    Settings,
    _get_float_env,
    _split_tools,
    load_settings,
)


def test_settings_builds_remote_mcp_tool_config() -> None:
    settings = Settings(openai_api_key="openai-key", telegram_bot_token="telegram-token")

    tool = settings.mcp_tool_config()

    assert tool["type"] == "mcp"
    assert tool["server_label"] == "vkusvill"
    assert tool["server_url"] == "https://mcp.vkusvill.ru/mcp"
    assert tool["allowed_tools"] == list(DEFAULT_ALLOWED_MCP_TOOLS)
    assert tool["require_approval"] == "never"


def test_tbank_tool_absent_without_tunnel_id() -> None:
    settings = Settings(openai_api_key="openai-key", telegram_bot_token="telegram-token")

    assert settings.tbank_mcp_tool_config() is None
    assert settings.mcp_tools() == [settings.mcp_tool_config()]


def test_tbank_tool_uses_tunnel_id_and_grocery_whitelist() -> None:
    settings = Settings(
        openai_api_key="openai-key",
        telegram_bot_token="telegram-token",
        tbank_tunnel_id="tunnel_abc123",
    )

    tool = settings.tbank_mcp_tool_config()

    assert tool is not None
    assert tool["type"] == "mcp"
    assert tool["server_label"] == "tbank"
    assert tool["tunnel_id"] == "tunnel_abc123"
    assert "server_url" not in tool
    assert tool["require_approval"] == "never"
    assert tool["allowed_tools"] == list(DEFAULT_TBANK_ALLOWED_TOOLS)
    assert "grocery_add_to_cart" in tool["allowed_tools"]
    assert "grocery_set_cart" in tool["allowed_tools"]
    assert "grocery_cart" in tool["allowed_tools"]
    assert "grocery_checkout" not in tool["allowed_tools"]
    assert "grocery_order_cancel" not in tool["allowed_tools"]
    assert settings.mcp_tools() == [settings.mcp_tool_config(), tool]


def test_load_settings_reads_tbank_tunnel_id(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TBANK_TUNNEL_ID", "  tunnel_from_env  ")

    settings = load_settings()

    assert settings.tbank_tunnel_id == "tunnel_from_env"


def test_load_settings_treats_blank_tbank_tunnel_id_as_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TBANK_TUNNEL_ID", "   ")

    settings = load_settings()

    assert settings.tbank_tunnel_id is None
    assert settings.tbank_mcp_tool_config() is None


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
