#!/usr/bin/env python3
"""
Генератор товарного фида для wonderfulbed.ru
Создает XML фид из товаров ctradei
"""
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path

def generate_yandex_feed(products: list) -> str:
    """Генерирует Yandex Market фид в формате XML."""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<yml_catalog date="%s">\n' % datetime.now().isoformat()
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
        xml += f'  <offer id="{offer_id}" available="true">\n'
        xml += f'    <url>https://wonderfulbed.ru/products/{product.get("slug", f"product-{idx}")}</url>\n'
        xml += f'    <price>{product.get("price", 0)}</price>\n'
        xml += '    <currencyId>RUR</currencyId>\n'
        xml += '    <categoryId>1</categoryId>\n'
        xml += f'    <picture>https://via.placeholder.com/400x400?text={product.get("name", f"Product {idx}")}</picture>\n'
        xml += f'    <name>{product.get("title", product.get("name"))}</name>\n'
        xml += f'    <description>{product.get("description", "")}</description>\n'

        # Добавляем параметры товара
        if product.get("features"):
            for feature in product.get("features", [])[:3]:
                xml += f'    <param name="Особенность">{feature}</param>\n'

        xml += '  </offer>\n'

    xml += '</offers>\n'
    xml += '</shop>\n'
    xml += '</yml_catalog>\n'

    return xml


def generate_google_merchant_feed(products: list) -> str:
    """Генерирует Google Merchant Center фид в формате XML."""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">\n'
    xml += '<channel>\n'
    xml += '<title>Wonderfulbed.ru Products</title>\n'
    xml += '<link>https://wonderfulbed.ru</link>\n'
    xml += '<description>Постельное белье и товары для дома</description>\n'

    for idx, product in enumerate(products, 1):
        xml += '  <item>\n'
        xml += f'    <g:id>WB-{idx:05d}</g:id>\n'
        xml += f'    <title>{product.get("title", product.get("name"))}</title>\n'
        xml += f'    <description>{product.get("description", "")}</description>\n'
        xml += f'    <g:price>{product.get("price", 0)} RUB</g:price>\n'
        xml += '    <g:availability>in stock</g:availability>\n'
        xml += f'    <link>https://wonderfulbed.ru/products/{product.get("slug", f"product-{idx}")}</link>\n'
        xml += '<g:image_link>https://via.placeholder.com/400x400</g:image_link>\n'
        xml += '<g:product_category>Постельное белье</g:product_category>\n'

        if product.get("target_audience"):
            xml += f'    <g:target_demographic>{product.get("target_audience")}</g:target_demographic>\n'

        xml += '  </item>\n'

    xml += '</channel>\n'
    xml += '</rss>\n'

    return xml


def generate_sample_products() -> list:
    """Генерирует примеры товаров для демонстрации."""
    return [
        {
            "name": "Комплект постельного белья хлопок 1,5-спального размера",
            "title": "Комплект белья хлопок 1,5-спального размера",
            "description": "Мягкий натуральный хлопковый комплект для комфортного сна. Легко стирается, долговечен.",
            "price": 2999,
            "slug": "komplekt-belogo-khlop-1-5",
            "features": ["Натуральный хлопок", "Яркие цвета", "Легко стирается"],
            "target_audience": "Семьи с детьми"
        },
        {
            "name": "Евро комплект постельного белья сатин",
            "title": "Евро комплект белья сатин премиум качество",
            "description": "Премиум сатиновое постельное белье. Гладкое, блестящее, максимально комфортное.",
            "price": 5999,
            "slug": "evro-komplekt-satin-premium",
            "features": ["Премиум сатин", "Блестящее", "Комфортное"],
            "target_audience": "Люди, ценящие качество"
        },
        {
            "name": "Детское постельное белье с рисунками",
            "title": "Детский комплект белья с любимыми персонажами",
            "description": "Яркое детское постельное белье с рисунками. Безопасное для детской кожи.",
            "price": 1999,
            "slug": "detskoe-belie-s-risunkami",
            "features": ["Детское", "Яркое", "Безопасное"],
            "target_audience": "Дети"
        },
    ]


def main():
    """Основная функция генерации фидов."""
    print("🚀 Generating product feeds...")

    # Создаем директорию public если её нет
    public_dir = Path("public")
    public_dir.mkdir(exist_ok=True)

    feeds_dir = public_dir / "feeds"
    feeds_dir.mkdir(exist_ok=True)

    # TODO: В production здесь будет загрузка товаров с ctradei
    products = generate_sample_products()

    # Генерируем Yandex Market фид
    print("📋 Generating Yandex Market feed...")
    yandex_feed = generate_yandex_feed(products)
    yandex_file = feeds_dir / "yandex-market.xml"
    yandex_file.write_text(yandex_feed, encoding='utf-8')
    print(f"✅ Yandex feed saved: {yandex_file}")
    print(f"   URL: https://grachik2007.github.io/TestGitHub/feeds/yandex-market.xml")

    # Генерируем Google Merchant Center фид
    print("📋 Generating Google Merchant feed...")
    google_feed = generate_google_merchant_feed(products)
    google_file = feeds_dir / "google-merchant.xml"
    google_file.write_text(google_feed, encoding='utf-8')
    print(f"✅ Google feed saved: {google_file}")
    print(f"   URL: https://grachik2007.github.io/TestGitHub/feeds/google-merchant.xml")

    # Генерируем JSON фид для API
    print("📋 Generating JSON feed...")
    json_feed = {
        "shop": {
            "name": "Wonderfulbed",
            "url": "https://wonderfulbed.ru",
            "updated": datetime.now().isoformat(),
            "product_count": len(products),
            "products": products
        }
    }
    json_file = feeds_dir / "products.json"
    json_file.write_text(json.dumps(json_feed, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"✅ JSON feed saved: {json_file}")
    print(f"   URL: https://grachik2007.github.io/TestGitHub/feeds/products.json")

    # Создаем index.html для перенаправления
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
    </style>
</head>
<body>
    <div class="container">
        <h1>🛒 Wonderfulbed Product Feeds</h1>
        <p>Товарные фиды для синхронизации товаров с маркетплейсами</p>

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

        <h2>🤖 Онлайн-интерфейс агентов:</h2>
        <a href="agents.html" class="feed-link" style="display: inline-block; margin-top: 10px;">
            🎯 Перейти в интерфейс управления агентами
        </a>

        <div class="timestamp">
            Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M:%S MSK')}
        </div>
    </div>
</body>
</html>
"""

    index_file = public_dir / "index.html"
    index_file.write_text(index_html, encoding='utf-8')
    print(f"✅ Index page created: {index_file}")

    print("\n✅ Feed generation completed!")
    print("\n📊 Feed URLs:")
    print("  Yandex:  https://grachik2007.github.io/TestGitHub/feeds/yandex-market.xml")
    print("  Google:  https://grachik2007.github.io/TestGitHub/feeds/google-merchant.xml")
    print("  JSON:    https://grachik2007.github.io/TestGitHub/feeds/products.json")
    print("  Main:    https://grachik2007.github.io/TestGitHub/")


if __name__ == "__main__":
    main()
