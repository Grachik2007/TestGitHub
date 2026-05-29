import logging
import os
import json
from typing import Final
from datetime import datetime
import requests

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TOKEN: Final = os.getenv("TELEGRAM_BOT_TOKEN", "")
API_URL: Final = os.getenv("API_URL", "http://localhost:8000")
PRICING_API_URL: Final = os.getenv("PRICING_API_URL", "http://localhost:3001")

# ============= PRICING API HELPERS =============

async def get_pricing_config():
    """Get current pricing configuration."""
    try:
        response = requests.get(f"{PRICING_API_URL}/api/v1/pricing", timeout=5)
        return response.json()
    except Exception as e:
        logger.error(f"Error getting pricing config: {e}")
        return None

async def update_pricing_config(updates: dict):
    """Update pricing configuration."""
    try:
        response = requests.post(
            f"{PRICING_API_URL}/api/v1/pricing",
            json=updates,
            timeout=5
        )
        return response.json()
    except Exception as e:
        logger.error(f"Error updating pricing config: {e}")
        return None

async def recalculate_prices():
    """Trigger price recalculation."""
    try:
        response = requests.post(
            f"{PRICING_API_URL}/api/v1/pricing/recalculate",
            timeout=30
        )
        return response.json()
    except Exception as e:
        logger.error(f"Error recalculating prices: {e}")
        return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hello {user.first_name}! 👋\n\n"
        "I'm your AI Assistant. Here's what I can do:\n\n"
        "🔍 /seo - SEO Analysis Agent\n"
        "🏭 /suppliers - Supplier Research Agent\n"
        "📦 /products - Product Research Agent\n"
        "💰 /pricing - Pricing Optimization Agent\n"
        "⚙️ /prices - Manage pricing parameters\n"
        "/help - Get help\n\n"
        "Just send me a message to start chatting!",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    await update.message.reply_text(
        "Available Commands:\n\n"
        "/start - Start the bot\n"
        "/seo - Analyze SEO\n"
        "/suppliers - Find suppliers\n"
        "/products - Research products\n"
        "/pricing - Optimize pricing\n"
        "/help - Show this message\n\n"
        "Just send me a question and I'll help!"
    )


async def seo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /seo command."""
    await update.message.reply_text(
        "🔍 SEO Analysis Agent\n\n"
        "What would you like to analyze?\n"
        "- Keyword research\n"
        "- Competitor analysis\n"
        "- Content optimization\n"
        "- Metadata suggestions\n\n"
        "Send me your query!"
    )


async def suppliers_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /suppliers command."""
    await update.message.reply_text(
        "🏭 Supplier Research Agent\n\n"
        "I can help you with:\n"
        "- Find suppliers\n"
        "- Compare prices\n"
        "- Analyze margins\n"
        "- Sourcing recommendations\n\n"
        "What are you looking for?"
    )


async def products_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /products command."""
    await update.message.reply_text(
        "📦 Product Research Agent\n\n"
        "I can analyze:\n"
        "- Trending products\n"
        "- Profitable niches\n"
        "- Market validation\n"
        "- Competition analysis\n\n"
        "Tell me what interests you!"
    )


async def pricing_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /pricing command."""
    await update.message.reply_text(
        "💰 Pricing Optimization Agent\n\n"
        "I help with:\n"
        "- Price optimization\n"
        "- Profitability analysis\n"
        "- Competitor pricing\n"
        "- Strategy recommendations\n\n"
        "For managing current prices, use: /prices\n"
        "What product do you need pricing for?"
    )

