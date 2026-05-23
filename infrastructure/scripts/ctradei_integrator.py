#!/usr/bin/env python3
"""
Интегратор ctradei - получает данные из YML и CSV
Объединяет товары, цены, изображения и остатки в единый фид
"""
import xml.etree.ElementTree as ET
import csv
import json
import httpx
from io import StringIO
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from apps.api.services.pricing_calculator import PricingCalculator, PricingConfig


class CtradeiYMLParser:
    """Парсер YML файла с ctradei"""

    CTRADEI_YML_URL = "https://ctradei.com/x/shop2_1410641-yml.xml"
    CSV_URL = "https://ctradei.com/f/ostatki_2020.csv"

    @staticmethod
    async def fetch_yml() -> Optional[str]:
        """Скачать YML с ctradei"""
        print(f"📥 Скачиваю YML с ctradei...")
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    CtradeiYMLParser.CTRADEI_YML_URL,
                    follow_redirects=True
                )
                response.raise_for_status()
                print(f"✅ YML скачан ({len(response.text)} символов)")
                return response.text
        except Exception as e:
            print(f"❌ Ошибка при скачивании YML: {e}")
            return None

    @staticmethod
    async def fetch_csv() -> Optional[str]:
        """Скачать CSV с ctradei"""
        print(f"📥 Скачиваю CSV с ctradei...")
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    CtradeiYMLParser.CSV_URL,
                    follow_redirects=True
                )
                response.raise_for_status()
                print(f"✅ CSV скачан ({len(response.text)} символов)")
                return response.text
        except Exception as e:
            print(f"❌ Ошибка при скачивании CSV: {e}")
            return None

    @staticmethod
    def parse_yml(yml_content: str) -> Dict[str, Dict]:
        """Парсить YML и извлечь товары с изображениями"""
        products_by_id = {}

        try:
            root = ET.fromstring(yml_content)

            # Пути для навигации по XML
            offers = root.findall('.//offer')

            print(f"📋 Найдено {len(offers)} товаров в YML")

            for offer in offers:
                offer_id = offer.get('id')
                if not offer_id:
                    continue

                # Извлекаем данные
                product = {
                    'id': offer_id,
                    'name': offer.findtext('name', ''),
                    'description': offer.findtext('description', ''),
                    'price': 0,  # Будет переписана из CSV
                    'images': [],
                    'url': offer.findtext('url', ''),
                    'category': offer.findtext('categoryId', ''),
                }

                # Извлекаем изображения
                pictures = offer.findall('picture')
                for picture in pictures:
                    picture_url = picture.text
                    if picture_url:
                        product['images'].append(picture_url)

                # Извлекаем параметры
                params = {}
                for param in offer.findall('param'):
                    param_name = param.get('name', '')
                    param_value = param.text or ''
                    params[param_name] = param_value

                product['params'] = params

                products_by_id[offer_id] = product

            print(f"✅ Спарсено {len(products_by_id)} товаров из YML")
            return products_by_id

        except Exception as e:
            print(f"❌ Ошибка при парсинге YML: {e}")
            return {}

    @staticmethod
    def parse_csv(csv_content: str) -> Dict[str, Dict]:
        """Парсить CSV для получения текущих цен и остатков"""
        stock_data = {}

        try:
            lines = csv_content.strip().split('\n')
            delimiter = ';' if ';' in lines[0] else ','

            reader = csv.DictReader(lines, delimiter=delimiter)

            for row in reader:
                product_id = row.get('ID') or row.get('id') or row.get('Код')
                price_str = row.get('Цена') or row.get('price') or '0'
                stock_str = row.get('Остаток') or row.get('stock') or '0'

                if not product_id:
                    continue

                try:
                    price = float(price_str.replace(',', '.'))
                    stock = int(float(stock_str.replace(',', '.')))

                    stock_data[str(product_id)] = {
                        'price': price,
                        'stock': max(0, stock),
                    }
                except (ValueError, TypeError):
                    continue

            print(f"✅ Спарсено {len(stock_data)} записей из CSV")
            return stock_data

        except Exception as e:
            print(f"❌ Ошибка при парсинге CSV: {e}")
            return {}

    @staticmethod
    def merge_data(yml_products: Dict, csv_stock: Dict) -> List[Dict]:
        """Объединить данные из YML и CSV"""
        merged = []

        for product_id, yml_product in yml_products.items():
            csv_data = csv_stock.get(product_id, {})

            merged_product = yml_product.copy()
            merged_product['price'] = csv_data.get('price', yml_product.get('price', 0))
            merged_product['stock'] = csv_data.get('stock', 0)

            merged.append(merged_product)

        print(f"✅ Объединено {len(merged)} товаров из YML и CSV")
        return merged


