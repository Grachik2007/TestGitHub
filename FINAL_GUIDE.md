# 🚀 AI Business SaaS Agents Platform - Финальный гайд

**Status:** ✅ ПОЛНОСТЬЮ ГОТОВО К ИСПОЛЬЗОВАНИЮ

---

## 📦 ЧТО ВКЛЮЧЕНО

### Backend (FastAPI)
- ✅ REST API с полной документацией (Swagger)
- ✅ JWT аутентификация
- ✅ PostgreSQL ORM (SQLAlchemy)
- ✅ Redis кеширование
- ✅ Celery для фоновых задач
- ✅ 5 AI агентов
- ✅ Smart Pricing Engine
- ✅ Parser API для ctradei

### Frontend (Next.js)
- ✅ Dashboard с 6+ страницами
- ✅ Аутентификация
- ✅ Управление агентами
- ✅ Конфигурация цен
- ✅ Парсер интерфейс
- ✅ Аналитика и биллинг

### Telegram Bot
- ✅ 5 команд (/start, /help, /seo, /suppliers, /products)
- ✅ Обработка сообщений
- ✅ Интеграция с API

### Интеграции
- ✅ ctradei (YML + CSV парсинг)
- ✅ Smart Pricing (маржа + расходы)
- ✅ insales (CSV/YML для импорта)
- ✅ GitHub Pages (фиды + интерфейс)

### DevOps
- ✅ Docker & Docker Compose
- ✅ GitHub Actions CI/CD
- ✅ Nginx reverse proxy
- ✅ Monitoring ready

---

## 🎯 НАЧАЛО РАБОТЫ (5 МИНУТ)

### Вариант 1: Docker (РЕКОМЕНДУЕТСЯ)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Grachik2007/TestGitHub.git
cd TestGitHub

# 2. Создать .env файл
cp .env.example .env
nano .env  # Заполнить требуемые переменные

# 3. Запустить проект
docker-compose up -d

# 4. Готово!
# - Web:    http://localhost:3000
# - API:    http://localhost:8000
# - Docs:   http://localhost:8000/api/docs
# - Admin:  http://localhost:8000/docs
```

### Вариант 2: Локально (Python + Node)

```bash
# Backend
cd apps/api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Frontend (в новом терминале)
cd apps/web
npm install
npm run dev

# Telegram Bot (в новом терминале)
cd apps/telegram
pip install -r requirements.txt
python main.py
```

---

## 📋 КОНФИГУРАЦИЯ

### Основные переменные (.env)

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_agents
REDIS_URL=redis://localhost:6379/0

# API
API_HOST=0.0.0.0
API_PORT=8000
JWT_SECRET_KEY=your-super-secret-key-change-in-production

# Pricing
PRICING_MARGIN=35.0
PRICING_LOGISTICS=8.0
PRICING_COMMISSION=5.0
PRICING_FIXED=15.0

# GigaChat (для обогащения описаний)
GIGACHAT_CLIENT_ID=your-client-id
GIGACHAT_CLIENT_SECRET=your-client-secret

# insales (опционально)
INSALES_SHOP_ID=your-shop-id

# Telegram (опционально)
TELEGRAM_BOT_TOKEN=your-bot-token

# Stripe (опционально)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
```

### GitHub Secrets (для CI/CD)

```
DOCKER_USERNAME=your-username
DOCKER_PASSWORD=your-password
GIGACHAT_CLIENT_ID=...
GIGACHAT_CLIENT_SECRET=...
INSALES_SHOP_ID=...
```

---

## 🌐 ДОСТУПНЫЕ URL

### Локально (localhost)

| Сервис | URL | Назначение |
|--------|-----|-----------|
| **Web** | http://localhost:3000 | Dashboard |
| **API** | http://localhost:8000 | REST API |
| **Docs** | http://localhost:8000/api/docs | Swagger UI |
| **Admin** | http://localhost:8000/docs | ReDoc |

### На GitHub Pages

| Ресурс | URL | Назначение |
|--------|-----|-----------|
| **Фиды** | https://grachik2007.github.io/TestGitHub/ | Список фидов |
| **Agents** | https://grachik2007.github.io/TestGitHub/agents.html | UI агентов |
| **CSV** | https://grachik2007.github.io/TestGitHub/insales-import.csv | Для insales |
| **YML** | https://grachik2007.github.io/TestGitHub/insales-import.yml | Для insales |

