#!/usr/bin/env python3
"""
Генератор файлов для загрузки в insales
Создает CSV и YML в формате, требуемом insales.ru
"""
import json
import csv
from pathlib import Path
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def generate_insales_csv(products: list) -> str:
    """
    Генерирует CSV файл для insales
    Формат: https://help.insales.ru/articles/1206697
    """
    # Заголовки CSV для insales
    headers = [
        'Название',                    # title
        'Артикул',                     # sku/external_id
        'Описание',                    # description
        'Цена',                        # price
        'Валюта',                      # currency (RUB)
        'Наличие',                     # quantity (stock)
        'Категория',                   # category
        'Изображение',                 # image_url (первое)
        'URL товара',                  # product_url
        'Тип товара',                  # product_type
        'Производитель',               # manufacturer/brand
        'Поставщик',                   # supplier (ctradei)
        'Себестоимость',               # cost_price
        'Маржа %',                     # margin_percent
    ]

    output = '﻿'  # BOM для правильного кодирования в Excel
    writer_obj = csv.writer([])

    # Добавляем заголовок
    output += ','.join(f'"{h}"' for h in headers) + '\n'

    # Добавляем товары
    for product in products:
        values = [
            product.get('name', ''),                    # Название
            product.get('id', ''),                      # Артикул
            product.get('description', ''),             # Описание
            str(int(product.get('retail_price', 0))),  # Цена (целое число)
            'RUB',                                      # Валюта
            str(product.get('stock', 0)),              # Наличие
            'Постельное белье',                        # Категория
            product.get('images', [''])[0],            # Первое изображение
            product.get('url', ''),                    # URL товара
            'Товар',                                   # Тип товара
            'ctradei',                                 # Производитель
            'ctradei',                                 # Поставщик
            str(int(product.get('cost_price', 0))),   # Себестоимость
            f"{product.get('margin_percent', 0):.1f}", # Маржа %
        ]

        # Экранируем и добавляем строку
        row = ','.join(f'"{str(v).replace('"', '""')}"' for v in values)
        output += row + '\n'

    return output


def generate_insales_yml(products: list) -> str:
    """
    Генерирует YML файл для insales
    Формат совместим с требованиями insales
    """
    yml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    yml += '<yml_catalog date="%s">\n' % datetime.now().isoformat()
    yml += '<shop>\n'
    yml += '  <name>Wonderfulbed</name>\n'
    yml += '  <company>Wonderfulbed.ru</company>\n'
    yml += '  <url>https://wonderfulbed.ru</url>\n'

    # Валюты
    yml += '  <currencies>\n'
    yml += '    <currency id="RUR" rate="1"/>\n'
    yml += '  </currencies>\n'

    # Категории
    yml += '  <categories>\n'
    yml += '    <category id="1">Постельное белье</category>\n'
    yml += '    <category id="2">Одеяла</category>\n'
    yml += '    <category id="3">Подушки</category>\n'
    yml += '    <category id="4">Наматрасники</category>\n'
    yml += '  </categories>\n'

    # Доставка (опционально)
    yml += '  <delivery-options>\n'
    yml += '    <option cost="0" days="1"/>\n'
    yml += '  </delivery-options>\n'

    # Товары
    yml += '  <offers>\n'

    for idx, product in enumerate(products, 1):
        offer_id = product.get('id', f'WB-{idx:05d}')
        name = product.get('name', '')
        description = product.get('description', '')
        price = int(product.get('retail_price', 0))
        stock = product.get('stock', 0)
        available = 'true' if stock > 0 else 'false'

        yml += f'    <offer id="{offer_id}" available="{available}">\n'
        yml += f'      <url>{product.get("url", "")}</url>\n'
        yml += f'      <price>{price}</price>\n'
        yml += '      <currencyId>RUR</currencyId>\n'
        yml += '      <categoryId>1</categoryId>\n'

        # Добавляем все изображения
        images = product.get('images', [])
        for image_url in images[:10]:  # insales поддерживает до 10 изображений
            yml += f'      <picture>{image_url}</picture>\n'

        yml += f'      <name>{escape_xml(name)}</name>\n'
        yml += f'      <description>{escape_xml(description)}</description>\n'

        # Параметры товара
        yml += '      <param name="Артикул">' + escape_xml(str(product.get('id', ''))) + '</param>\n'
        yml += '      <param name="Остаток">' + str(stock) + ' шт</param>\n'
        yml += '      <param name="Поставщик">ctradei</param>\n'

        if 'cost_price' in product:
            yml += '      <param name="Себестоимость">' + str(int(product.get('cost_price', 0))) + ' ₽</param>\n'

        if 'margin_percent' in product:
            yml += '      <param name="Маржа">' + f"{product.get('margin_percent', 0):.1f}" + '%</param>\n'

        if 'supplier_price' in product:
            yml += '      <param name="Цена поставщика">' + str(int(product.get('supplier_price', 0))) + ' ₽</param>\n'

        yml += '    </offer>\n'

    yml += '  </offers>\n'
    yml += '</shop>\n'
    yml += '</yml_catalog>\n'

    return yml


def generate_insales_import_html(summary: dict, product_count: int) -> str:
    """Генерирует HTML страницу с инструкциями по импорту"""
    html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>insales Import Files - Wonderfulbed</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }}
        .file-card {{
            background: #f9f9f9;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
        }}
        .file-card h3 {{
            margin-top: 0;
            color: #667eea;
        }}
        .download-btn {{
            display: inline-block;
            padding: 12px 24px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
            margin-top: 10px;
            transition: all 0.3s ease;
        }}
        .download-btn:hover {{
            background: #5568d3;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}
        .csv-btn {{
            background: #10b981;
        }}
        .csv-btn:hover {{
            background: #059669;
        }}
        .yml-btn {{
            background: #f59e0b;
        }}
        .yml-btn:hover {{
            background: #d97706;
        }}
        .instruction-card {{
            background: #f0f7ff;
            border-left: 4px solid #3b82f6;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
        }}
        .instruction-card h3 {{
            margin-top: 0;
            color: #3b82f6;
        }}
        .instruction-card ol {{
            margin: 15px 0;
            padding-left: 20px;
        }}
        .instruction-card li {{
            margin: 8px 0;
            line-height: 1.6;
        }}
        .stats {{
            background: #f3f4f6;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .stat-item {{
            display: inline-block;
            margin-right: 30px;
            margin-bottom: 10px;
        }}
        .stat-label {{
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
        }}
        .stat-value {{
            color: #333;
            font-size: 24px;
            font-weight: bold;
        }}
        .warning {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0;
            color: #92400e;
        }}
        .success {{
            background: #d1fae5;
            border-left: 4px solid #10b981;
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0;
            color: #065f46;
        }}
        code {{
            background: #f3f4f6;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛒 insales Import Files</h1>
        <p class="subtitle">Файлы для импорта товаров в интернет-магазин insales</p>

        <div class="stats">
            <div class="stat-item">
                <div class="stat-label">Товаров</div>
                <div class="stat-value">{product_count}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Средняя цена</div>
                <div class="stat-value">{summary.get('avg_retail_price', 0):,.0f}₽</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Общая маржа</div>
                <div class="stat-value">{summary.get('avg_margin_percent', 0):.1f}%</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Потенциал</div>
                <div class="stat-value">{summary.get('total_margin_potential', 0):,.0f}₽</div>
            </div>
        </div>

        <h2>📥 Файлы для скачивания</h2>

        <div class="file-card">
            <h3>📊 CSV Файл (рекомендуется)</h3>
            <p>Классический формат для импорта товаров. Совместим со всеми версиями insales.</p>
            <p><strong>Содержит:</strong> Название, артикул, цена, остаток, категория, изображение, параметры</p>
            <a href="insales-import.csv" class="download-btn csv-btn">⬇️ Скачать CSV</a>
            <p style="color: #666; font-size: 12px; margin-top: 10px;">
                Размер: ~{product_count * 0.5:.0f} KB | Товаров: {product_count} | Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </div>

        <div class="file-card">
            <h3>📋 YML Файл</h3>
            <p>XML формат с полной информацией о товарах, включая все изображения.</p>
            <p><strong>Содержит:</strong> Полное описание, все изображения, параметры, маржа</p>
            <a href="insales-import.yml" class="download-btn yml-btn">⬇️ Скачать YML</a>
            <p style="color: #666; font-size: 12px; margin-top: 10px;">
                Размер: ~{product_count * 2:.0f} KB | Товаров: {product_count} | Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </div>

        <h2>📌 Инструкция по импорту в insales</h2>

        <div class="instruction-card">
            <h3>🔷 Вариант 1: Импорт через CSV (быстро)</h3>
            <ol>
                <li>Скачайте <strong>insales-import.csv</strong></li>
                <li>Откройте личный кабинет insales</li>
                <li>Перейдите в <strong>Товары → Импорт товаров</strong></li>
                <li>Выберите <strong>CSV файл</strong></li>
                <li>Загрузите скачанный <code>insales-import.csv</code></li>
                <li>Разберите соответствие полей (обычно автоматически)</li>
                <li>Нажмите <strong>"Импортировать"</strong></li>
                <li>Дождитесь завершения импорта</li>
            </ol>
        </div>

        <div class="instruction-card">
            <h3>📋 Вариант 2: Импорт через YML (с изображениями)</h3>
            <ol>
                <li>Скачайте <strong>insales-import.yml</strong></li>
                <li>Откройте личный кабинет insales</li>
                <li>Перейдите в <strong>Товары → Импорт товаров</strong></li>
                <li>Выберите <strong>YML файл</strong></li>
                <li>Загрузите скачанный <code>insales-import.yml</code></li>
                <li>Нажмите <strong>"Импортировать"</strong></li>
                <li>Товары будут загружены вместе со всеми изображениями</li>
            </ol>
        </div>

        <div class="warning">
            <strong>⚠️ Перед импортом:</strong>
            <ul>
                <li>Сделайте резервную копию существующих товаров</li>
                <li>Проверьте что валюта установлена на RUB</li>
                <li>Убедитесь что категория "Постельное белье" существует</li>
                <li>Если переимпортируете - товары обновятся по артикулу</li>
            </ul>
        </div>

        <div class="success">
            <strong>✅ После импорта проверьте:</strong>
            <ul>
                <li>Все товары загружены корректно</li>
                <li>Цены рассчитаны правильно (с маржей и расходами)</li>
                <li>Остатки обновлены из ctradei</li>
                <li>Изображения загружены и отображаются</li>
                <li>Параметры товаров видны (маржа, поставщик)</li>
            </ul>
        </div>

        <h2>📊 Что содержат файлы</h2>

        <div class="file-card">
            <h3>Расчет цен (Smart Pricing)</h3>
            <p>Каждая цена рассчитана по формуле:</p>
            <code>Розничная цена = (Цена поставщика + Логистика + Комиссия + Фиксированные) × (1 + Маржа)</code>
            <p style="margin-top: 10px; color: #666;">
                Пример: Товар стоит 2999₽<br>
                + Логистика (8%) = 240₽<br>
                + Комиссия (5%) = 150₽<br>
                + Фиксированные = 15₽<br>
                = Себестоимость 3404₽<br>
                × Маржа (35%) = <strong>4595₽ розничная цена</strong>
            </p>
        </div>

        <div class="file-card">
            <h3>Данные источников</h3>
            <p>Информация собирается из двух постоянных ссылок ctradei:</p>
            <ul style="margin: 10px 0; padding-left: 20px;">
                <li><strong>YML:</strong> https://ctradei.com/x/shop2_1410641-yml.xml</li>
                <li><strong>CSV:</strong> https://ctradei.com/f/ostatki_2020.csv</li>
            </ul>
            <p style="color: #666; margin-top: 10px; font-size: 12px;">
                YML обновляется каждые 15 минут на ctradei<br>
                CSV обновляется в реальном времени
            </p>
        </div>

        <h2>🔄 Автоматическое обновление</h2>

        <p>Файлы обновляются автоматически каждый день в <strong>00:30 MSK</strong>:</p>

        <div style="background: #f3f4f6; padding: 15px; border-radius: 6px; margin: 15px 0;">
            <strong>Процесс обновления:</strong>
            <ol style="margin: 10px 0; padding-left: 20px;">
                <li>GitHub Actions получает свежие данные с ctradei</li>
                <li>Применяет Smart Pricing расчеты</li>
                <li>Генерирует обновленные CSV и YML файлы</li>
                <li>Публикует файлы на этой странице</li>
                <li>Вы скачиваете и загружаете в insales</li>
            </ol>
        </div>

        <p style="margin-top: 30px; text-align: center; color: #999; font-size: 12px; border-top: 1px solid #e5e7eb; padding-top: 20px;">
            Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M:%S MSK')}<br>
            Источник данных: ctradei.com
        </p>
    </div>
</body>
</html>
"""
    return html


def escape_xml(text: str) -> str:
    """Экранирует спецсимволы для XML"""
    if not text:
        return ''
    text = str(text)
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text


async def main():
    """Основная функция"""
    print("🚀 Генерация файлов для insales\n")

    # Читаем unified-feed.json
    feed_path = Path("public/feeds/unified-feed.json")

    if not feed_path.exists():
        print("❌ Файл unified-feed.json не найден")
        print("Запустите ctradei_integrator.py сначала")
        return

    print(f"📖 Читаю фид: {feed_path}")
    with open(feed_path, 'r', encoding='utf-8') as f:
        feed = json.load(f)

    products = feed.get('products', [])
    summary = feed.get('summary', {})

    print(f"📦 Загружено {len(products)} товаров\n")

    if not products:
        print("⚠️  Нет товаров для обработки")
        return

    # Создаем директорию
    public_dir = Path("public")
    public_dir.mkdir(exist_ok=True)

    # Генерируем CSV
    print("📊 Генерирую CSV файл...")
    csv_content = generate_insales_csv(products)
    csv_file = public_dir / "insales-import.csv"
    csv_file.write_text(csv_content, encoding='utf-8-sig')
    print(f"✅ CSV создан: {csv_file}")
    print(f"   Размер: {csv_file.stat().st_size / 1024:.1f} KB\n")

    # Генерируем YML
    print("📋 Генерирую YML файл...")
    yml_content = generate_insales_yml(products)
    yml_file = public_dir / "insales-import.yml"
    yml_file.write_text(yml_content, encoding='utf-8')
    print(f"✅ YML создан: {yml_file}")
    print(f"   Размер: {yml_file.stat().st_size / 1024:.1f} KB\n")

    # Генерируем HTML страницу
    print("📄 Генерирую HTML страницу...")
    html_content = generate_insales_import_html(summary, len(products))
    html_file = public_dir / "insales-import.html"
    html_file.write_text(html_content, encoding='utf-8')
    print(f"✅ HTML создан: {html_file}")
    print(f"   URL: https://grachik2007.github.io/TestGitHub/insales-import.html\n")

    print("=" * 60)
    print("✅ ФАЙЛЫ ДЛЯ INSALES ГОТОВЫ!")
    print("=" * 60)
    print(f"\n📥 Скачивайте и загружайте в insales:")
    print(f"  CSV:  {csv_file}")
    print(f"  YML:  {yml_file}")
    print(f"\n📋 Инструкция: https://grachik2007.github.io/TestGitHub/insales-import.html")
    print(f"\n📊 Статистика:")
    print(f"  Товаров: {len(products)}")
    print(f"  Средняя цена: {summary.get('avg_retail_price', 0):,.0f}₽")
    print(f"  Маржа: {summary.get('avg_margin_percent', 0):.1f}%")
    print(f"  Потенциал: {summary.get('total_margin_potential', 0):,.0f}₽")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
