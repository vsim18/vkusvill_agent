from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.agent import VkusVillAgentError
from app.bot import START_MESSAGE, USER_ERROR_MESSAGE, handle_text, start


class FakeAgent:
    def __init__(self, answer: str | None = None, exc: Exception | None = None) -> None:
        self.answer = answer or "Корзина готова."
        self.exc = exc
        self.messages: list[str] = []

    async def run(self, message: str) -> str:
        self.messages.append(message)
        if self.exc is not None:
            raise self.exc
        return self.answer


@pytest.mark.asyncio
async def test_start_replies_with_intro() -> None:
    message = SimpleNamespace(reply_text=AsyncMock())
    update = SimpleNamespace(message=message)

    await start(update, SimpleNamespace())

    message.reply_text.assert_awaited_once_with(START_MESSAGE)


@pytest.mark.asyncio
async def test_handle_text_passes_message_to_agent() -> None:
    message = SimpleNamespace(text="яйца 20 шт", reply_text=AsyncMock())
    update = SimpleNamespace(message=message)
    agent = FakeAgent(answer="Корзина готова.")
    context = SimpleNamespace(application=SimpleNamespace(bot_data={"agent": agent}))

    await handle_text(update, context)

    assert agent.messages == ["яйца 20 шт"]
    message.reply_text.assert_awaited_once_with("Корзина готова.", disable_web_page_preview=True)


@pytest.mark.asyncio
async def test_handle_text_hides_agent_errors() -> None:
    message = SimpleNamespace(text="молоко", reply_text=AsyncMock())
    update = SimpleNamespace(message=message)
    agent = FakeAgent(exc=VkusVillAgentError("failed"))
    context = SimpleNamespace(application=SimpleNamespace(bot_data={"agent": agent}))

    await handle_text(update, context)

    message.reply_text.assert_awaited_once_with(USER_ERROR_MESSAGE)
