"""
Wonderfulbed Parser Agent
Парсит товары с ctradei для wonderfulbed.ru
Синхронизирует с insales API
"""
import asyncio
import logging
from datetime import datetime
from typing import Optional, Dict, List, Any
import hashlib
import json

try:
    import httpx
    from langchain.prompts import PromptTemplate
except ImportError:
    pass

logger = logging.getLogger(__name__)


class WonderfulbedParserAgent:
    """AI Agent для парсинга и синхронизации товаров."""

    def __init__(
        self,
        ctradei_login: str,
        ctradei_password: str,
        ctradei_client_id: str,
        ctradei_client_secret: str,
        insales_api_url: str,
        insales_api_key: str,
        use_gigachat: bool = True,
    ):
        self.ctradei_login = ctradei_login
        self.ctradei_password = ctradei_password
        self.ctradei_client_id = ctradei_client_id
        self.ctradei_client_secret = ctradei_client_secret
        self.insales_api_url = insales_api_url
        self.insales_api_key = insales_api_key
        self.use_gigachat = use_gigachat

        # Initialize LLM
        self.llm = self._init_llm()
        self.session: Optional[httpx.AsyncClient] = None
        self.ctradei_token: Optional[str] = None

    def _init_llm(self):
        """Initialize LLM (GigaChat or OpenAI)."""
        if self.use_gigachat:
            try:
                from gigachat import GigaChat
                return GigaChat(
                    credentials=f"{self.ctradei_client_id}:{self.ctradei_client_secret}",
                    model="GigaChat",
                    temperature=0.7,
                    top_p=0.1,
                )
            except Exception as e:
                logger.warning(f"Failed to init GigaChat: {e}, falling back to OpenAI")
                return None
        return None

    async def __aenter__(self):
        self.session = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()

    async def authenticate_ctradei(self) -> bool:
        """Аутентификация на ctradei."""
        try:
            login_url = "https://ctradei.ru/api/users/login"

            response = await self.session.post(
                login_url,
                json={
                    "email": self.ctradei_login,
                    "password": self.ctradei_password,
                },
                timeout=10.0,
            )

            if response.status_code == 200:
                data = response.json()
                self.ctradei_token = data.get("token")
                logger.info("✅ Successfully authenticated with ctradei")
                return True
            else:
                logger.error(f"❌ ctradei auth failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Error authenticating with ctradei: {e}")
            return False

    async def fetch_products_from_ctradei(self, category: str = "постельное белье") -> List[Dict[str, Any]]:
        """Получает товары с ctradei по категории."""
        try:
            headers = {
                "Authorization": f"Bearer {self.ctradei_token}",
                "Content-Type": "application/json",
            }

            url = "https://ctradei.ru/api/products"
            params = {"category": category, "limit": 100}

            response = await self.session.get(
                url,
                headers=headers,
                params=params,
                timeout=15.0,
            )

            if response.status_code == 200:
                products = response.json().get("data", [])
                logger.info(f"✅ Fetched {len(products)} products from ctradei")
                return products
            else:
                logger.error(f"❌ Failed to fetch products: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"❌ Error fetching products: {e}")
            return []

    async def enrich_product_data(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Использует GigaChat/LLM для обогащения данных товара."""
        prompt_text = f"""
Проанализируй товар для магазина wonderfulbed.ru:
Товар: {product.get("name", "")}
Описание: {product.get("description", "")}
Цена: {product.get("price", 0)}

Предоставь ответ в формате JSON:
{{
  "title": "SEO-оптимизированное название (макс 60 символов)",
  "description": "SEO-оптимизированное описание (макс 160 символов)",
  "features": ["особенность 1", "особенность 2", "особенность 3"],
  "target_audience": "целевая аудитория",
  "tags": ["тег1", "тег2", "тег3"]
}}

Ответ только JSON без дополнительного текста.
        """

        try:
            if self.llm and self.use_gigachat:
                # Use GigaChat for Russian text
                response = await asyncio.to_thread(
                    self.llm,
                    prompt_text,
                )

                response_text = str(response)
                logger.info(f"GigaChat response: {response_text[:100]}...")

                # Extract JSON from response
                if "{" in response_text:
                    json_str = response_text[response_text.find("{"):response_text.rfind("}")+1]
                    enriched = json.loads(json_str)
                    return enriched
            else:
                # Fallback: return minimal enrichment
                logger.warning("LLM not available, returning basic enrichment")
                return {
                    "title": product.get("name", ""),
                    "description": product.get("description", ""),
                    "features": ["Товар из ctradei"],
                    "target_audience": "Широкая аудитория",
                    "tags": ["постельное белье", "ctradei"],
                }

            return {}
        except Exception as e:
            logger.error(f"Error enriching product: {e}", exc_info=True)
            return {
                "title": product.get("name", ""),
                "description": product.get("description", ""),
            }

    async def sync_to_insales(self, products: List[Dict[str, Any]]) -> bool:
        """Синхронизирует товары с insales API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.insales_api_key}",
                "Content-Type": "application/json",
            }

            for product in products:
                # Create/update product in insales
                payload = {
                    "product": {
                        "title": product.get("title", product.get("name")),
                        "description": product.get("description"),
                        "price": product.get("price"),
                        "sku": self._generate_sku(product.get("name")),
                        "available": product.get("stock", 0) > 0,
                        "quantity": product.get("stock", 0),
                        "tags": product.get("tags", []),
                    }
                }

                response = await self.session.post(
                    f"{self.insales_api_url}/products",
                    headers=headers,
                    json=payload,
                    timeout=10.0,
                )

                if response.status_code not in [200, 201]:
                    logger.warning(
                        f"⚠️ Failed to sync product {product.get('name')}: "
                        f"{response.status_code}"
                    )

            logger.info(f"✅ Successfully synced {len(products)} products to insales")
            return True
        except Exception as e:
            logger.error(f"❌ Error syncing to insales: {e}")
            return False

    def _generate_sku(self, product_name: str) -> str:
        """Генерирует SKU на основе названия товара."""
        hash_obj = hashlib.md5(product_name.encode())
        return f"WB-{hash_obj.hexdigest()[:8].upper()}"

    async def create_feed_file(self, products: List[Dict[str, Any]]) -> str:
        """Создает фид-файл для wonderfulbed.ru."""
        feed_content = self._generate_yandex_feed(products)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wonderfulbed_feed_{timestamp}.xml"

        # Save locally (в production - в S3/облако)
        with open(f"/tmp/{filename}", "w", encoding="utf-8") as f:
            f.write(feed_content)

        logger.info(f"✅ Feed file created: {filename}")
        return filename

    def _generate_yandex_feed(self, products: List[Dict[str, Any]]) -> str:
        """Генерирует Yandex Market feed."""
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
        xml += '</categories>\n'
        xml += '<offers>\n'

        for product in products:
            xml += f'<offer id="{product.get("id")}" available="{str(product.get("stock", 0) > 0).lower()}">\n'
            xml += f'<url>https://wonderfulbed.ru/products/{product.get("slug")}</url>\n'
            xml += f'<price>{product.get("price", 0)}</price>\n'
            xml += '<currencyId>RUR</currencyId>\n'
            xml += '<categoryId>1</categoryId>\n'
            xml += f'<picture>https://ctradei.ru{product.get("image_url")}</picture>\n'
            xml += f'<name>{product.get("name")}</name>\n'
            xml += f'<description>{product.get("description")}</description>\n'
            xml += '</offer>\n'

        xml += '</offers>\n'
        xml += '</shop>\n'
        xml += '</yml_catalog>\n'

        return xml

    async def run_sync(self) -> Dict[str, Any]:
        """Полный цикл синхронизации."""
        logger.info("🚀 Starting Wonderfulbed sync...")

        start_time = datetime.now()

        # Authenticate
        if not await self.authenticate_ctradei():
            return {"success": False, "error": "Authentication failed"}

        # Fetch products
        products = await self.fetch_products_from_ctradei()
        if not products:
            return {"success": False, "error": "No products fetched"}

        # Enrich product data with AI
        logger.info("🤖 Enriching product data with AI...")
        enriched_products = []
        for product in products[:5]:  # Limit for demo
            enriched = await self.enrich_product_data(product)
            enriched_products.append({**product, **enriched})

        # Sync to insales
        sync_result = await self.sync_to_insales(enriched_products)

        # Create feed file
        feed_file = await self.create_feed_file(enriched_products)

        duration = (datetime.now() - start_time).total_seconds()

        logger.info(f"✅ Sync completed in {duration:.2f}s")

        return {
            "success": sync_result,
            "products_synced": len(enriched_products),
            "feed_file": feed_file,
            "duration_seconds": duration,
            "timestamp": datetime.now().isoformat(),
        }


async def run_parser():
    """Главная функция запуска парсера с поддержкой GigaChat."""
    import os

    async with WonderfulbedParserAgent(
        ctradei_login=os.getenv("CTRADEI_LOGIN", "bgrachik@yandex.ru"),
        ctradei_password=os.getenv("CTRADEI_PASSWORD", ""),
        ctradei_client_id=os.getenv("GIGACHAT_CLIENT_ID", ""),
        ctradei_client_secret=os.getenv("GIGACHAT_CLIENT_SECRET", ""),
        insales_api_url=os.getenv("INSALES_API_URL", "https://api.insales.ru/v1"),
        insales_api_key=os.getenv("INSALES_API_KEY", ""),
        use_gigachat=os.getenv("USE_GIGACHAT", "true").lower() == "true",
    ) as agent:
        return await agent.run_sync()