---

## 🔐 УЧЕТНЫЕ ДАННЫЕ (DEMO)

### Вход в систему

```
Email: demo@example.com
Password: demo123456
```

### Регистрация новой учетной записи

```
1. Перейти на http://localhost:3000
2. Нажать "Sign Up"
3. Заполнить форму
4. Авторизоваться
```

---

## 📊 ИНТЕГРАЦИЯ СИСТЕМ

### ctradei → Фиды → insales

```
ctradei.com
    ↓
YML (изображения) + CSV (цены/остатки)
    ↓
Unified Feed (JSON)
    ↓
Smart Pricing Engine
    ↓
CSV & YML для insales
    ↓
GitHub Pages публикация
    ↓
Скачать и загрузить в insales
    ↓
wonderfulbed.ru (обновлены товары)
```

### Автоматизация

```
GitHub Actions (00:30 MSK каждый день)
    ↓
1. ctradei_integrator.py (объединение данных)
2. generate_feed_with_pricing.py (если нужно)
3. generate_insales_files.py (файлы для insales)
4. generate_dashboard.py (HTML интерфейс)
5. Публикация на GitHub Pages
```

---

## 🛠️ КОМАНДЫ

### Docker Compose

```bash
# Запустить
docker-compose up -d

# Остановить
docker-compose down

# Логи
docker-compose logs -f api
docker-compose logs -f web
docker-compose logs -f telegram

# Rebuild
docker-compose up -d --build

# БД миграции
docker-compose exec api alembic upgrade head
```

### Python скрипты

```bash
# Генерировать ctradei фиды
python infrastructure/scripts/ctradei_integrator.py

# Генерировать insales файлы
python infrastructure/scripts/generate_insales_files.py

# Генерировать dashboard
python infrastructure/scripts/generate_dashboard.py

# Smart Pricing калькулятор
python -c "from apps.api.services.pricing_calculator import *; ..."
```

### Frontend

```bash
cd apps/web

# Dev сервер
npm run dev

# Build
npm run build

# Запустить production
npm start

# Lint & format
npm run lint
npm run format
```

---

## 📱 ФУНКЦИОНАЛЬНОСТЬ

### Dashboard (http://localhost:3000/dashboard)

- 📊 **Dashboard** - статистика и метрики
- 🤖 **AI Agents** - управление агентами
- 🛒 **Wonderfulbed Parser** - синхронизация товаров
- 💰 **Smart Pricing** - управление ценами
- 📈 **Analytics** - аналитика
- 💳 **Billing** - подписки

### API (http://localhost:8000/api/docs)

```
POST   /api/v1/auth/register         - Регистрация
POST   /api/v1/auth/login            - Вход
GET    /api/v1/agents                - Список агентов
POST   /api/v1/agents/execute        - Запустить агента
GET    /api/v1/parser/status         - Статус парсера
POST   /api/v1/pricing/calculate     - Расчет цен
GET    /api/v1/analytics             - Аналитика
```

### Telegram Bot

```
/start      - Начало
/help       - Справка
/seo        - SEO агент
/suppliers  - Поиск поставщиков
/products   - Анализ товаров
/pricing    - Оптимизация цен
```

---

## 🔄 ЕЖЕДНЕВНАЯ СИНХРОНИЗАЦИЯ

**Время:** 00:30 MSK каждый день

**Процесс:**

```
1. Скачать YML с ctradei
   - Товары, описания, изображения
   
2. Скачать CSV с ctradei
   - Цены, остатки
   
3. Объединить по ID
   - Merge товаров
   
4. Smart Pricing
   - Розничные цены
   
5. Генерировать фиды
   - JSON, XML для маркетов
   - CSV, YML для insales
   
6. Публиковать на GitHub Pages
   - Доступны по постоянным ссылкам
```

---

## 🚀 DEVELOPMENT

### Код

```
apps/
├── api/          # FastAPI backend
│   ├── main.py   # Entry point
│   ├── agents/   # AI agents
│   ├── api/      # REST endpoints
│   ├── core/     # Config, security
│   ├── tasks/    # Celery tasks
│   └── services/ # Business logic
├── web/          # Next.js frontend
│   ├── app/      # Pages
│   ├── components/
│   └── hooks/
└── telegram/     # Bot
```

### Git Workflow

