# 🛒 Интеграция insales - Полное руководство

Синхронизация товаров, цен, остатков и изображений в интернет-магазин insales.

## 📋 Требования

- ✅ Аккаунт на insales.ru
- ✅ ID магазина (shop_id)
- ✅ API ключ
- ✅ API пароль

## 🔑 Получение учетных данных insales

### Шаг 1: Войти в личный кабинет insales

```
https://www.insales.ru/ → Вход
```

### Шаг 2: Перейти в Настройки → API

```
Личный кабинет → Настройки → Интеграции → API
```

### Шаг 3: Создать API приложение

1. Нажмите "Создать приложение"
2. Укажите название: "Wonderfulbed Sync"
3. Выберите разрешения:
   - ✅ Products (чтение/запись)
   - ✅ Stock (чтение/запись)
   - ✅ Images (запись)
   - ✅ Orders (чтение)

### Шаг 4: Скопируйте учетные данные

```
Shop ID: your-shop-id (из URL: your-shop-id.myinsales.ru)
API Key: xxxxxxxxxxxxxxxx
API Password: yyyyyyyyyyyyyyyy
```

## 🔧 Конфигурация

### Способ 1: GitHub Secrets (рекомендуется)

Добавьте в GitHub Settings → Secrets and variables → Actions:

```
INSALES_SHOP_ID=your-shop-id
INSALES_API_KEY=your-api-key
INSALES_API_PASSWORD=your-api-password
```

### Способ 2: Переменные окружения (локально)

```bash
export INSALES_SHOP_ID=your-shop-id
export INSALES_API_KEY=your-api-key
export INSALES_API_PASSWORD=your-api-password
```

### Способ 3: Файл .env (локально)

```bash
# apps/api/.env
INSALES_SHOP_ID=your-shop-id
INSALES_API_KEY=your-api-key
INSALES_API_PASSWORD=your-api-password
```

## 🚀 Использование

### Локально (тестирование)

```bash
cd /home/user/TestGitHub

# Установить зависимости (если еще не установлены)
pip install httpx pydantic

# Установить переменные окружения
export INSALES_SHOP_ID=your-shop-id
export INSALES_API_KEY=your-api-key
export INSALES_API_PASSWORD=your-api-password

# Запустить интеграцию ctradei
python infrastructure/scripts/ctradei_integrator.py

# Синхронизировать с insales
python infrastructure/scripts/sync_insales.py
```

### Через GitHub Actions (автоматическая)

Добавьте этап синхронизации в `.github/workflows/generate-feed.yml`:

```yaml
- name: Sync products to insales
  env:
    INSALES_SHOP_ID: ${{ secrets.INSALES_SHOP_ID }}
    INSALES_API_KEY: ${{ secrets.INSALES_API_KEY }}
    INSALES_API_PASSWORD: ${{ secrets.INSALES_API_PASSWORD }}
  run: |
    python infrastructure/scripts/sync_insales.py
```

## 📊 Что синхронизируется

### Данные товара

```python
{
    "title": "Комплект постельного белья",           # Название
    "description": "Мягкий натуральный...",          # Описание
    "external_id": "WB-001",                         # ID товара
    "sku": "WB-001",                                 # SKU
    "price": 4595,                                   # Розничная цена (Smart Pricing)
    "supplier_price": 2999,                          # Цена поставщика
    "quantity": 15                                   # Остаток на складе
}
```

### Изображения

```
До 5 изображений на товар:
- Автоматически скачиваются из ctradei
- Загружаются в insales
- Первое изображение устанавливается как основное
```

### Пользовательские поля

```
Поставщик: ctradei
Маржа: 34.8%
Себестоимость: 3404₽
```

## 🔄 Процесс синхронизации

```
1. Получить unified-feed.json (из ctradei_integrator)
   ├── Товары
   ├── Цены (с Smart Pricing)
   ├── Остатки
   └── Изображения

2. Проверить соединение с insales API
   └── Аутентификация Basic Auth

3. Получить существующие товары в insales
   └── Поиск по external_id

4. Для каждого товара:
   ├── Если существует → Обновить
   ├── Если новый → Создать
   ├── Загрузить до 5 изображений
   └── Обновить остаток

5. Вывести отчет синхронизации
   ├── Количество синхронизированных товаров
   ├── Количество пропущенных товаров
   └── Время синхронизации
```

## 📈 Примеры интеграции

### Полный workflow (рекомендуется)

```yaml
# .github/workflows/daily-sync.yml
name: Daily Sync to insales

on:
  schedule:
    # 00:30 MSK каждый день
    - cron: '30 21 * * *'
  workflow_dispatch:  # Можно запустить вручную

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install httpx pydantic requests

      # 1. Получить данные из ctradei и применить Smart Pricing
      - name: Generate unified feed
        env:
          PRICING_MARGIN: '35.0'
          PRICING_LOGISTICS: '8.0'
          PRICING_COMMISSION: '5.0'
          PRICING_FIXED: '15.0'
          PRICING_MIN_MARKUP: '15.0'
        run: |
          python infrastructure/scripts/ctradei_integrator.py

      # 2. Синхронизировать с insales
      - name: Sync to insales
        env:
          INSALES_SHOP_ID: ${{ secrets.INSALES_SHOP_ID }}
          INSALES_API_KEY: ${{ secrets.INSALES_API_KEY }}
          INSALES_API_PASSWORD: ${{ secrets.INSALES_API_PASSWORD }}
        run: |
          python infrastructure/scripts/sync_insales.py

      # 3. Развернуть фиды на GitHub Pages
      - name: Deploy feeds
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

### Локальный тест

```bash
#!/bin/bash

