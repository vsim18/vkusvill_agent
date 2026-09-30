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


def test_system_prompt_requires_tbank_cart_transfer() -> None:
    assert "Перенос корзины в Т-Банк" in SYSTEM_PROMPT
    assert "тот же самый набор" in SYSTEM_PROMPT
    assert "🛒 Корзина ВкусВилла в Т-Банке" in SYSTEM_PROMPT
    assert "grocery_stores" in SYSTEM_PROMPT
    assert "grocery_search" in SYSTEM_PROMPT
    assert "grocery_add_to_cart" in SYSTEM_PROMPT
    assert "grocery_cart" in SYSTEM_PROMPT
    assert "Не сопоставлено" in SYSTEM_PROMPT


def test_system_prompt_requires_confident_matching_only() -> None:
    assert "однозначные совпадения" in SYSTEM_PROMPT
    assert "равновероятных" in SYSTEM_PROMPT
    assert "НЕ добавляй" in SYSTEM_PROMPT


def test_system_prompt_forbids_checkout() -> None:
    assert "Никогда не вызывай grocery_checkout" in SYSTEM_PROMPT
    assert "Не вызывай grocery_checkout" in SYSTEM_PROMPT
    assert "Не оплачивай заказ" in SYSTEM_PROMPT


def test_system_prompt_drops_legacy_tbank_search_queries() -> None:
    assert "T-Bank search queries" not in SYSTEM_PROMPT
    assert "🏦 Для ВкусВилла в Т-Банке" not in SYSTEM_PROMPT
    assert "Нажми кнопку ниже" not in SYSTEM_PROMPT
    assert "search_query" not in SYSTEM_PROMPT
    assert "не готовая корзина" not in SYSTEM_PROMPT


def test_system_prompt_requires_full_product_names() -> None:
    assert "ПОЛНЫЕ" in SYSTEM_PROMPT
    assert "Яйцо куриное высшей категории СВ, 10 шт" in SYSTEM_PROMPT
    assert "яйца" in SYSTEM_PROMPT.lower()
    assert "Молоко 3,2% «Экомилк» 930 мл" in SYSTEM_PROMPT
