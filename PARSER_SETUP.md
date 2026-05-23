# 🛒 Wonderfulbed Parser Setup

Полное руководство по настройке и запуску парсера товаров с ctradei для wonderfulbed.ru

## 📋 Требования

- Python 3.11+
- Redis для Celery
- PostgreSQL для логов
- API ключи:
  - OpenAI API key
  - insales API key для wonderfulbed.ru

## 🚀 Быстрый старт

### 1. Конфигурация окружения

```bash
# В .env файл добавить:

# ctradei credentials
CTRADEI_LOGIN=bgrachik@yandex.ru
CTRADEI_PASSWORD=89682753114Grach

# insales API
INSALES_API_URL=https://api.insales.ru/v1
INSALES_API_KEY=your-insales-api-key

# OpenAI
OPENAI_API_KEY=sk-your-openai-key

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1
```

### 2. Установка зависимостей

```bash
cd apps/api
pip install -r requirements.txt
```

### 3. Запуск Celery Worker

```bash
# В одном терминале - Celery Worker
celery -A tasks worker --loglevel=info

# В другом терминале - Celery Beat (для запланированных задач)
celery -A tasks beat --loglevel=info
```

### 4. Запуск FastAPI сервера

```bash
uvicorn main:app --reload
```

## 🔄 Автоматическая синхронизация

Парсер настроен на автоматическую синхронизацию **каждый день в 00:00 MSK**.

Расписание управляется в `celery_config.py`:

```python
beat_schedule = {
    "wonderfulbed-daily-sync": {
        "task": "tasks.wonderfulbed_sync.sync_wonderfulbed_daily",
        "schedule": crontab(hour=0, minute=0),  # 00:00 MSK
    },
}
```

## 📊 Как это работает

### 1️⃣ Аутентификация

- Парсер аутентифицируется на ctradei с использованием email/пароля
- Получает Bearer token для дальнейших запросов

### 2️⃣ Парсинг товаров

- Получает список товаров из категории "Постельное белье"
- Извлекает:
  - Название товара
  - Описание
  - Цену
  - Остатки
  - Изображения

### 3️⃣ Обогащение AI

- Использует GPT-4 для обогащения данных:
  - SEO-оптимизированные названия
  - SEO-оптимизированные описания
  - Выделение ключевых особенностей
  - Определение целевой аудитории
  - Генерация тегов

### 4️⃣ Синхронизация с insales

- Отправляет обогащенные товары в insales API
- Обновляет цены, остатки, описания
- Создает уникальные SKU для каждого товара

### 5️⃣ Создание фидов

Генерирует Yandex Market фид с форматом:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<yml_catalog>
  <shop>
    <name>Wonderfulbed</name>
    <offers>
      <offer>
        <url>https://wonderfulbed.ru/products/...</url>
        <price>2999</price>
        <name>Комплект постельного белья</name>
        <description>...</description>
      </offer>
    </offers>
  </shop>
</yml_catalog>
```

## 🔌 API Endpoints

### Получить статус парсера

```bash
GET /api/v1/parser/status

Response:
{
  "agent_id": "wonderfulbed-parser",
  "status": "active",
  "last_sync": "2024-01-24T12:30:45.123Z",
  "next_sync": "2024-01-25T00:00:00+03:00",
  "products_count": 1247,
  "success_rate": 99.1
}
```

### Запустить синхронизацию

```bash
POST /api/v1/parser/sync

Body:
{
  "force": true,
  "dry_run": false
}

Response:
{
  "success": true,
  "products_synced": 1247,
  "feed_file": "wonderfulbed_feed_20240124_000000.xml",
  "duration_seconds": 45.32,
  "timestamp": "2024-01-24T12:30:45.123Z"
}
```

### Получить конфигурацию

```bash
GET /api/v1/parser/config
```

### Обновить конфигурацию

```bash
PUT /api/v1/parser/config

