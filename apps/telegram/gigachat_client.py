"""
GigaChat Client for Telegram Bot
Интеграция с GigaChat API для реальных AI ответов
"""

import os
import json
import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class GigaChatClient:
    def __init__(self):
        self.auth_key = os.getenv("GIGACHAT_AUTH_KEY", "")
        self.client_id = os.getenv("GIGACHAT_CLIENT_ID", "")
        self.client_secret = os.getenv("GIGACHAT_CLIENT_SECRET", "")
        self.access_token = None
        self.api_url = "https://gigachat.devices.sberbank.ru/api/v1"

        if not all([self.auth_key, self.client_id, self.client_secret]):
            logger.warning("GigaChat credentials not fully configured")

    async def get_token(self) -> Optional[str]:
        """Get access token from GigaChat."""
        try:
            response = requests.post(
                f"{self.api_url}/oauth",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                    "RqUID": self.client_id,
                },
                data={
                    "scope": "GIGACHAT_API_PERS",
                },
                auth=(self.client_id, self.client_secret),
                verify=False,
                timeout=10
            )

            if response.status_code == 200:
                self.access_token = response.json()["access_token"]
                return self.access_token
            else:
                logger.error(f"GigaChat auth failed: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error getting GigaChat token: {e}")
            return None

    async def send_message(self, message: str, system_prompt: str = None) -> Optional[str]:
        """Send message to GigaChat and get response."""
        try:
            if not self.access_token:
                token = await self.get_token()
                if not token:
                    return None

            system_msg = system_prompt or "Ты полезный помощник, ответствуй на русском языке коротко и по делу."

            payload = {
                "model": "GigaChat",
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": message}
                ],
                "temperature": 0.7,
                "top_p": 0.1,
                "max_tokens": 512
            }

            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.access_token}"
                },
                json=payload,
                verify=False,
                timeout=15
            )

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                return content.strip()
            else:
                logger.error(f"GigaChat request failed: {response.status_code}")
                logger.error(response.text)
                return None

        except Exception as e:
            logger.error(f"Error calling GigaChat: {e}")
            return None

    async def analyze_seo(self, url: str, query: str = None) -> Optional[str]:
        """Analyze website SEO."""
        prompt = f"""Проанализируй сайт {url} с точки зрения SEO.
{f'Запрос пользователя: {query}' if query else ''}

Дай 5 конкретных рекомендаций по улучшению:
1. Технические SEO
2. Оптимизация контента
3. Структура и разметка
4. Юзабилити сайта
5. Бэклинки и авторитет

Ответ структурирован, на русском, коротко и по делу."""

        system = "Ты SEO эксперт с 10-летним опытом. Даешь конкретные, действенные рекомендации."
        return await self.send_message(prompt, system)

    async def research_suppliers(self, product: str, query: str = None) -> Optional[str]:
        """Research suppliers for a product."""
        prompt = f"""Помоги найти поставщиков для товара: {product}
{f'Дополнительная информация: {query}' if query else ''}

Дай:
1. Какие маркетплейсы использовать (Alibaba, 1688, ctradei и т.д.)
2. На какие параметры обращать внимание
3. Как проверить надежность поставщика
4. Примерные сроки доставки
5. Рекомендации по переговорам

Кратко и по делу."""

        system = "Ты опытный импортер товаров из Китая и Азии. Даешь практические советы."
        return await self.send_message(prompt, system)

    async def research_products(self, niche: str, query: str = None) -> Optional[str]:
        """Research products in a niche."""
        prompt = f"""Помоги исследовать рынок товаров в нише: {niche}
{f'Уточнение: {query}' if query else ''}

Дай анализ:
1. Спрос на товары в этой нише (России)
2. Основные конкуренты
3. Ценовой диапазон
4. Главные критерии выбора покупателей
5. Рекомендации по продвижению

Практично, на русском, коротко."""

        system = "Ты эксперт по интернет-коммерции и маркетплейсам. Помогаешь найти прибыльные ниши."
        return await self.send_message(prompt, system)

    async def optimize_pricing(self, product: str, cost: float, query: str = None) -> Optional[str]:
        """Get pricing recommendations."""
        prompt = f"""Помоги оптимизировать цену для товара: {product}
Себестоимость: {cost}₽
{f'Контекст: {query}' if query else ''}

Рекомендации:
1. Оптимальная розничная цена
2. Учет конкуренции
3. Психологическая цена
4. Скидочная стратегия
5. Сезонность и тренды

Конкретные числа и обоснование."""

        system = "Ты эксперт по ценообразованию. Помогаешь максимизировать прибыль без потери продаж."
        return await self.send_message(prompt, system)
