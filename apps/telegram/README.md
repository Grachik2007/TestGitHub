# Telegram Bot

Full-featured Telegram AI Assistant for the AI Agents Platform.

## 🚀 Setup

### Prerequisites
- Python 3.11+
- Telegram bot token from @BotFather

### Installation

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Setup environment**
```bash
cp .env.example .env
# Add your TELEGRAM_BOT_TOKEN
```

3. **Run bot**
```bash
python main.py
```

## 🤖 Commands

- `/start` - Start the bot
- `/seo` - SEO Analysis Agent
- `/suppliers` - Supplier Research Agent
- `/products` - Product Research Agent
- `/pricing` - Pricing Optimization Agent
- `/help` - Get help

## 💬 Features

- Inline keyboards for quick actions
- Typing indicators for better UX
- Message history support
- Integration with backend API
- Markdown formatting
- Error handling

## 🔧 Development

### Telegram Bot Token

1. Talk to @BotFather on Telegram
2. Create a new bot: `/newbot`
3. Copy the token and paste into `.env`

### Testing

```bash
# Send test messages to your bot
# Try /start, /help, /seo, etc.
```

## 📚 Resources

- [Telegram Bot API](https://core.telegram.org/bots)
- [python-telegram-bot docs](https://docs.python-telegram-bot.org)

## 📝 License

MIT
