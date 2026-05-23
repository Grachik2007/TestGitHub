# 💰 Smart Pricing Engine - Полное руководство

Система автоматического расчета розничных цен на основе данных поставщика.

## 📊 Архитектура

```
ctradei CSV (поставщик)
        ↓
CSV Parser (получает товары и остатки)
        ↓
Smart Pricing Calculator (расчет цен)
        ↓
Feed Generator (XML/JSON)
        ↓
GitHub Pages (публикация)
```

## 🔧 Компоненты

### 1. **Pricing Calculator** (`apps/api/services/pricing_calculator.py`)

Ядро системы расчета цен с поддержкой:
- ✅ Базовая маржа (настраивается %)
- ✅ Логистические расходы
- ✅ Комиссия маркетплейса
- ✅ Фиксированные расходы
- ✅ Минимальная гарантированная маржа

**Формула расчета:**
```
Себестоимость = Цена поставщика + Логистика + Комиссия + Фиксированные расходы

Розничная цена = Себестоимость × (1 + Маржа)

Если Розничная цена < Себестоимость × (1 + Минимальная маржа):
    Розничная цена = Себестоимость × (1 + Минимальная маржа)

Психологическое ценообразование: цена округляется с .99
```

### 2. **Pricing API** (`apps/api/api/v1/endpoints/pricing.py`)

REST API для управления ценами:

```bash
# Получить конфигурацию
GET /api/v1/pricing/config?profile=wonderfulbed

# Обновить конфигурацию
POST /api/v1/pricing/config?profile=wonderfulbed
{
  "base_margin_percent": 35.0,
  "logistics_cost_percent": 8.0,
  "platform_commission_percent": 5.0,
  "fixed_costs_rub": 15.0,
  "min_markup_percent": 15.0
}

# Рассчитать цены для товаров
POST /api/v1/pricing/calculate
{
  "products": [
    {"id": "WB-001", "name": "Товар", "price": 1000},
    {"id": "WB-002", "name": "Товар", "price": 2000}
  ],
  "pricing_config": {
    "base_margin_percent": 35.0,
    ...
  }
}

# Получить статистику
POST /api/v1/pricing/summary
{...}

# Список профилей
GET /api/v1/pricing/profiles
```

### 3. **Pricing Settings UI** (`apps/web/app/(dashboard)/pricing/page.tsx`)

Красивый интерфейс для управления ценами:
- 📊 Интерактивные слайдеры для параметров
- 📈 Живой расчет цен
- 📋 Таблица с детализацией
- 💹 Статистика и аналитика

## 🔗 Интеграция с ctradei CSV

### Шаг 1: Скачать CSV файлы с ctradei

**Вариант A: Остатки товаров (текущие)**
```
https://ctradei.com/f/ostatki_2020.csv
```

**Вариант B: История остатков**
```
https://ctradei.com/f/ostatki_2020.csv (или другая дата)
```

Обе ссылки содержат:
- Товары с ID
- Цены поставщика
- Остатки на складе
- Характеристики товаров

### Шаг 2: Обновить CSV Parser

Обновить `apps/api/agents/wonderfulbed_parser.py`:

```python
import csv
import httpx
from pathlib import Path

class WonderfulbedParserAgent:
    def __init__(self, ctradei_csv_url: str, ...):
        self.ctradei_csv_url = ctradei_csv_url
        # ... другие параметры

    async def fetch_products_from_csv(self) -> List[Dict]:
        """Получить товары из CSV ctradei"""
        async with httpx.AsyncClient() as client:
            response = await client.get(self.ctradei_csv_url)
            response.raise_for_status()
            
        # Парсим CSV
        products = []
        lines = response.text.strip().split('\n')
        reader = csv.DictReader(lines, delimiter=';')
        
        for row in reader:
            products.append({
                'id': row['ID'] or row['product_id'],
                'name': row['Название'] or row['name'],
                'price': float(row['Цена'] or row['price']),
                'stock': int(row['Остаток'] or row['stock']) or 0,
                'sku': row.get('SKU', ''),
            })
        
        return products
```