```bash
# Create branch
git checkout -b feature/your-feature

# Commit changes
git add .
git commit -m "feat: your feature"

# Push
git push origin feature/your-feature

# Create PR
# GitHub Actions автоматически проверит
```

### Тестирование

```bash
# Backend тесты
cd apps/api
pytest

# Frontend тесты
cd apps/web
npm test

# Linting
npm run lint
black --check apps/api
```

---

## 📚 ДОКУМЕНТАЦИЯ

| Файл | Содержание |
|------|-----------|
| **README.md** | Основная документация |
| **ARCHITECTURE.md** | Архитектура системы |
| **DEPLOYMENT.md** | Развертывание |
| **CONTRIBUTING.md** | Контрибьютинг |
| **SMART_PRICING_GUIDE.md** | Smart Pricing Engine |
| **INSALES_FILES_GUIDE.md** | insales интеграция |
| **PARSER_SETUP.md** | Parser API |
| **GIGACHAT_SETUP.md** | GigaChat интеграция |
| **GITHUB_PAGES_URLS.md** | Публичные URL |

---

## ✅ CHECKLIST ПЕРЕД PRODUCTION

- [ ] `.env` файл заполнен
- [ ] База данных создана
- [ ] Redis запущен
- [ ] Docker images собраны
- [ ] Все сервисы запущены
- [ ] API работает (http://localhost:8000/api/docs)
- [ ] Frontend загружается (http://localhost:3000)
- [ ] Telegram bot подключен (если требуется)
- [ ] GigaChat credentials настроены (если требуется)
- [ ] GitHub Secrets установлены (если используется CI/CD)
- [ ] Тесты проходят
- [ ] Документация актуальна
- [ ] Резервная копия БД создана

---

## 🆘 ПОМОЩЬ

### Логирование

```bash
# Смотреть логи контейнера
docker-compose logs -f api

# Смотреть логи приложения
tail -f logs/app.log

# Смотреть logfile
docker-compose logs -f postgres
```

### Проблемы

**Порт занят:**
```bash
# Найти процесс
lsof -i :3000
lsof -i :8000

# Убить процесс
kill -9 <PID>
```

**БД ошибка:**
```bash
# Пересоздать контейнер
docker-compose down
docker-compose rm postgres
docker-compose up -d postgres
docker-compose exec api alembic upgrade head
```

**Redis ошибка:**
```bash
# Пересоздать
docker-compose down
docker-compose rm redis
docker-compose up -d redis
```

---

## 📈 МАСШТАБИРОВАНИЕ

### Production Deploy (на Railway, Render, VPS)

Смотрите: **DEPLOYMENT.md**

```
1. Docker images в Docker Registry
2. Database на облачном сервисе
3. Redis на облачном сервисе
4. GitHub Actions для CI/CD
5. Monitoring с Sentry/DataDog
```

### Оптимизация

- Включить Redis кеширование
- Настроить Celery для фоновых задач
- Оптимизировать базу данных (индексы)
- Установить CDN для статики
- Включить gzip compression
- Добавить логирование/мониторинг

---

## 🎓 ОБУЧЕНИЕ

### API тестирование

```bash
# С Postman
Import: http://localhost:8000/api/docs

# С curl
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"demo123456"}'
```

### Dashboard навигация

```
1. Перейти http://localhost:3000
2. Sign Up или вход
3. Explore Dashboard:
   - Dashboard (статистика)
   - AI Agents (запуск агентов)
   - Smart Pricing (конфигурация)
   - Parser (управление парсером)
```

---

## 🚀 БЫСТРЫЙ СТАРТ (30 СЕКУНД)

```bash
# Clone
git clone https://github.com/Grachik2007/TestGitHub.git
cd TestGitHub

# Copy env
cp .env.example .env

# Start
docker-compose up -d

# Wait 30 seconds
sleep 30

# Open
open http://localhost:3000

# Done! ✅
```

---

## 📞 ПОДДЕРЖКА

- GitHub Issues: https://github.com/Grachik2007/TestGitHub/issues
- Email: bgrachik@yandex.ru
- Документация: Смотреть выше

---

**🎉 ПРОЕКТ ПОЛНОСТЬЮ ГОТОВ К ИСПОЛЬЗОВАНИЮ! 🎉**

**Версия:** 1.0.0
**Статус:** Production Ready ✅
**Последнее обновление:** 2026-05-23
**Разработчик:** Grachik2007

Спасибо за использование!
