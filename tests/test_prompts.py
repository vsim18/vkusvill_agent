from app.prompts import SYSTEM_PROMPT


def test_system_prompt_contains_safety_boundaries() -> None:
    assert "Не оформляй заказ" in SYSTEM_PROMPT
    assert "Не оплачивай заказ" in SYSTEM_PROMPT
    assert "выдумывай" in SYSTEM_PROMPT.lower()
    assert "product id" in SYSTEM_PROMPT
    assert "xml_id" in SYSTEM_PROMPT


def test_system_prompt_requires_real_mcp_cart_link() -> None:
    assert "MCP" in SYSTEM_PROMPT
    assert "ссылку на корзину" in SYSTEM_PROMPT
    assert "реальными xml_id" in SYSTEM_PROMPT


def test_system_prompt_handles_mcp_rate_limits() -> None:
    assert "rate limit" in SYSTEM_PROMPT
    assert "Попробуйте повторить запрос через несколько минут" in SYSTEM_PROMPT
    assert "не продолжай уточнять" in SYSTEM_PROMPT