### Шаг 3: Интегрировать в workflow

Обновить `.github/workflows/generate-feed.yml`:

```yaml
env:
  CTRADEI_CSV_URL: https://ctradei.com/f/ostatki_2020.csv
  PRICING_MARGIN: 35
  PRICING_LOGISTICS: 8

- name: Generate product feed with pricing
  run: |
    python infrastructure/scripts/generate_feed_with_pricing.py
```

### Шаг 4: Создать генератор фидов с ценами

Новый скрипт `infrastructure/scripts/generate_feed_with_pricing.py`:

```python
#!/usr/bin/env python3
import httpx
import csv
from io import StringIO
from pathlib import Path
from apps.api.services.pricing_calculator import (
    PricingCalculator, 
    PricingConfig
)

def generate_feed_with_pricing():
    # Получаем CSV с товарами
    csv_url = "https://ctradei.com/f/ostatki_2020.csv"
    response = httpx.get(csv_url)
    
    # Парсим CSV
    reader = csv.DictReader(StringIO(response.text), delimiter=';')
    products = []
    for row in reader:
        products.append({
            'id': row['ID'],
            'name': row['Название'],
            'price': float(row['Цена']),
            'stock': int(row['Остаток'])
        })
    
    # Рассчитываем цены
    config = PricingConfig(
        base_margin_percent=35.0,
        logistics_cost_percent=8.0,
        platform_commission_percent=5.0,
        fixed_costs_rub=15.0,
        min_markup_percent=15.0
    )
    calculator = PricingCalculator(config)
    priced = calculator.calculate_batch(products)
    
    # Генерируем фиды с рассчитанными ценами
    # ... код генерации XML/JSON с retail_price
```

## 💡 Примеры использования

### Пример 1: Расчет цены для одного товара

```python
from apps.api.services.pricing_calculator import PricingCalculator, PricingConfig

config = PricingConfig(
    base_margin_percent=35.0,
    logistics_cost_percent=8.0,
    platform_commission_percent=5.0,
    fixed_costs_rub=15.0,
    min_markup_percent=15.0
)

calculator = PricingCalculator(config)
priced = calculator.calculate_price(
    product_id="WB-001",
    name="Комплект постельного белья",
    supplier_price=2999.0
)

print(f"Цена поставщика: {priced.supplier_price}₽")
print(f"Себестоимость: {priced.cost_price}₽")
print(f"Розничная цена: {priced.retail_price}₽")
print(f"Маржа: {priced.margin_rub}₽ ({priced.margin_percent}%)")
```

**Результат:**
```
Цена поставщика: 2999₽
Себестоимость: 3374₽
Розничная цена: 4549₽
Маржа: 1175₽ (34.8%)
```

### Пример 2: Использование API

```bash
curl -X POST http://localhost:8000/api/v1/pricing/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "products": [
      {
        "id": "WB-001",
        "name": "Постельное белье",
        "price": 2999
      }
    ],
    "pricing_config": {
      "base_margin_percent": 35.0,
      "logistics_cost_percent": 8.0,
      "platform_commission_percent": 5.0,
      "fixed_costs_rub": 15.0,
      "min_markup_percent": 15.0
    }
  }'
```

### Пример 3: Несколько профилей ценообразования

```python
# Профиль "Бюджетный" - низкая маржа
config_budget = PricingConfig(
    base_margin_percent=20.0,
    logistics_cost_percent=10.0,
    platform_commission_percent=6.0,
    fixed_costs_rub=10.0,
    min_markup_percent=10.0
)

# Профиль "Премиум" - высокая маржа
config_premium = PricingConfig(
    base_margin_percent=50.0,
    logistics_cost_percent=5.0,
    platform_commission_percent=3.0,
    fixed_costs_rub=20.0,
    min_markup_percent=25.0
)

# Профиль "Сезонный" - учет сезонности
config_seasonal = PricingConfig(
    base_margin_percent=45.0,
    logistics_cost_percent=8.0,
    platform_commission_percent=5.0,
    fixed_costs_rub=25.0,
    min_markup_percent=20.0
)
```

