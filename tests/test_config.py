from app.config import DEFAULT_ALLOWED_MCP_TOOLS, Settings, _split_tools


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
