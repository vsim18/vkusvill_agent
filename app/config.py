import os
from dataclasses import dataclass, field
from typing import Any

from dotenv import load_dotenv

VKUSVILL_MCP_URL = "https://mcp.vkusvill.ru/mcp"
VKUSVILL_MCP_SERVER_LABEL = "vkusvill"
TBANK_MCP_SERVER_LABEL = "tbank"
DEFAULT_OPENAI_MODEL = "gpt-6-luna"
DEFAULT_TELEGRAM_TIMEOUT_SECONDS = 30.0
DEFAULT_TELEGRAM_POOL_TIMEOUT_SECONDS = 5.0
DEFAULT_ALLOWED_MCP_TOOLS = (
    "vkusvill_products_search",
    "vkusvill_products_discount",
    "vkusvill_product_details",
    "vkusvill_product_analogs",
    "vkusvill_recipes",
    "vkusvill_cart_link_create",
)
# Grocery-only subset of tbank-mcp tools. Checkout / order management and all
# banking tools stay out on purpose: the bot may fill a cart, never place or
# pay for an order.
DEFAULT_TBANK_ALLOWED_TOOLS = (
    "grocery_stores",
    "grocery_search",
    "grocery_plan_order",
    "grocery_rank",
    "grocery_good_info",
    "grocery_add_to_cart",
    "grocery_set_cart",
    "grocery_cart",
)


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    telegram_bot_token: str
    openai_model: str = DEFAULT_OPENAI_MODEL
    vkusvill_mcp_url: str = VKUSVILL_MCP_URL
    vkusvill_mcp_server_label: str = VKUSVILL_MCP_SERVER_LABEL
    allowed_mcp_tools: tuple[str, ...] = field(default_factory=lambda: DEFAULT_ALLOWED_MCP_TOOLS)
    tbank_tunnel_id: str | None = None
    tbank_mcp_server_label: str = TBANK_MCP_SERVER_LABEL
    tbank_allowed_mcp_tools: tuple[str, ...] = field(
        default_factory=lambda: DEFAULT_TBANK_ALLOWED_TOOLS
    )
    telegram_connect_timeout: float = DEFAULT_TELEGRAM_TIMEOUT_SECONDS
    telegram_read_timeout: float = DEFAULT_TELEGRAM_TIMEOUT_SECONDS
    telegram_write_timeout: float = DEFAULT_TELEGRAM_TIMEOUT_SECONDS
    telegram_pool_timeout: float = DEFAULT_TELEGRAM_POOL_TIMEOUT_SECONDS
    telegram_proxy_url: str | None = None

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

    def tbank_mcp_tool_config(self) -> dict[str, Any] | None:
        """Second MCP tool for the local tbank-mcp stdio server reached via
        OpenAI Secure MCP Tunnel. Returns None when TBANK_TUNNEL_ID is unset."""
        if not self.tbank_tunnel_id:
            return None
        return {
            "type": "mcp",
            "server_label": self.tbank_mcp_server_label,
            "tunnel_id": self.tbank_tunnel_id,
            "allowed_tools": list(self.tbank_allowed_mcp_tools),
            "require_approval": "never",
            "server_description": (
                "Local tbank-mcp grocery tools: find a T-Bank store, search products "
                "and fill a T-Bank cart. Checkout is not allowed."
            ),
        }

    def mcp_tools(self) -> list[dict[str, Any]]:
        tools: list[dict[str, Any]] = [self.mcp_tool_config()]
        tbank_tool = self.tbank_mcp_tool_config()
        if tbank_tool is not None:
            tools.append(tbank_tool)
        return tools


def _split_tools(raw_tools: str | None) -> tuple[str, ...]:
    if not raw_tools:
        return DEFAULT_ALLOWED_MCP_TOOLS

    tools = tuple(tool.strip() for tool in raw_tools.split(",") if tool.strip())
    return tools or DEFAULT_ALLOWED_MCP_TOOLS


def _get_float_env(name: str, default: float) -> float:
    raw_value = os.getenv(name)
    if raw_value is None or raw_value.strip() == "":
        return default

    try:
        return float(raw_value)
    except ValueError as exc:
        msg = f"{name} must be a number"
        raise RuntimeError(msg) from exc


def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        openai_model=os.getenv("OPENAI_MODEL", DEFAULT_OPENAI_MODEL),
        vkusvill_mcp_url=os.getenv("VKUSVILL_MCP_URL", VKUSVILL_MCP_URL),
        vkusvill_mcp_server_label=os.getenv("VKUSVILL_MCP_SERVER_LABEL", VKUSVILL_MCP_SERVER_LABEL),
        allowed_mcp_tools=_split_tools(os.getenv("VKUSVILL_ALLOWED_MCP_TOOLS")),
        tbank_tunnel_id=os.getenv("TBANK_TUNNEL_ID", "").strip() or None,
        telegram_connect_timeout=_get_float_env(
            "TELEGRAM_CONNECT_TIMEOUT", DEFAULT_TELEGRAM_TIMEOUT_SECONDS
        ),
        telegram_read_timeout=_get_float_env(
            "TELEGRAM_READ_TIMEOUT", DEFAULT_TELEGRAM_TIMEOUT_SECONDS
        ),
        telegram_write_timeout=_get_float_env(
            "TELEGRAM_WRITE_TIMEOUT", DEFAULT_TELEGRAM_TIMEOUT_SECONDS
        ),
        telegram_pool_timeout=_get_float_env(
            "TELEGRAM_POOL_TIMEOUT", DEFAULT_TELEGRAM_POOL_TIMEOUT_SECONDS
        ),
        telegram_proxy_url=os.getenv("TELEGRAM_PROXY_URL") or None,
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
