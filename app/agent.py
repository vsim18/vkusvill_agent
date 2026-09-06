import logging
from typing import Any, Protocol

from openai import APIConnectionError, APIError, APITimeoutError, AsyncOpenAI

from app.config import Settings
from app.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class VkusVillAgentError(RuntimeError):
    """Raised when the shopping agent cannot return a user-safe response."""


class ResponsesClient(Protocol):
    async def create(self, **kwargs: Any) -> Any: ...


class VkusVillAgent:
    def __init__(self, settings: Settings, responses_client: ResponsesClient | None = None) -> None:
        self._settings = settings
        if responses_client is None:
            openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
            responses_client = openai_client.responses
        self._responses_client = responses_client

    async def run(self, user_message: str) -> str:
        text = user_message.strip()
        if not text:
            return "Напишите, что нужно купить во ВкусВилле."

        try:
            response = await self._responses_client.create(
                model=self._settings.openai_model,
                instructions=SYSTEM_PROMPT,
                input=text,
                tools=[self._settings.mcp_tool_config()],
                max_tool_calls=40,
            )
        except APITimeoutError as exc:
            logger.warning("OpenAI request timed out: %s", exc.__class__.__name__)
            raise VkusVillAgentError("OpenAI request timed out") from exc
        except (APIConnectionError, APIError) as exc:
            logger.warning("OpenAI or MCP request failed: %s", exc.__class__.__name__)
            raise VkusVillAgentError("OpenAI or MCP request failed") from exc

        output_text = getattr(response, "output_text", None)
        if not isinstance(output_text, str) or not output_text.strip():
            logger.warning("OpenAI response did not contain output_text")
            raise VkusVillAgentError("Empty OpenAI response")

        return output_text.strip()
