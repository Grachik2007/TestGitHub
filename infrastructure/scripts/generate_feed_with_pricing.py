#!/usr/bin/env python3
"""
Генератор фидов с интеграцией ctradei и Smart Pricing
Скачивает товары с ctradei, рассчитывает цены, генерирует фиды
"""
import csv
import json
import httpx
from io import StringIO
from datetime import datetime
from pathlib import Path
from decimal import Decimal

# Путь для импорта
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from apps.api.services.pricing_calculator import PricingCalculator, PricingConfig


class CtradeiCSVParser:
    """Парсер CSV данных с ctradei"""

    CTRADEI_CSV_URL = "https://ctradei.com/f/ostatki_2020.csv"

    @staticmethod
    async def fetch_csv() -> str:
        """Скачать CSV с ctradei"""
        print(f"📥 Скачиваю CSV с ctradei...")
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    CtradeiCSVParser.CTRADEI_CSV_URL,
                    follow_redirects=True
                )
                response.raise_for_status()
                print(f"✅ CSV скачан ({len(response.text)} символов)")
                return response.text
        except Exception as e:
            print(f"❌ Ошибка при скачивании CSV: {e}")
            print(f"⚠️  Используются пример-товары")
            return None

    @staticmethod
    def parse_csv(csv_content: str) -> list:
        """Парсить CSV контент в список товаров"""
        if not csv_content:
            return []

        products = []
        try:
            # Определяем кодировку и разделитель
            lines = csv_content.strip().split('\n')
            if not lines:
                return []

            # Пробуем разные разделители (; или ,)
            first_line = lines[0]
            delimiter = ';' if ';' in first_line else ','

            reader = csv.DictReader(lines, delimiter=delimiter)

            for row in reader:
                # Ищем поля в разных форматах
                product_id = row.get('ID') or row.get('id') or row.get('Код') or row.get('код')
                name = row.get('Название') or row.get('name') or row.get('название')
                price_str = row.get('Цена') or row.get('price') or row.get('цена') or '0'
                stock_str = row.get('Остаток') or row.get('stock') or row.get('остаток') or '0'

                if not product_id or not name:
                    continue

                try:
                    price = float(price_str.replace(',', '.')) if price_str else 0
                    stock = int(float(stock_str.replace(',', '.'))) if stock_str else 0

                    if price > 0:
                        products.append({
                            'id': str(product_id),
                            'name': str(name),
                            'price': price,
                            'stock': max(0, stock),
                            'slug': str(name).lower().replace(' ', '-')[:50],
                            'description': f'{name} от поставщика ctradei'
                        })
                except (ValueError, TypeError) as e:
                    print(f"⚠️  Пропущена строка: {row} ({e})")
                    continue

            print(f"✅ Спарсено {len(products)} товаров из CSV")
            return products

        except Exception as e:
            print(f"❌ Ошибка при парсинге CSV: {e}")
            return []


def generate_yandex_feed(products: list) -> str:
    """Генерирует Yandex Market фид в формате XML с рассчитанными ценами."""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += f'<yml_catalog date="{datetime.now().isoformat()}">\n'
    xml += '<shop>\n'
    xml += '<name>Wonderfulbed</name>\n'
    xml += '<company>Wonderfulbed.ru</company>\n'
    xml += '<url>https://wonderfulbed.ru</url>\n'
    xml += '<currencies>\n'
    xml += '<currency id="RUR" rate="1"/>\n'
    xml += '</currencies>\n'
    xml += '<categories>\n'
    xml += '<category id="1">Постельное белье</category>\n'
    xml += '<category id="2">Товары для дома</category>\n'
    xml += '</categories>\n'
    xml += '<offers>\n'

    for idx, product in enumerate(products, 1):
        offer_id = f"WB-{idx:05d}"
        # Используем рассчитанную цену если есть, иначе исходную
        price = product.get('retail_price') or product.get('price', 0)

        xml += f'  <offer id="{offer_id}" available="{"true" if product.get("stock", 0) > 0 else "false"}">\n'
        xml += f'    <url>https://wonderfulbed.ru/products/{product.get("slug", f"product-{idx}")}</url>\n'
        xml += f'    <price>{price:.0f}</price>\n'
        xml += '    <currencyId>RUR</currencyId>\n'
        xml += '    <categoryId>1</categoryId>\n'
        xml += f'    <picture>https://via.placeholder.com/400x400?text={product.get("name", f"Product {idx}")}</picture>\n'
        xml += f'    <name>{product.get("name")}</name>\n'
        xml += f'    <description>{product.get("description", "")}</description>\n'

        # Добавляем информацию об остатках
        if product.get('stock'):
            xml += f'    <param name="Остаток на складе">{product.get("stock")} шт</param>\n'

        # Добавляем маржу если есть
        if 'margin_percent' in product:
            xml += f'    <param name="Маржа">{product.get("margin_percent"):.1f}%</param>\n'

        xml += '  </offer>\n'

    xml += '</offers>\n'
    xml += '</shop>\n'
    xml += '</yml_catalog>\n'

    return xml