Body:
{
  "ctradei_login": "bgrachik@yandex.ru",
  "ctradei_password": "password",
  "insales_api_url": "https://api.insales.ru/v1",
  "enabled": true,
  "sync_interval_hours": 24,
  "retry_on_failure": true
}
```

### Получить логи

```bash
GET /api/v1/parser/logs?limit=50
```

### Протестировать соединение

```bash
POST /api/v1/parser/test

Response:
{
  "ctradei": {
    "status": "connected",
    "message": "✅ Successfully authenticated"
  },
  "insales": {
    "status": "connected",
    "message": "✅ API key valid"
  }
}
```

## 🎯 Web Dashboard

Откройте в браузере:

```
http://localhost:3000/dashboard/parser
```

На странице парсера можно:
- 📊 Просмотреть статус синхронизации
- 🚀 Запустить синхронизацию вручную
- ⚙️ Настроить параметры парсера
- 🔗 Проверить соединение с API
- 📋 Просмотреть историю синхронизаций

## 🐛 Логирование

Логи сохраняются в:
- **Консоль** - В реальном времени
- **База данных** - В таблице `sync_logs`
- **Файлы** - В `/logs/parser.log`

## ⚠️ Обработка ошибок

Парсер автоматически:
- ✅ Переподключается при разрыве соединения
- ✅ Повторяет неудачные операции
- ✅ Логирует все ошибки
- ✅ Отправляет уведомления при критических сбоях

## 🔒 Безопасность

- ✅ Пароли хранятся в переменных окружения
- ✅ Все API ключи шифруются
- ✅ Запросы используют HTTPS
- ✅ Логирование не содержит чувствительных данных
- ✅ Rate limiting на API запросы

## 📈 Мониторинг

### Метрики парсера

- `wonderfulbed.parser.sync_duration` - Время синхронизации (сек)
- `wonderfulbed.parser.products_synced` - Количество товаров
- `wonderfulbed.parser.sync_errors` - Количество ошибок
- `wonderfulbed.parser.success_rate` - Процент успешных синхронизаций

### Настройка алертов

```python
# alerts.py
if success_rate < 95:
    send_alert("Parser success rate is low")

if sync_duration > 120:
    send_alert("Parser is running slow")
```

## 🚀 Развертывание

### Docker

```bash
docker-compose up -d

# Проверить статус
docker-compose ps

# Просмотреть логи
docker-compose logs -f api
docker-compose logs -f celery_worker
docker-compose logs -f celery_beat
```

### Production

```bash
# Убедитесь, что Redis и PostgreSQL запущены
# Отправьте переменные окружения
# Запустите Celery Worker как service
# Запустите Celery Beat как service
# Запустите FastAPI с gunicorn

gunicorn main:app --workers 4 --bind 0.0.0.0:8000
```

## 🆘 Troubleshooting

### Ошибка аутентификации ctradei

```
❌ ctradei auth failed: 401
```

**Решение:**
- Проверьте email и пароль в .env
- Убедитесь, что аккаунт не заблокирован
- Проверьте интернет соединение

### Задача не запускается

```
Task not picked up by worker
```

**Решение:**
```bash
# Проверьте, что worker запущен
celery -A tasks inspect active

# Проверьте Redis соединение
redis-cli ping
```

### Синхронизация зависает

**Решение:**
```bash
# Увеличьте task timeout в celery_config.py
task_time_limit = 60 * 60  # 1 hour

# Или запустите с отладкой
celery -A tasks worker --loglevel=debug
```

## 📚 Дополнительные ресурсы

- [ctradei API Docs](https://ctradei.ru/docs)
- [insales API Docs](https://insales.ru/developers)
- [Celery Documentation](https://docs.celeryproject.org/)
- [LangChain Documentation](https://python.langchain.com/)

## 📞 Поддержка

По вопросам обращайтесь:
- Email: bgrachik@yandex.ru
- GitHub Issues: https://github.com/Grachik2007/TestGitHub/issues