## 📈 Стратегии ценообразования

### Базовая маржа

| Категория | Маржа | Обоснование |
|-----------|-------|-------------|
| Конкурентные товары | 20-25% | Низкая маржа, высокий оборот |
| Массовые товары | 30-40% | Оптимальный баланс |
| Уникальные товары | 50-100% | Высокая маржа, низкий оборот |
| Сезонные товары | 35-60% | В зависимости от сезона |

### Логистические расходы

| Доставка | % |
|----------|---|
| Самовывоз (0 расходов) | 0% |
| Локальная доставка | 3-5% |
| Региональная доставка | 8-12% |
| Россия (среднее) | 10-15% |

### Фиксированные расходы

| Тип расходов | Руб |
|--------------|-----|
| Обработка заказа | 5-10 |
| Упаковка товара | 5-15 |
| Документы/проверка | 2-5 |
| **Итого** | **15-30** |

## 🔄 Автоматическое обновление цен

### Ежедневная синхронизация

```yaml
# .github/workflows/generate-feed.yml
schedule:
  # Каждый день в 00:30 MSK
  - cron: '30 21 * * *'
```

**Процесс:**
1. GitHub Actions запускает workflow в 00:30 MSK
2. Скачивается актуальный CSV с ctradei
3. Парсятся товары и остатки
4. Рассчитываются цены по текущей конфигурации
5. Генерируются XML и JSON фиды
6. Публикуются на GitHub Pages
7. Фиды доступны по URL для маркетплейсов

## 🚀 Оптимизация цен

### Динамическое ценообразование

```python
# Увеличение цены при низких остатках
def calculate_dynamic_markup(stock_qty: int) -> float:
    if stock_qty < 5:
        return 1.15  # +15% маржа при дефиците
    elif stock_qty < 20:
        return 1.10  # +10% при низких остатках
    else:
        return 1.05  # +5% при нормальных остатках
```

### Сезонные скидки

```python
# Скидка в конце сезона
def calculate_seasonal_discount(date: datetime) -> float:
    month = date.month
    if month in [6, 7, 8]:  # Лето
        return 0.95  # -5% в летний период
    else:
        return 1.0  # Нормальная цена
```

## 📊 Мониторинг и аналитика

### Ключевые метрики

```json
{
  "total_products": 1247,
  "avg_supplier_price": 3299,
  "avg_retail_price": 4799,
  "avg_margin_percent": 34.5,
  "total_margin_potential": 1875000,
  "min_price": 1499,
  "max_price": 12999
}
```

### Аналитика прибыльности

- Товары с минимальной маржей
- Товары с максимальной маржей
- Средняя маржа по категориям
- Динамика цен во времени

## 🔒 Безопасность

### Защита от случайных ошибок

- ✅ Минимальная маржа предотвращает убытки
- ✅ Валидация цен поставщика
- ✅ Проверка остатков перед расчетом
- ✅ Логирование всех изменений цен

### Конфиденциальность

- ✅ Цены не публикуются в фидах для конкурентов
- ✅ Фиды содержат только розничные цены
- ✅ Аналитика доступна только авторизованным пользователям

## 🎯 Следующие шаги

1. ✅ Интегрировать CSV parser с ctradei
2. ✅ Добавить динамическое ценообразование
3. ✅ Реализовать сезонные скидки
4. ✅ Добавить аналитику по товарам
5. ✅ Настроить мониторинг цен

## 📞 Поддержка

Вопросы по Smart Pricing Engine:
- GitHub Issues: https://github.com/Grachik2007/TestGitHub/issues
- Email: bgrachik@yandex.ru
