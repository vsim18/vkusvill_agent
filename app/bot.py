import logging

from telegram import Update
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.request import HTTPXRequest

from app.agent import VkusVillAgent, VkusVillAgentError
from app.config import Settings, load_settings, validate_runtime_settings

logger = logging.getLogger(__name__)
START_MESSAGE = "Привет! Я помогу собрать корзину во ВкусВилле.\nНапиши, что нужно купить."
USER_ERROR_MESSAGE = "Не удалось собрать корзину. Попробуйте ещё раз через несколько секунд."


async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(START_MESSAGE)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.message.text is None:
        return

    agent = context.application.bot_data["agent"]
    try:
        answer = await agent.run(update.message.text)
    except VkusVillAgentError:
        logger.exception("Agent failed to handle Telegram message")
        await update.message.reply_text(USER_ERROR_MESSAGE)
        return
    except TelegramError:
        raise
    except Exception:
        logger.exception("Unexpected error while handling Telegram message")
        await update.message.reply_text(USER_ERROR_MESSAGE)
        return

    await update.message.reply_text(answer, disable_web_page_preview=True)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Telegram error while processing update %r", update, exc_info=context.error)


def _build_telegram_request(settings: Settings) -> HTTPXRequest:
    return HTTPXRequest(
        connect_timeout=settings.telegram_connect_timeout,
        read_timeout=settings.telegram_read_timeout,
        write_timeout=settings.telegram_write_timeout,
        pool_timeout=settings.telegram_pool_timeout,
        proxy=settings.telegram_proxy_url,
    )


def build_application(agent: VkusVillAgent | None = None) -> Application:
    settings = load_settings()
    validate_runtime_settings(settings)
    application = (
        ApplicationBuilder()
        .token(settings.telegram_bot_token)
        .request(_build_telegram_request(settings))
        .build()
    )
    application.bot_data["agent"] = agent or VkusVillAgent(settings)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_error_handler(error_handler)
    return application


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    application = build_application()
    application.run_polling(allowed_updates=Update.ALL_TYPES)