def generate_google_merchant_feed(products: list) -> str:
    """Генерирует Google Merchant Center фид в формате XML с рассчитанными ценами."""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">\n'
    xml += '<channel>\n'
    xml += '<title>Wonderfulbed.ru Products</title>\n'
    xml += '<link>https://wonderfulbed.ru</link>\n'
    xml += '<description>Постельное белье и товары для дома</description>\n'

    for idx, product in enumerate(products, 1):
        price = product.get('retail_price') or product.get('price', 0)

        xml += '  <item>\n'
        xml += f'    <g:id>WB-{idx:05d}</g:id>\n'
        xml += f'    <title>{product.get("name")}</title>\n'
        xml += f'    <description>{product.get("description", "")}</description>\n'
        xml += f'    <g:price>{price:.0f} RUB</g:price>\n'
        xml += f'    <g:availability>{"in stock" if product.get("stock", 0) > 0 else "out of stock"}</g:availability>\n'
        xml += f'    <link>https://wonderfulbed.ru/products/{product.get("slug", f"product-{idx}")}</link>\n'
        xml += '<g:image_link>https://via.placeholder.com/400x400</g:image_link>\n'
        xml += '<g:product_category>Постельное белье</g:product_category>\n'
        xml += '  </item>\n'

    xml += '</channel>\n'
    xml += '</rss>\n'

    return xml


def generate_json_feed(products: list, pricing_summary: dict = None) -> str:
    """Генерирует JSON фид с информацией о ценах и маржах."""
    feed = {
        "shop": {
            "name": "Wonderfulbed",
            "url": "https://wonderfulbed.ru",
            "updated": datetime.now().isoformat(),
            "product_count": len(products),
            "products": products
        }
    }

    if pricing_summary:
        feed["pricing_info"] = pricing_summary

    return json.dumps(feed, ensure_ascii=False, indent=2)