async def main():
    """Основная функция интеграции ctradei"""
    print("🚀 Интеграция ctradei (YML + CSV + Smart Pricing)\n")

    # Получаем конфигурацию цен
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
    print(f"   - Фиксированные: {pricing_config.fixed_costs_rub}₽\n")

    # Создаем директории
    public_dir = Path("public")
    public_dir.mkdir(exist_ok=True)
    feeds_dir = public_dir / "feeds"
    feeds_dir.mkdir(exist_ok=True)

    # Скачиваем данные
    yml_content = await CtradeiYMLParser.fetch_yml()
    csv_content = await CtradeiYMLParser.fetch_csv()
    print()

    # Парсим данные
    yml_products = CtradeiYMLParser.parse_yml(yml_content) if yml_content else {}
    csv_stock = CtradeiYMLParser.parse_csv(csv_content) if csv_content else {}
    print()

    # Объединяем
    merged_products = CtradeiYMLParser.merge_data(yml_products, csv_stock)

    if not merged_products:
        print("⚠️  Нет товаров для обработки")
        return

    # Рассчитываем цены
    print("💰 Рассчитываю цены...\n")
    calculator = PricingCalculator(pricing_config)
    priced_products = calculator.calculate_batch(merged_products)

    # Преобразуем в словари для фидов
    products_with_prices = []
    for orig, priced in zip(merged_products, priced_products):
        product_dict = orig.copy()
        product_dict.update({
            'supplier_price': priced.supplier_price,
            'cost_price': priced.cost_price,
            'retail_price': priced.retail_price,
            'margin_rub': priced.margin_rub,
            'margin_percent': priced.margin_percent,
        })
        products_with_prices.append(product_dict)

    # Генерируем единый фид с изображениями
    print("📊 Генерирую единый фид с изображениями и ценами...\n")

    unified_feed = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "source": "ctradei.com",
            "yml_url": "https://ctradei.com/x/shop2_1410641-yml.xml",
            "csv_url": "https://ctradei.com/f/ostatki_2020.csv",
            "update_frequency": "Every 15 minutes from ctradei",
            "pricing": {
                "margin": pricing_config.base_margin_percent,
                "logistics": pricing_config.logistics_cost_percent,
                "commission": pricing_config.platform_commission_percent,
                "fixed_costs": pricing_config.fixed_costs_rub,
                "min_markup": pricing_config.min_markup_percent,
            }
        },
        "summary": calculator.get_summary(priced_products),
        "products": products_with_prices
    }

    # Сохраняем основной фид
    feed_file = feeds_dir / "unified-feed.json"
    feed_file.write_text(
        json.dumps(unified_feed, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f"✅ Unified feed saved: {feed_file}")
    print(f"   URL: https://grachik2007.github.io/TestGitHub/feeds/unified-feed.json\n")

    # Генерируем Yandex фид с изображениями
    print("📋 Generating Yandex Market feed with images...\n")
    yandex_feed = generate_yandex_feed_with_images(products_with_prices)
    yandex_file = feeds_dir / "yandex-market.xml"
    yandex_file.write_text(yandex_feed, encoding='utf-8')
    print(f"✅ Yandex feed with images: {yandex_file}")
    print(f"   URL: https://grachik2007.github.io/TestGitHub/feeds/yandex-market.xml\n")

    # Генерируем Google фид с изображениями
    print("📋 Generating Google Merchant feed with images...\n")
    google_feed = generate_google_merchant_feed_with_images(products_with_prices)
    google_file = feeds_dir / "google-merchant.xml"
    google_file.write_text(google_feed, encoding='utf-8')
    print(f"✅ Google feed with images: {google_file}")
    print(f"   URL: https://grachik2007.github.io/TestGitHub/feeds/google-merchant.xml\n")

    # Создаем страницу со ссылками
    create_feeds_page(feeds_dir, calculator.get_summary(priced_products), len(products_with_prices))

    print("\n✅ Integration completed!")
    print("\n📊 Available feeds:")
    print("  Unified (JSON):  https://grachik2007.github.io/TestGitHub/feeds/unified-feed.json")
    print("  Yandex (XML):    https://grachik2007.github.io/TestGitHub/feeds/yandex-market.xml")
    print("  Google (XML):    https://grachik2007.github.io/TestGitHub/feeds/google-merchant.xml")
    print("  Dashboard:       https://grachik2007.github.io/TestGitHub/agents.html")


def generate_yandex_feed_with_images(products: List[Dict]) -> str:
    """Генерирует Yandex фид с изображениями"""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += f'<yml_catalog date="{datetime.now().isoformat()}">\n'
    xml += '<shop>\n'
    xml += '<name>Wonderfulbed</name>\n'
    xml += '<company>Wonderfulbed.ru</company>\n'
    xml += '<url>https://wonderfulbed.ru</url>\n'
    xml += '<currencies><currency id="RUR" rate="1"/></currencies>\n'
    xml += '<categories>\n'
    xml += '<category id="1">Постельное белье</category>\n'
    xml += '</categories>\n'
    xml += '<offers>\n'

    for idx, product in enumerate(products, 1):
        offer_id = product.get('id', f'WB-{idx:05d}')
        price = product.get('retail_price', product.get('price', 0))

        xml += f'  <offer id="{offer_id}" available="{"true" if product.get("stock", 0) > 0 else "false"}">\n'
        xml += f'    <name>{product.get("name", "")}</name>\n'
        xml += f'    <description>{product.get("description", "")}</description>\n'
        xml += f'    <price>{price:.0f}</price>\n'
        xml += '    <currencyId>RUR</currencyId>\n'
        xml += '    <categoryId>1</categoryId>\n'

        # Добавляем все изображения
        for image_url in product.get('images', [])[:10]:
            xml += f'    <picture>{image_url}</picture>\n'

        xml += f'    <url>{product.get("url", "")}</url>\n'

        # Дополнительная информация
        if product.get('stock'):
            xml += f'    <param name="Stock">{product.get("stock")} pcs</param>\n'
        if 'margin_percent' in product:
            xml += f'    <param name="Margin">{product.get("margin_percent"):.1f}%</param>\n'

        xml += '  </offer>\n'

    xml += '</offers>\n</shop>\n</yml_catalog>\n'
    return xml


def generate_google_merchant_feed_with_images(products: List[Dict]) -> str:
    """Генерирует Google Merchant фид с изображениями"""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">\n'
    xml += '<channel>\n'
    xml += '<title>Wonderfulbed.ru Products</title>\n'
    xml += '<link>https://wonderfulbed.ru</link>\n'
    xml += '<description>Bedding and home products</description>\n'

    for idx, product in enumerate(products, 1):
        offer_id = product.get('id', f'WB-{idx:05d}')
        price = product.get('retail_price', product.get('price', 0))

        xml += '  <item>\n'
        xml += f'    <g:id>{offer_id}</g:id>\n'
        xml += f'    <title>{product.get("name", "")}</title>\n'
        xml += f'    <description>{product.get("description", "")}</description>\n'
        xml += f'    <g:price>{price:.0f} RUB</g:price>\n'
        xml += f'    <g:availability>{"in stock" if product.get("stock", 0) > 0 else "out of stock"}</g:availability>\n'
        xml += f'    <link>{product.get("url", "")}</link>\n'

        # Главное изображение
        images = product.get('images', [])
        if images:
            xml += f'    <g:image_link>{images[0]}</g:image_link>\n'

            # Дополнительные изображения
            for image_url in images[1:10]:
                xml += f'    <g:additional_image_link>{image_url}</g:additional_image_link>\n'

        xml += '    <g:product_category>Bedding</g:product_category>\n'
        xml += '  </item>\n'

    xml += '</channel>\n</rss>\n'
    return xml


def create_feeds_page(feeds_dir: Path, summary: Dict, product_count: int):
    """Создает HTML страницу со ссылками на фиды"""
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wonderfulbed Feed - Unified ctradei Integration</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; margin-bottom: 10px; }}
        .subtitle {{ color: #666; margin-bottom: 30px; }}
        .feed-card {{ background: #f9f9f9; border-left: 4px solid #007bff; padding: 20px; margin: 15px 0; border-radius: 4px; }}
        .feed-card h3 {{ margin-top: 0; color: #007bff; }}
        .feed-url {{ background: #fff; padding: 10px; border-radius: 4px; border: 1px solid #ddd; font-family: monospace; font-size: 12px; word-break: break-all; margin: 10px 0; }}
        .badge {{ display: inline-block; padding: 4px 12px; background: #28a745; color: white; border-radius: 12px; font-size: 12px; margin-right: 10px; }}
        .stats {{ background: #e7f3ff; border-left: 4px solid #007bff; padding: 20px; border-radius: 4px; margin: 20px 0; }}
        .stat-item {{ margin: 8px 0; }}
        .stat-value {{ font-weight: bold; color: #007bff; }}
        .update-info {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; border-radius: 4px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛒 Wonderfulbed Unified Feed</h1>
        <p class="subtitle">Real-time product feed with images, prices & inventory from ctradei.com</p>

        <div class="update-info">
            <strong>⏰ Auto-Update Schedule:</strong><br>
            - ctradei YML: Every 15 minutes<br>
            - ctradei CSV: Real-time stock updates<br>
            - Our feeds: Daily at 00:30 MSK (00:30 UTC)<br>
            - All prices include Smart Pricing Engine calculations
        </div>

        <h2>📋 Available Feeds</h2>

        <div class="feed-card">
            <h3>🔗 Unified Feed (Recommended)</h3>
            <p>Complete product data with images, prices, margins & inventory</p>
            <span class="badge">JSON</span>
            <span class="badge">IMAGES</span>
            <span class="badge">PRICING</span>
            <div class="feed-url">https://grachik2007.github.io/TestGitHub/feeds/unified-feed.json</div>
            <p><strong>Use for:</strong> Custom integrations, mobile apps, data analysis</p>
        </div>

        <div class="feed-card">
            <h3>🔗 Yandex Market Feed</h3>
            <p>YML format with images for Russian marketplaces</p>
            <span class="badge">XML</span>
            <span class="badge">IMAGES</span>
            <div class="feed-url">https://grachik2007.github.io/TestGitHub/feeds/yandex-market.xml</div>
            <p><strong>Use for:</strong> Яндекс.Маркет, Авито, Юла</p>
        </div>

        <div class="feed-card">
            <h3>🔗 Google Merchant Feed</h3>
            <p>Google Shopping format with images</p>
            <span class="badge">XML</span>
            <span class="badge">IMAGES</span>
            <div class="feed-url">https://grachik2007.github.io/TestGitHub/feeds/google-merchant.xml</div>
            <p><strong>Use for:</strong> Google Shopping, Google Ads</p>
        </div>

        <div class="stats">
            <h3>📊 Synchronization Statistics</h3>
            <div class="stat-item">
                ✅ <strong>Products processed:</strong> <span class="stat-value">{product_count}</span>
            </div>
            <div class="stat-item">
                ✅ <strong>Avg supplier price:</strong> <span class="stat-value">{summary.get('avg_supplier_price', 0):,.0f}₽</span>
            </div>
            <div class="stat-item">
                ✅ <strong>Avg retail price:</strong> <span class="stat-value">{summary.get('avg_retail_price', 0):,.0f}₽</span>
            </div>
            <div class="stat-item">
                ✅ <strong>Avg margin:</strong> <span class="stat-value">{summary.get('avg_margin_percent', 0):.1f}%</span>
            </div>
            <div class="stat-item">
                ✅ <strong>Total margin potential:</strong> <span class="stat-value">{summary.get('total_margin_potential', 0):,.0f}₽</span>
            </div>
        </div>

        <h2>🔄 Data Sources</h2>
        <ul>
            <li><strong>YML:</strong> https://ctradei.com/x/shop2_1410641-yml.xml (Updated every 15 min)</li>
            <li><strong>CSV:</strong> https://ctradei.com/f/ostatki_2020.csv (Live stock data)</li>
            <li><strong>Pricing:</strong> Smart Pricing Engine (Custom margins & costs)</li>
        </ul>

        <h2>🎯 Integration Guide</h2>
        <p>Each feed is automatically updated and contains:</p>
        <ul>
            <li>Product names, descriptions & URLs</li>
            <li>Retail prices (calculated with Smart Pricing)</li>
            <li>Current stock levels</li>
            <li>Product images from ctradei</li>
            <li>Margin information</li>
            <li>Update timestamps</li>
        </ul>

        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #999; font-size: 12px;">
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S MSK')}</p>
            <p>Source: ctradei.com + Smart Pricing Engine</p>
        </div>
    </div>
</body>
</html>
"""
    feeds_page = Path("public") / "feeds.html"
    feeds_page.write_text(html, encoding='utf-8')
    print(f"✅ Feeds page created: {feeds_page}")
    print(f"   URL: https://grachik2007.github.io/TestGitHub/feeds.html")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
