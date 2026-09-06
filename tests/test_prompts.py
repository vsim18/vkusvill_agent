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


def test_system_prompt_supports_recipe_requests() -> None:
    assert "режиме рецепта" in SYSTEM_PROMPT
    assert "vkusvill_recipes" in SYSTEM_PROMPT
    assert "ингредиенты" in SYSTEM_PROMPT
    assert "соль, перец, воду" in SYSTEM_PROMPT


def test_system_prompt_does_not_require_full_recipe_for_dish_name() -> None:
    assert "не проси" in SYSTEM_PROMPT
    assert "прислать сам рецепт" in SYSTEM_PROMPT
    assert "для названия блюда всегда сначала используй vkusvill_recipes" in SYSTEM_PROMPT