async def prices_view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /prices view command - show current pricing config."""
    await update.message.chat.send_action("typing")

    config = await get_pricing_config()
    if not config or not config.get('success'):
        await update.message.reply_text("❌ Не смог получить конфигурацию цен. Проверь, запущен ли Pricing API?")
        return

    data = config.get('data', {})
    costs = data.get('costs', {})
    commissions = data.get('commissions', {})
    expenses = data.get('expenses', {})
    margin = data.get('margin', {})

    message = "📊 **ТЕКУЩИЕ ПАРАМЕТРЫ ЦЕН**\n\n"
    message += "💵 **Фиксированные затраты:**\n"
    message += f"  • Упаковка: {costs.get('packaging', 0)}₽\n"
    message += f"  • Сборка: {costs.get('assembly', 0)}₽\n"
    message += f"  • Себестоимость (по умолчанию): {costs.get('defaultWholesaleCost', 0)}₽\n\n"

    message += "📈 **Комиссии и расходы:**\n"
    message += f"  • Комиссия эквайринга: {commissions.get('acquiring', 0)*100:.1f}%\n"
    message += f"  • Маркетинг: {expenses.get('marketing', 0)*100:.1f}%\n"
    message += f"  • Налог УСН: {expenses.get('tax', 0)*100:.1f}%\n\n"

    message += "🎯 **Целевая маржа:**\n"
    message += f"  • {margin.get('target', 0)*100:.0f}%\n\n"

    message += "💡 **Доступные команды:**\n"
    message += "/prices packaging 300 - изменить упаковку\n"
    message += "/prices assembly 150 - изменить сборку\n"
    message += "/prices commission 0.04 - изменить комиссию\n"
    message += "/prices marketing 0.06 - изменить маркетинг\n"
    message += "/prices margin 0.35 - изменить маржу\n"
    message += "/prices recalc - пересчитать цены"

    await update.message.reply_text(message, parse_mode="Markdown")

async def prices_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /prices command with parameters."""
    if not context.args:
        await prices_view(update, context)
        return

    command = context.args[0].lower()
    await update.message.chat.send_action("typing")

    if command == "view":
        await prices_view(update, context)

    elif command == "packaging" and len(context.args) > 1:
        try:
            value = int(context.args[1])
            result = await update_pricing_config({"costs": {"packaging": value}})
            if result and result.get('success'):
                await update.message.reply_text(f"✅ Упаковка обновлена: {value}₽")
            else:
                await update.message.reply_text("❌ Ошибка обновления. Проверь Pricing API")
        except ValueError:
            await update.message.reply_text("❌ Введи число! Пример: /prices packaging 300")

    elif command == "assembly" and len(context.args) > 1:
        try:
            value = int(context.args[1])
            result = await update_pricing_config({"costs": {"assembly": value}})
            if result and result.get('success'):
                await update.message.reply_text(f"✅ Сборка обновлена: {value}₽")
            else:
                await update.message.reply_text("❌ Ошибка обновления")
        except ValueError:
            await update.message.reply_text("❌ Введи число! Пример: /prices assembly 150")

    elif command == "commission" and len(context.args) > 1:
        try:
            value = float(context.args[1])
            result = await update_pricing_config({"commissions": {"acquiring": value}})
            if result and result.get('success'):
                await update.message.reply_text(f"✅ Комиссия обновлена: {value*100:.1f}%")
            else:
                await update.message.reply_text("❌ Ошибка обновления")
        except ValueError:
            await update.message.reply_text("❌ Введи число! Пример: /prices commission 0.04")

    elif command == "marketing" and len(context.args) > 1:
        try:
            value = float(context.args[1])
            result = await update_pricing_config({"expenses": {"marketing": value}})
            if result and result.get('success'):
                await update.message.reply_text(f"✅ Маркетинг обновлен: {value*100:.1f}%")
            else:
                await update.message.reply_text("❌ Ошибка обновления")
        except ValueError:
            await update.message.reply_text("❌ Введи число! Пример: /prices marketing 0.06")

    elif command == "margin" and len(context.args) > 1:
        try:
            value = float(context.args[1])
            result = await update_pricing_config({"margin": {"target": value}})
            if result and result.get('success'):
                await update.message.reply_text(f"✅ Маржа обновлена: {value*100:.0f}%")
            else:
                await update.message.reply_text("❌ Ошибка обновления")
        except ValueError:
            await update.message.reply_text("❌ Введи число! Пример: /prices margin 0.35")

    elif command == "recalc":
        await update.message.reply_text("⏳ Пересчитываю цены... Это может занять минуту...")
        result = await recalculate_prices()
        if result and result.get('success'):
            await update.message.reply_text("✅ Цены успешно пересчитаны и feeds обновлены!")
        else:
            await update.message.reply_text("❌ Ошибка пересчета. Проверь логи.")

    else:
        await update.message.reply_text(
            "❌ Неизвестная команда!\n\n"
            "Используй:\n"
            "/prices view - показать текущие параметры\n"
            "/prices packaging 300 - изменить упаковку\n"
            "/prices assembly 150 - изменить сборку\n"
            "/prices commission 0.04 - изменить комиссию\n"
            "/prices marketing 0.06 - изменить маркетинг\n"
            "/prices margin 0.35 - изменить маржу\n"
            "/prices recalc - пересчитать цены"
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular messages."""
    user_message = update.message.text
    user = update.effective_user

    logger.info(f"Received message from {user.id}: {user_message}")

    # Show typing indicator
    await update.message.chat.send_action("typing")

    await update.message.reply_text(
        f"Thank you for your message! 🚀\n\n"
        f'You said: "{user_message}"\n\n'
        f"I'm processing your request... Please wait!"
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "Sorry, something went wrong! Please try again."
        )


def main() -> None:
    """Start the bot."""
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required!")

    application = Application.builder().token(TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("seo", seo_command))
    application.add_handler(CommandHandler("suppliers", suppliers_command))
    application.add_handler(CommandHandler("products", products_command))
    application.add_handler(CommandHandler("pricing", pricing_command))
    application.add_handler(CommandHandler("prices", prices_command))

    # Messages
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Error handler
    application.add_error_handler(error_handler)

    # Start polling
    logger.info("Bot is starting...")
    logger.info(f"Pricing API URL: {PRICING_API_URL}")
    application.run_polling()


if __name__ == "__main__":
    main()