# Установить переменные окружения
export INSALES_SHOP_ID=your-shop-id
export INSALES_API_KEY=your-api-key
export INSALES_API_PASSWORD=your-api-password

export PRICING_MARGIN=35.0
export PRICING_LOGISTICS=8.0
export PRICING_COMMISSION=5.0
export PRICING_FIXED=15.0
export PRICING_MIN_MARKUP=15.0

# 1. Генерировать фид
echo "1️⃣  Generating ctradei feed..."
python infrastructure/scripts/ctradei_integrator.py

# 2. Синхронизировать
echo ""
echo "2️⃣  Syncing to insales..."
python infrastructure/scripts/sync_insales.py

echo ""
echo "✅ Complete!"
```

## 🔐 Безопасность

### Защита учетных данных

```bash
# ❌ НИКОГДА не коммитьте в Git:
INSALES_API_KEY=...
INSALES_API_PASSWORD=...

# ✅ Используйте GitHub Secrets:
Settings → Secrets and variables → Actions

# ✅ Локально используйте .env (в .gitignore):
.env
.env.local
```

### Разрешения API

Убедитесь что приложение имеет только необходимые разрешения:

- ✅ Products (read, write) - для создания/обновления товаров
- ✅ Stock (read, write) - для обновления остатков
- ✅ Images (write) - для загрузки изображений
- ❌ Orders, Customers - если не требуются

## 📊 Мониторинг синхронизации

### Логирование

Скрипт выводит подробные логи:

```
🚀 Синхронизация товаров в insales

🔗 Проверяю соединение с insales...
✅ Успешно подключено к магазину: wonderfulbed.ru

📖 Читаю фид...
📦 Загружено 1247 товаров из фида

📋 Получаю существующие товары из insales...
✅ Найдено 150 товаров в insales

🔄 Синхронизирую товары...

[1/1247] Синхронизирую: Комплект постельного белья
✅ Товар обновлен: ID 123
📸 Загружаю изображение 1/5
✅ Остаток обновлен: ID 123 - 15 шт

[2/1247] Синхронизирую: Евро комплект...
✅ Товар создан: Евро комплект...

...

════════════════════════════════════════════════════════════════════════════
📊 ИТОГИ СИНХРОНИЗАЦИИ:
════════════════════════════════════════════════════════════════════════════
✅ Синхронизировано: 1247
⚠️  Пропущено: 0
📦 Всего товаров: 1247
⏰ Время: 2026-05-23 00:32:15
════════════════════════════════════════════════════════════════════════════
```

### Отчеты в insales

После синхронизации проверьте в insales:

1. **Товары** → Все товары (должны появиться новые или обновиться)
2. **Товары** → каждый товар:
   - Название ✅
   - Описание ✅
   - Цена ✅
   - Остаток ✅
   - Изображения (5 шт) ✅
   - Пользовательские поля (маржа, себестоимость) ✅

## 🚨 Решение проблем

### Ошибка: "Не указаны учетные данные insales"

```bash
# Проверьте что установлены переменные окружения:
echo $INSALES_SHOP_ID
echo $INSALES_API_KEY
echo $INSALES_API_PASSWORD

# Если пусто - установите их:
export INSALES_SHOP_ID=your-shop-id
export INSALES_API_KEY=your-key
export INSALES_API_PASSWORD=your-password
```

### Ошибка: "Не удалось подключиться к insales"

```bash
# Проверьте учетные данные:
- INSALES_SHOP_ID должен быть ID без ".myinsales.ru"
- INSALES_API_KEY и INSALES_API_PASSWORD скопированы без пробелов

# Проверьте соединение:
curl -X GET https://YOUR-SHOP-ID.myinsales.ru/api/v1/shop.json \
  -H "Authorization: Basic $(echo -n 'KEY:PASSWORD' | base64)"
```

### Ошибка: "401 Unauthorized"

```bash
# Неправильные учетные данные
# Проверьте что API приложение активно в insales

Личный кабинет → API → Проверить статус приложения
```

### Ошибка: "Товар не обновляется"

```bash
# Причины:
1. Внешний ID (external_id) не совпадает
   → Используйте одинаковый ID как в ctradei
   
2. Нет разрешения на запись товаров
   → Проверьте разрешения API приложения
   
3. Товар заблокирован в insales
   → Разблокируйте в личном кабинете
```

## 📚 Дополнительные ресурсы

- [insales API Документация](https://insales.ru/developers)
- [insales FAQ](https://help.insales.ru)
- [Проверка соединения API](https://insales.ru/developers/api)

## 🎯 Checklist перед запуском

- [ ] Создан API ключ в insales
- [ ] Скопированы SHOP_ID, API_KEY, API_PASSWORD
- [ ] Добавлены в GitHub Secrets
- [ ] Установлены разрешения на Products, Stock, Images
- [ ] Протестирован локально
- [ ] Проверено что товары появляются в insales
- [ ] Проверены изображения, цены, остатки
- [ ] Добавлен этап синхронизации в GitHub Actions (опционально)
- [ ] Документация обновлена
- [ ] Готово к production синхронизации!

---

**Все готово! Синхронизация с insales работает! 🚀**
