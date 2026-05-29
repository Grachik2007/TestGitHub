# 🤖 Telegram Bot - Полное руководство запуска

## 📋 Информация о боте

- **Bot Username:** @SaaS_It_bot
- **Bot Token:** `8743509236:AAG_m2T2Qm0ytKN0cw9gxZs3110wCaDn0YtU`
- **Status:** Готов к запуску ✅

## 🚀 Быстрый старт (5 минут)

### 1. Клонировать репозиторий

```bash
cd /home/user/TestGitHub
```

### 2. Создать .env файл

```bash
cp .env.example .env
```

Отредактировать `.env` и заполнить:

```env
# Telegram Bot (уже есть!)
TELEGRAM_BOT_TOKEN=8743509236:AAG_m2T2Qm0ytKN0cw9gxZs3110wCaDn0YtU

# GigaChat API (нужны твои ключи от ctradei)
GIGACHAT_AUTH_KEY=xxx
GIGACHAT_CLIENT_ID=xxx
GIGACHAT_CLIENT_SECRET=xxx

# URLs (по умолчанию)
API_URL=http://localhost:8000
PRICING_API_URL=http://localhost:3001
```

### 3. Установить зависимости

```bash
pip install python-telegram-bot requests
```

### 4. Запустить Pricing API в одном терминале

```bash
node pricing-api.js
```

Должно вывести:
```
💰 === PRICING API ЗАПУЩЕНА ===
🌐 http://localhost:3001/api/v1/pricing
```

### 5. Запустить бот в другом терминале

```bash
# Загрузить переменные из .env
export $(cat .env | xargs)

# Запустить бот
python apps/telegram/main.py
```

Должно вывести:
```
Bot is starting...
Pricing API URL: http://localhost:3001
```

**Готово! Бот работает! 🎉**

---

## 📱 Тестирование бота

Откройте Telegram и найдите **@SaaS_It_bot**

Или в браузере: `https://t.me/SaaS_It_bot`

Попробуйте команды:

```
/start
/prices
/seo https://wonderfulbed.ru
/suppliers кровати
/products мебель
/pricing кровать 1500
```

---

## 🔑 Как получить GigaChat ключи

1. Зайдите на https://ctradei.com/
2. Логин: `bgrachik@yandex.ru`
3. Найдите раздел "Мой GigaChat API"
4. Скопируйте три значения:
   - Authorization Key
   - Client ID
   - Client Secret
5. Вставьте в `.env`

Подробнее: смотрите `GIGACHAT_SETUP.md`

---

## 📊 Архитектура системы

```
                    ┌─────────────────────┐
                    │   Telegram (@SaaS_It_bot)
                    └───────────┬──────────┘
                                │
                    ┌───────────▼──────────┐
                    │  Bot (main.py)       │
                    │  • /seo              │
                    │  • /suppliers        │
                    │  • /products         │
                    │  • /pricing          │
                    │  • /prices           │
                    └───┬──────────┬───────┘
                        │          │
         ┌──────────────┴─┐        └────────────────┐
         │                │                        │
    ┌────▼────────┐   ┌──▼──────────────┐   ┌────▼──────────┐
    │ GigaChat API │   │ Pricing API     │   │ config/        │
    │ (AI ответы) │   │ (pricing-api.js)│   │ pricing.json   │
    └─────────────┘   └────────────────┘   └────────────────┘
```

---

## 🛠️ Команды для разработки

### Перезагрузить бот

```bash
# Остановить: Ctrl+C
# Запустить заново:
python apps/telegram/main.py
```

### Проверить логи

Логи выводятся в консоль в реальном времени

### Изменить цены

В боте:
```
/prices packaging 300
/prices margin 0.35
/prices recalc
```

### Анализ сайта

```
/seo https://wonderfulbed.ru
```

---

## 📝 Структура кода бота

```
apps/telegram/
├── main.py              # Основной файл бота с командами
├── gigachat_client.py   # GigaChat API клиент для AI анализа
└── __init__.py

config/
└── pricing.json         # Конфигурация параметров ценообразования

pricing-api.js           # REST API для управления ценами
.env                     # Секреты (НЕ в git!)
.env.example             # Пример конфигурации
```

---

## 🔐 Безопасность

**⚠️ ВАЖНО:**

```bash
# НЕ закоммичивать .env файл!
git status  # должен показать .env в .gitignore

# Все секреты только в .env или в переменных окружения
export TELEGRAM_BOT_TOKEN="xxx"
export GIGACHAT_AUTH_KEY="xxx"
```

---

## 🐛 Troubleshooting

### "Bot token not found"
```bash
export TELEGRAM_BOT_TOKEN=8743509236:AAG_m2T2Qm0ytKN0cw9gxZs3110wCaDn0YtU
```

### "GigaChat credentials not configured"
Заполни GIGACHAT_* в .env файле

### "Pricing API not responding"
```bash
# Убедись что запущена:
node pricing-api.js
# Проверь http://localhost:3001/api/v1/pricing
```

### "Bot doesn't respond"
1. Проверь токен правильный
2. Посмотри логи в консоли
3. Убедись что интернет работает
4. Перезагрузи бот: Ctrl+C и python apps/telegram/main.py

---

## 📞 Поддержка

Бот логирует все события. Посмотри консоль для ошибок.

Команда `/help` в боте показывает справку.

---

## ✅ Чек-лист запуска

- [ ] Создал .env файл
- [ ] Заполнил TELEGRAM_BOT_TOKEN
- [ ] Заполнил GigaChat ключи (или пока пропустил)
- [ ] Установил python-telegram-bot: `pip install python-telegram-bot requests`
- [ ] Запустил Pricing API: `node pricing-api.js`
- [ ] Запустил бот: `python apps/telegram/main.py`
- [ ] Бот работает (логи в консоли)
- [ ] Написал /start в @SaaS_It_bot в Telegram
- [ ] Бот ответил приветствием ✅

**Готово к работе! 🚀**
