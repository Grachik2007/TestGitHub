# 🤖 GigaChat Integration Guide

Интеграция GigaChat для обогащения товаров на русском языке.

## Что такое GigaChat?

**GigaChat** - это русский LLM от Яндекса, специально оптимизированный для работы с русским текстом. Идеален для:
- ✅ Генерации описаний товаров на русском
- ✅ SEO оптимизации русского текста
- ✅ Анализа русского контента
- ✅ Работы с русскоязычными API

## 📋 Как получить доступ к GigaChat

### Шаг 1: Авторизуйтесь на ctradei.com

Зайдите на сайт поставщика:
```
https://ctradei.com/
```

Логин: `bgrachik@yandex.ru`

### Шаг 2: Откройте "Мой GigaChat API"

1. Перейдите в личный кабинет
2. Найдите раздел "API"
3. Выберите "Мой GigaChat API"

### Шаг 3: Скопируйте учетные данные

На странице вы увидите три значения:

```
Authorization Key: MDE5ZTU0ZjgtNDA5M...
Client Secret: 48e7bc23-05a9-4661-e4f5-8e965b138c2
Client ID: 019e54f6-4092-7355-abe7-986275a009cb
```

**⚠️ ВАЖНО:** Сохраните эти данные в безопасном месте!

## ⚙️ Конфигурация

### Обновите .env файл

```bash
# GigaChat credentials из ctradei
GIGACHAT_CLIENT_ID=019e54f6-4092-7355-abe7-986275a009cb
GIGACHAT_CLIENT_SECRET=48e7bc23-05a9-4661-e4f5-8e965b138c2
GIGACHAT_SCOPE=GIGACHAT_API_PERS
GIGACHAT_MODEL=GigaChat
GIGACHAT_TEMPERATURE=0.7
USE_GIGACHAT=true
```

### Параметры

| Параметр | Описание | Пример |
|----------|---------|--------|
| `GIGACHAT_CLIENT_ID` | Client ID из ctradei | `019e54f6...` |
| `GIGACHAT_CLIENT_SECRET` | Client Secret из ctradei | `48e7bc23...` |
| `GIGACHAT_SCOPE` | Область доступа | `GIGACHAT_API_PERS` |
| `GIGACHAT_MODEL` | Модель | `GigaChat` |
| `GIGACHAT_TEMPERATURE` | Творческость ответов (0-2) | `0.7` |
| `USE_GIGACHAT` | Использовать GigaChat | `true` |

## 🚀 Как это работает

### Процесс обогащения товаров

1. **Получение товара с ctradei**
   ```
   Название: "Комплект постельного белья"
   Описание: "Хлопковый комплект"
   Цена: 2999₽
   ```

2. **Отправка GigaChat**
   ```
   Проанализируй товар для магазina wonderfulbed.ru...
   ```

3. **Получение обогащенных данных**
   ```json
   {
     "title": "Комплект белья хлопок 1,5-спального размера",
     "description": "Мягкий хлопковый комплект для комфортного сна",
     "features": ["Натуральный хлопок", "Яркие цвета", "Легко стирается"],
     "target_audience": "Семьи с детьми",
     "tags": ["хлопок", "уход за собой", "постель"]
   }
   ```

4. **Загрузка в wonderfulbed.ru**
   ```
   insales API → обновление товара
   ```

## 📊 Примеры промптов

### SEO оптимизация

```
Создай SEO-оптимизированное название (макс 60 символов) для товара:
"Постельное белье из хлопка"

Требования:
- Включить ключевые слова
- Быть привлекательным
- Подходить для поиска
```

### Анализ товара

```
Проанализируй преимущества товара "Постельное белье":
- Из какого материала?
- Какой размер?
- Для кого подходит?
- Уникальные особенности?

Формат: JSON с полями features, target_audience
```

## 🔧 Отладка

### Проверить соединение с GigaChat

```bash
curl -X POST /api/v1/parser/test
```

Ответ:
```json
{
  "gigachat": {
    "status": "connected",
    "message": "✅ GigaChat API доступен"
  }
}
```

### Просмотреть логи

```bash
docker-compose logs -f api | grep GigaChat
```

### Если GigaChat недоступен

Если GigaChat не подключается, парсер автоматически:
- ✅ Возвращает базовое описание товара
- ✅ Продолжает синхронизацию
- ✅ Логирует ошибку для отладки

## 📈 Примеры улучшения

### До использования GigaChat
```
Название: "Набор постельного белья"
Описание: "Набор белья"
```

### После GigaChat
```
Название: "Комплект постельного белья 1,5-спального размера из хлопка"
Описание: "Мягкий хлопковый комплект с яркими узорами для комфортного сна"
Теги: ["хлопок", "постель", "качество", "комфорт"]
```

## 🎯 Оптимизация

### Параметры качества

```env
# Высокое качество (медленнее)
GIGACHAT_TEMPERATURE=0.5

# Сбалансированное
GIGACHAT_TEMPERATURE=0.7

# Творческие ответы (быстрее)
GIGACHAT_TEMPERATURE=0.9
```

### Оптимизация скорости

```env
# Если GigaChat медленно отвечает
GIGACHAT_TIMEOUT=30  # секунд
GIGACHAT_RETRIES=3   # попытки
```

## 🔒 Безопасность

### Защита учетных данных

✅ **Никогда не коммитьте в Git:**
- GIGACHAT_CLIENT_ID
- GIGACHAT_CLIENT_SECRET

✅ **Используйте переменные окружения**

✅ **На production используйте:**
- Шифрование переменных
- Separate .env для каждого окружения
- Ограничение доступа по IP

## 📚 Полезные ссылки

- [GigaChat Документация](https://docs.gigachat.ai/)
- [ctradei API Docs](https://ctradei.com/api)
- [insales API Docs](https://insales.ru/developers)

## 🆘 Решение проблем

### Ошибка: "Invalid credentials"

```
❌ GigaChat auth failed: 401
```

**Решение:**
- Проверьте CLIENT_ID и CLIENT_SECRET
- Убедитесь что они скопированы полностью
- Проверьте права доступа на ctradei

### Ошибка: "Timeout"

```
❌ GigaChat request timeout
```

**Решение:**
- Увеличьте GIGACHAT_TIMEOUT
- Проверьте интернет соединение
- Попробуйте позже (может быть перегруз)

### Ошибка: "Rate limit"

```
❌ GigaChat rate limit exceeded
```

**Решение:**
- Добавьте задержку между запросами
- Используйте batch processing
- Обратитесь в support GigaChat

## 📞 Поддержка

По вопросам:
- Email: bgrachik@yandex.ru
- GitHub Issues: https://github.com/Grachik2007/TestGitHub/issues
- GigaChat Support: https://support.gigachat.ai/
