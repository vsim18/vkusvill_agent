# vkusvill-agent

Минимальный production-ready MVP персонального Telegram-бота для сборки корзины во ВкусВилле.

Пользователь пишет запрос естественным языком, бот через OpenAI Responses API подключает официальный remote MCP ВкусВилла, ищет реальные товары, выбирает подходящие позиции и возвращает ссылку на корзину. Бот не оформляет и не оплачивает заказ.

## Архитектура

```text
Telegram
  -> Python Telegram Bot polling
  -> OpenAI Responses API
  -> remote MCP
  -> https://mcp.vkusvill.ru/mcp
```

Приложение stateless: без базы данных, Redis, Celery, FastAPI, LangChain, LangGraph и собственного MCP server/client.

## Требования

- Python 3.12+
- Telegram bot token
- OpenAI API key
- Docker и Docker Compose, если нужен контейнерный запуск

## Создание Telegram bot

1. Откройте Telegram и найдите `@BotFather`.
2. Выполните `/newbot`.
3. Сохраните выданный token в `TELEGRAM_BOT_TOKEN` в `.env`.

## Создание OpenAI API key

1. Откройте OpenAI Platform.
2. Создайте API key для проекта.
3. Сохраните его в `OPENAI_API_KEY` в `.env`.

## Установка

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Настройка

```bash
cp .env.example .env
```

Заполните:

```text
OPENAI_API_KEY=
TELEGRAM_BOT_TOKEN=
OPENAI_MODEL=gpt-5-mini
```

Опциональные переменные:

```text
VKUSVILL_MCP_URL=https://mcp.vkusvill.ru/mcp
VKUSVILL_MCP_SERVER_LABEL=vkusvill
VKUSVILL_ALLOWED_MCP_TOOLS=vkusvill_products_search,vkusvill_products_discount,vkusvill_product_details,vkusvill_product_analogs,vkusvill_cart_link_create
TELEGRAM_CONNECT_TIMEOUT=30
TELEGRAM_READ_TIMEOUT=30
TELEGRAM_WRITE_TIMEOUT=30
TELEGRAM_POOL_TIMEOUT=5
TELEGRAM_PROXY_URL=
```

Если локальный запуск падает на `telegram.error.TimedOut` во время `get_me()`,
проверьте доступ к Telegram Bot API с этой машины. Для локального proxy можно
задать, например, `TELEGRAM_PROXY_URL=socks5://127.0.0.1:1080` или HTTP proxy URL,
который доступен в вашей среде.

## Запуск локально

```bash
python -m app
```

или:

```bash
make run
```

## Запуск Docker

```bash
docker compose up -d
```

## Пример запроса

```text
Собери продукты на неделю:
- яйца 20 шт
- молоко 3 л
- куриная грудка 1.5 кг
- творог 5% 4 пачки
- бананы 1 кг
- овощи
- кофе

Бюджет 4000 ₽.
Старайся выбирать товары со скидкой.
```

## Ограничения

- Бот только создаёт ссылку на корзину.
- Финальное оформление заказа пользователь делает вручную на стороне ВкусВилла.
- Бот не выполняет платежи и не запрашивает платёжные данные.
- Качество подбора зависит от доступности OpenAI API и официального MCP ВкусВилла.
- Приложение не хранит историю диалогов.

## MCP ВкусВилла

Официальная страница MCP: <https://mcp.vkusvill.ru/mcp>.

Контракт проверен 2026-09-06. На странице указаны tools:

- `vkusvill_products_search`: поиск товаров по текстовому запросу. Возвращает `id`, `xml_id`, описание, цену, рейтинг, состав, КБЖУ и фото. Поддерживает `mode: full|short|custom`, `fields`, `sort: popularity|rating|price_asc|price_desc|new`, `page`; limit фиксирован 10 на страницу.
- `vkusvill_products_discount`: поиск акционных товаров по текстовому запросу. Возвращает товарные данные. Поддерживает `sort` и `page`; limit фиксирован 10 на страницу.
- `vkusvill_product_details`: детали товара по `id` из поиска.
- `vkusvill_product_analogs`: аналоги товара по `id` из поиска.
- `vkusvill_product_barcode`: детали товара по штрихкоду.
- `vkusvill_cart_link_create`: создаёт ссылку на корзину. Вход: `products` от 1 до 20 элементов, каждый элемент `{xml_id:int>0, q:number 0.01..40}`.
- `vkusvill_recipes`: поиск рецептов.
- `vkusvill_shops`: поиск магазинов.

В приложении разрешены только минимально необходимые tools: поиск, скидки, детали, аналоги и создание ссылки на корзину.

OpenAI remote MCP tool используется через Responses API с конфигурацией:

```python
{
    "type": "mcp",
    "server_label": "vkusvill",
    "server_url": "https://mcp.vkusvill.ru/mcp",
    "allowed_tools": [
        "vkusvill_products_search",
        "vkusvill_products_discount",
        "vkusvill_product_details",
        "vkusvill_product_analogs",
        "vkusvill_cart_link_create",
    ],
    "require_approval": "never",
}
```

Формат сверялся с official OpenAI documentation по Responses API и remote MCP tools: MCP tool имеет `type: "mcp"`, `server_label`, один из `server_url`/`connector_id`, опциональные `allowed_tools` и `require_approval`.

## Security notes

- `.env` добавлен в `.gitignore`.
- Секреты не логируются.
- Пользовательские traceback не отправляются в Telegram.
- Unit tests не вызывают OpenAI и MCP.
- Бот не оформляет заказ, не оплачивает заказ и не работает с банковскими картами.

## Tests и lint

```bash
ruff check .
ruff format --check .
pytest
```

Опциональный integration test:

```bash
RUN_INTEGRATION_TESTS=1 pytest -m integration
```

Integration test требует настоящие `OPENAI_API_KEY` и доступность MCP ВкусВилла.
