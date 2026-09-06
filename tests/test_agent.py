from types import SimpleNamespace

import pytest
from openai import APIConnectionError

from app.agent import VkusVillAgent, VkusVillAgentError
from app.config import Settings
from app.prompts import SYSTEM_PROMPT


class FakeResponses:
    def __init__(self, response: object | None = None, exc: Exception | None = None) -> None:
        self.response = response
        self.exc = exc
        self.calls: list[dict[str, object]] = []

    async def create(self, **kwargs: object) -> object:
        self.calls.append(kwargs)
        if self.exc is not None:
            raise self.exc
        return self.response


@pytest.mark.asyncio
async def test_agent_calls_responses_api_with_mcp_tool() -> None:
    responses = FakeResponses(SimpleNamespace(output_text="Корзина готова."))
    settings = Settings(openai_api_key="key", telegram_bot_token="token", openai_model="test-model")
    agent = VkusVillAgent(settings, responses_client=responses)

    answer = await agent.run("молоко 2 л")

    assert answer == "Корзина готова."
    call = responses.calls[0]
    assert call["model"] == "test-model"
    assert call["instructions"] == SYSTEM_PROMPT
    assert call["input"] == "молоко 2 л"
    assert call["tools"] == [settings.mcp_tool_config()]


@pytest.mark.asyncio
async def test_agent_rejects_empty_model_response() -> None:
    responses = FakeResponses(SimpleNamespace(output_text=""))
    settings = Settings(openai_api_key="key", telegram_bot_token="token")
    agent = VkusVillAgent(settings, responses_client=responses)

    with pytest.raises(VkusVillAgentError):
        await agent.run("молоко")


@pytest.mark.asyncio
async def test_agent_wraps_openai_errors() -> None:
    responses = FakeResponses(exc=APIConnectionError(request=None))
    settings = Settings(openai_api_key="key", telegram_bot_token="token")
    agent = VkusVillAgent(settings, responses_client=responses)

    with pytest.raises(VkusVillAgentError):
        await agent.run("молоко")
