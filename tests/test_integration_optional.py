import os

import pytest

from app.agent import VkusVillAgent
from app.config import load_settings, validate_runtime_settings


@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_can_call_openai_and_vkusvill_mcp_when_enabled() -> None:
    if os.getenv("RUN_INTEGRATION_TESTS") != "1":
        pytest.skip("Set RUN_INTEGRATION_TESTS=1 to run network integration tests")

    settings = load_settings()
    validate_runtime_settings(settings)
    agent = VkusVillAgent(settings)

    answer = await agent.run("Для теста найди один литр молока и создай ссылку на корзину.")

    assert answer
