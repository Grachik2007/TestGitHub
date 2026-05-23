import logging
import os
from typing import Final

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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hello {user.first_name}! 👋\n\n"
        "I'm your AI Assistant. Here's what I can do:\n\n"
        "/seo - SEO Analysis Agent\n"
        "/suppliers - Supplier Research Agent\n"
        "/products - Product Research Agent\n"
        "/pricing - Pricing Optimization Agent\n"
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
        "What product do you need pricing for?"
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

    # Messages
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Error handler
    application.add_error_handler(error_handler)

    # Start polling
    logger.info("Bot is starting...")
    application.run_polling()


if __name__ == "__main__":
    main()
