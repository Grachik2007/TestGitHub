#!/usr/bin/env python3
"""
Синхронизация товаров в insales
Загружает товары, цены, остатки и изображения в интернет-магазин insales
"""
import httpx
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class InsalesSync:
    """Синхронизация товаров и изображений в insales"""

    def __init__(self, shop_id: str, api_key: str, api_password: str):
        """
        Инициализация insales клиента

        Args:
            shop_id: ID магазина в insales
            api_key: API ключ
            api_password: API пароль
        """
        self.shop_id = shop_id
        self.api_key = api_key
        self.api_password = api_password
        self.base_url = f"https://{shop_id}.myinsales.ru"
        self.api_url = f"{self.base_url}/api/v1"

        # Заголовки для аутентификации
        self.headers = {
            "Authorization": f"Basic {self._encode_auth(api_key, api_password)}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @staticmethod
    def _encode_auth(api_key: str, api_password: str) -> str:
        """Кодирует учетные данные для Basic Auth"""
        import base64
        credentials = f"{api_key}:{api_password}"
        return base64.b64encode(credentials.encode()).decode()

    async def check_connection(self) -> bool:
        """Проверить соединение с insales"""
        print("🔗 Проверяю соединение с insales...")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.api_url}/shop.json",
                    headers=self.headers
                )
                if response.status_code == 200:
                    shop_data = response.json()
                    print(f"✅ Успешно подключено к магазину: {shop_data.get('shop', {}).get('title')}")
                    return True
                else:
                    print(f"❌ Ошибка: {response.status_code} - {response.text}")
                    return False
        except Exception as e:
            print(f"❌ Ошибка соединения: {e}")
            return False

    async def get_products(self, limit: int = 250, page: int = 1) -> Optional[List[Dict]]:
        """Получить список товаров из insales"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.api_url}/products.json",
                    headers=self.headers,
                    params={"limit": limit, "page": page}
                )
                if response.status_code == 200:
                    return response.json().get('products', [])
                else:
                    print(f"❌ Ошибка получения товаров: {response.status_code}")
                    return None
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return None

    async def create_product(self, product_data: Dict) -> Optional[Dict]:
        """Создать новый товар в insales"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_url}/products.json",
                    headers=self.headers,
                    json={"product": product_data}
                )
                if response.status_code in [200, 201]:
                    print(f"✅ Товар создан: {product_data.get('title')}")
                    return response.json().get('product')
                else:
                    print(f"❌ Ошибка создания товара: {response.status_code} - {response.text}")
                    return None
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return None

    async def update_product(self, product_id: int, product_data: Dict) -> bool:
        """Обновить товар в insales"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.put(
                    f"{self.api_url}/products/{product_id}.json",
                    headers=self.headers,
                    json={"product": product_data}
                )
                if response.status_code in [200, 204]:
                    print(f"✅ Товар обновлен: ID {product_id}")
                    return True
                else:
                    print(f"❌ Ошибка обновления: {response.status_code} - {response.text}")
                    return False
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return False

    async def upload_image(self, product_id: int, image_url: str) -> Optional[Dict]:
        """Загрузить изображение товара"""
        try:
            # Скачиваем изображение
            async with httpx.AsyncClient(timeout=30.0) as client:
                img_response = await client.get(image_url, follow_redirects=True)
                img_data = img_response.content

                # Загружаем в insales
                files = {'image[original_filename]': ('image.jpg', img_data, 'image/jpeg')}

                response = await client.post(
                    f"{self.api_url}/products/{product_id}/images.json",
                    headers={"Authorization": self.headers["Authorization"]},
                    files=files
                )

                if response.status_code in [200, 201]:
                    return response.json().get('image')
                else:
                    print(f"⚠️  Ошибка загрузки изображения: {response.status_code}")
                    return None
        except Exception as e:
            print(f"⚠️  Ошибка загрузки изображения: {e}")
            return None

    async def update_stock(self, product_id: int, quantity: int) -> bool:
        """Обновить остаток товара"""
        try:
            # Получаем SKU товара
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Сначала получаем товар
                product_response = await client.get(
                    f"{self.api_url}/products/{product_id}.json",
                    headers=self.headers
                )

                if product_response.status_code != 200:
                    return False

                product = product_response.json().get('product', {})
                skus = product.get('skus', [])

                if not skus:
                    print(f"⚠️  Нет SKU для товара {product_id}")
                    return False

                # Обновляем остаток для каждого SKU
                for sku in skus:
                    sku_id = sku.get('id')
                    response = await client.put(
                        f"{self.api_url}/skus/{sku_id}.json",
                        headers=self.headers,
                        json={
                            "sku": {
                                "quantity": quantity
                            }
                        }
                    )

                    if response.status_code not in [200, 204]:
                        print(f"⚠️  Ошибка обновления остатка: {response.status_code}")
                        return False

                print(f"✅ Остаток обновлен: ID {product_id} - {quantity} шт")
                return True

        except Exception as e:
            print(f"⚠️  Ошибка обновления остатка: {e}")
            return False

    async def sync_product(
        self,
        ctradei_product: Dict,
        existing_insales_products: Optional[List[Dict]] = None
    ) -> bool:
        """
        Синхронизировать товар из ctradei в insales

        Args:
            ctradei_product: Товар из unified-feed
            existing_insales_products: Список существующих товаров в insales
        """
        product_id = ctradei_product.get('id', '')
        name = ctradei_product.get('name', '')

        if not name:
            print(f"⚠️  Пропущен товар без названия")
            return False

        # Ищем товар в insales по внешнему ID
        insales_product = None
        if existing_insales_products:
            for p in existing_insales_products:
                external_id = p.get('external_id')
                if external_id == product_id:
                    insales_product = p
                    break

        # Подготавливаем данные товара для insales
        product_data = {
            "title": name,
            "description": ctradei_product.get('description', ''),
            "external_id": product_id,
            "sku": product_id,
            "price": ctradei_product.get('retail_price', 0),
            "supplier_price": ctradei_product.get('supplier_price', 0),
            "quantity": ctradei_product.get('stock', 0),
            "visible": True,
        }

        # Добавляем пользовательские поля для маржи
        custom_fields = {
            "Поставщик": "ctradei",
            "Маржа": f"{ctradei_product.get('margin_percent', 0):.1f}%",
            "Себестоимость": f"{ctradei_product.get('cost_price', 0):.0f}₽",
        }

        # Если товар существует - обновляем
        if insales_product:
            insales_product_id = insales_product.get('id')
            success = await self.update_product(insales_product_id, product_data)

            if success:
                # Обновляем остаток
                await self.update_stock(
                    insales_product_id,
                    ctradei_product.get('stock', 0)
                )

                # Загружаем изображения
                images = ctradei_product.get('images', [])
                for idx, image_url in enumerate(images[:5]):  # Первые 5 изображений
                    print(f"📸 Загружаю изображение {idx + 1}/{len(images[:5])}")
                    await self.upload_image(insales_product_id, image_url)

            return success

        # Если товара нет - создаем
        else:
            new_product = await self.create_product(product_data)

            if new_product:
                insales_product_id = new_product.get('id')

                # Загружаем изображения
                images = ctradei_product.get('images', [])
                for idx, image_url in enumerate(images[:5]):
                    print(f"📸 Загружаю изображение {idx + 1}/{len(images[:5])}")
                    await self.upload_image(insales_product_id, image_url)

                return True

            return False


async def sync_to_insales():
    """Основная функция синхронизации"""
    import os

    print("🚀 Синхронизация товаров в insales\n")

    # Получаем учетные данные из переменных окружения
    shop_id = os.getenv('INSALES_SHOP_ID')
    api_key = os.getenv('INSALES_API_KEY')
    api_password = os.getenv('INSALES_API_PASSWORD')

    if not all([shop_id, api_key, api_password]):
        print("❌ Не указаны учетные данные insales")
        print("Требуются переменные:")
        print("  - INSALES_SHOP_ID")
        print("  - INSALES_API_KEY")
        print("  - INSALES_API_PASSWORD")
        return

    # Инициализируем клиент
    insales = InsalesSync(shop_id, api_key, api_password)

    # Проверяем соединение
    if not await insales.check_connection():
        print("❌ Не удалось подключиться к insales")
        return

    print()

    # Получаем товары из unified-feed
    feed_path = Path("public/feeds/unified-feed.json")

    if not feed_path.exists():
        print("❌ Файл unified-feed.json не найден")
        print("Запустите ctradei_integrator.py сначала")
        return

    print(f"📖 Читаю фид: {feed_path}")
    with open(feed_path, 'r', encoding='utf-8') as f:
        feed = json.load(f)

    products = feed.get('products', [])
    print(f"📦 Загружено {len(products)} товаров из фида\n")

    if not products:
        print("⚠️  Нет товаров для синхронизации")
        return

    # Получаем существующие товары в insales
    print("📋 Получаю существующие товары из insales...")
    existing_products = await insales.get_products()
    if existing_products:
        print(f"✅ Найдено {len(existing_products)} товаров в insales\n")
    else:
        print("⚠️  Не удалось получить существующие товары\n")
        existing_products = []

    # Синхронизируем товары
    print("🔄 Синхронизирую товары...\n")

    synced_count = 0
    skipped_count = 0

    for idx, product in enumerate(products, 1):
        print(f"[{idx}/{len(products)}] Синхронизирую: {product.get('name', 'Unknown')}")

        success = await insales.sync_product(product, existing_products)

        if success:
            synced_count += 1
        else:
            skipped_count += 1

        print()

    # Итоги
    print("\n" + "=" * 60)
    print("📊 ИТОГИ СИНХРОНИЗАЦИИ:")
    print("=" * 60)
    print(f"✅ Синхронизировано: {synced_count}")
    print(f"⚠️  Пропущено: {skipped_count}")
    print(f"📦 Всего товаров: {len(products)}")
    print(f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Результаты по товарам
    if existing_products:
        print(f"\n📈 Обновленных товаров: {synced_count}")
        print(f"🆕 Новых товаров: {synced_count - len([p for p in existing_products])}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(sync_to_insales())
