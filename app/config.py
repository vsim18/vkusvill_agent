import os
from dataclasses import dataclass, field
from typing import Any

from dotenv import load_dotenv

VKUSVILL_MCP_URL = "https://mcp.vkusvill.ru/mcp"
VKUSVILL_MCP_SERVER_LABEL = "vkusvill"
DEFAULT_OPENAI_MODEL = "gpt-5-mini"
DEFAULT_ALLOWED_MCP_TOOLS = (
    "vkusvill_products_search",
    "vkusvill_products_discount",
    "vkusvill_product_details",
    "vkusvill_product_analogs",
    "vkusvill_cart_link_create",
)


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    telegram_bot_token: str
    openai_model: str = DEFAULT_OPENAI_MODEL
    vkusvill_mcp_url: str = VKUSVILL_MCP_URL
    vkusvill_mcp_server_label: str = VKUSVILL_MCP_SERVER_LABEL
    allowed_mcp_tools: tuple[str, ...] = field(default_factory=lambda: DEFAULT_ALLOWED_MCP_TOOLS)

    def mcp_tool_config(self) -> dict[str, Any]:
        return {
            "type": "mcp",
            "server_label": self.vkusvill_mcp_server_label,
            "server_url": self.vkusvill_mcp_url,
            "allowed_tools": list(self.allowed_mcp_tools),
            "require_approval": "never",
            "server_description": (
                "Official VkusVill MCP server for product search and cart link creation."
            ),
        }


def _split_tools(raw_tools: str | None) -> tuple[str, ...]:
    if not raw_tools:
        return DEFAULT_ALLOWED_MCP_TOOLS

    tools = tuple(tool.strip() for tool in raw_tools.split(",") if tool.strip())
    return tools or DEFAULT_ALLOWED_MCP_TOOLS


def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        openai_model=os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL),
        vkusvill_mcp_url=os.getenv("VKUSVILL_MCP_URL", VKUSVILL_MCP_URL),
        vkusvill_mcp_server_label=os.getenv("VKUSVILL_MCP_SERVER_LABEL", VKUSVILL_MCP_SERVER_LABEL),
        allowed_mcp_tools=_split_tools(os.getenv("VKUSVILL_ALLOWED_MCP_TOOLS")),
    )


def validate_runtime_settings(settings: Settings) -> None:
    missing = []
    if not settings.openai_api_key:
        missing.append("OPENAI_API_KEY")
    if not settings.telegram_bot_token:
        missing.append("TELEGRAM_BOT_TOKEN")
    if missing:
        missing_vars = ", ".join(missing)
        msg = f"Missing required environment variables: {missing_vars}"
        raise RuntimeError(msg)