async def main():
    """Основная функция генерации фидов с ctradei + Smart Pricing"""
    print("🚀 Генерация фидов с Smart Pricing Engine\n")

    # Парсим конфигурацию цен из переменных окружения или используем стандартные
    import os
    pricing_config = PricingConfig(
        base_margin_percent=float(os.getenv('PRICING_MARGIN', '35.0')),
        logistics_cost_percent=float(os.getenv('PRICING_LOGISTICS', '8.0')),
        platform_commission_percent=float(os.getenv('PRICING_COMMISSION', '5.0')),
        fixed_costs_rub=float(os.getenv('PRICING_FIXED', '15.0')),
        min_markup_percent=float(os.getenv('PRICING_MIN_MARKUP', '15.0'))
    )

    print(f"⚙️  Конфигурация цен:")
    print(f"   - Маржа: {pricing_config.base_margin_percent}%")
    print(f"   - Логистика: {pricing_config.logistics_cost_percent}%")
    print(f"   - Комиссия: {pricing_config.platform_commission_percent}%")
    print(f"   - Фиксированные расходы: {pricing_config.fixed_costs_rub}₽")
    print()

    # Создаем директорию public если её нет
    public_dir = Path("public")
    public_dir.mkdir(exist_ok=True)

    feeds_dir = public_dir / "feeds"
    feeds_dir.mkdir(exist_ok=True)

    # Получаем товары из ctradei CSV
    csv_content = await CtradeiCSVParser.fetch_csv()
    products = CtradeiCSVParser.parse_csv(csv_content) if csv_content else []

    # Если не смогли получить товары, используем примеры
    if not products:
        print("⚠️  Используются товары-примеры\n")
        products = [
            {
                "id": "WB-001",
                "name": "Комплект постельного белья хлопок 1,5-спального размера",
                "price": 2999,
                "stock": 15,
                "slug": "komplekt-belogo-khlop-1-5",
                "description": "Мягкий натуральный хлопковый комплект для комфортного сна"
            },
            {
                "id": "WB-002",
                "name": "Евро комплект постельного белья сатин",
                "price": 5999,
                "stock": 8,
                "slug": "evro-komplekt-satin-premium",
                "description": "Премиум сатиновое постельное белье"
            },
            {
                "id": "WB-003",
                "name": "Детское постельное белье с рисунками",
                "price": 1999,
                "stock": 25,
                "slug": "detskoe-belie-s-risunkami",
                "description": "Яркое детское постельное белье"
            },
        ]

    # Рассчитываем цены
    print("💰 Рассчитываю цены...\n")
    calculator = PricingCalculator(pricing_config)
    priced_products = calculator.calculate_batch(products)

    # Преобразуем в словари для фидов
    products_with_prices = []
    for orig, priced in zip(products, priced_products):
        product_dict = orig.copy()
        product_dict.update({
            'supplier_price': priced.supplier_price,
            'cost_price': priced.cost_price,
            'retail_price': priced.retail_price,
            'margin_rub': priced.margin_rub,
            'margin_percent': priced.margin_percent,
        })
        products_with_prices.append(product_dict)

    # Генерируем Yandex Market фид
    print("📋 Generating Yandex Market feed...")
    yandex_feed = generate_yandex_feed(products_with_prices)
    yandex_file = feeds_dir / "yandex-market.xml"
    yandex_file.write_text(yandex_feed, encoding='utf-8')
    print(f"✅ Yandex feed saved: {yandex_file}")
    print(f"   URL: https://grachik2007.github.io/TestGitHub/feeds/yandex-market.xml\n")

    # Генерируем Google Merchant Center фид
    print("📋 Generating Google Merchant feed...")
    google_feed = generate_google_merchant_feed(products_with_prices)
    google_file = feeds_dir / "google-merchant.xml"
    google_file.write_text(google_feed, encoding='utf-8')
    print(f"✅ Google feed saved: {google_file}")
    print(f"   URL: https://grachik2007.github.io/TestGitHub/feeds/google-merchant.xml\n")

    # Генерируем JSON фид
    print("📋 Generating JSON feed...")
    summary = calculator.get_summary(priced_products)
    json_feed = generate_json_feed(products_with_prices, summary)
    json_file = feeds_dir / "products.json"
    json_file.write_text(json_feed, encoding='utf-8')
    print(f"✅ JSON feed saved: {json_file}")
    print(f"   URL: https://grachik2007.github.io/TestGitHub/feeds/products.json\n")

    # Генерируем индекс страницу
    index_html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wonderfulbed Product Feeds</title>
    <style>
        body {{ font-family: sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; }}
        .feed-list {{ list-style: none; padding: 0; }}
        .feed-list li {{ margin: 15px 0; }}
        .feed-link {{ display: block; padding: 15px; background: #007bff; color: white; text-decoration: none; border-radius: 4px; }}
        .feed-link:hover {{ background: #0056b3; }}
        .feed-info {{ color: #666; font-size: 12px; margin-top: 5px; }}
        .timestamp {{ color: #999; font-size: 12px; margin-top: 20px; }}
        .stats {{ background: #f9f9f9; padding: 15px; border-radius: 4px; margin: 20px 0; }}
        .stat-item {{ margin: 8px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛒 Wonderfulbed Product Feeds</h1>
        <p>Товарные фиды для синхронизации товаров с маркетплейсами и интернет-магазинами</p>

        <h2>📋 Доступные фиды:</h2>
        <ul class="feed-list">
            <li>
                <a href="feeds/yandex-market.xml" class="feed-link">
                    🔗 Yandex Market Feed (XML)
                </a>
                <div class="feed-info">
                    Для Яндекс.Маркета и других маркетплейсов<br>
                    Обновляется автоматически в 00:30 MSK
                </div>
            </li>
            <li>
                <a href="feeds/google-merchant.xml" class="feed-link">
                    🔗 Google Merchant Center Feed (XML)
                </a>
                <div class="feed-info">
                    Для Google Shopping<br>
                    Обновляется автоматически в 00:30 MSK
                </div>
            </li>
            <li>
                <a href="feeds/products.json" class="feed-link">
                    🔗 Products JSON Feed
                </a>
                <div class="feed-info">
                    Для API и пользовательских интеграций<br>
                    Обновляется автоматически в 00:30 MSK
                </div>
            </li>
        </ul>

        <div class="stats">
            <h3>📊 Статистика синхронизации:</h3>
            <div class="stat-item">✅ Товаров обработано: {len(products_with_prices)}</div>
            <div class="stat-item">✅ Средняя цена поставщика: {summary.get('avg_supplier_price', 0):,.0f}₽</div>
            <div class="stat-item">✅ Средняя розничная цена: {summary.get('avg_retail_price', 0):,.0f}₽</div>
            <div class="stat-item">✅ Средняя маржа: {summary.get('avg_margin_percent', 0):.1f}%</div>
            <div class="stat-item">✅ Потенциал маржи: {summary.get('total_margin_potential', 0):,.0f}₽</div>
        </div>

        <h2>🤖 Онлайн-интерфейс агентов:</h2>
        <a href="agents.html" class="feed-link" style="display: inline-block; margin-top: 10px;">
            🎯 Перейти в интерфейс управления агентами
        </a>

        <div class="timestamp">
            Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M:%S MSK')}<br>
            Источник данных: ctradei.com (товары постельного белья)
        </div>
    </div>
</body>
</html>
"""

    index_file = public_dir / "index.html"
    index_file.write_text(index_html, encoding='utf-8')
    print(f"✅ Index page created: {index_file}\n")

    print("\n✅ Feed generation completed!")
    print("\n📊 Feed URLs:")
    print("  Yandex:  https://grachik2007.github.io/TestGitHub/feeds/yandex-market.xml")
    print("  Google:  https://grachik2007.github.io/TestGitHub/feeds/google-merchant.xml")
    print("  JSON:    https://grachik2007.github.io/TestGitHub/feeds/products.json")
    print("  Main:    https://grachik2007.github.io/TestGitHub/")
    print("  Agents:  https://grachik2007.github.io/TestGitHub/agents.html")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
