"""
Smart Pricing Calculator Service
Расчет цен на основе маржи и расходов поставщика
"""
from typing import Dict, List, Optional
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class PricingConfig:
    """Конфигурация расчета цен"""
    base_margin_percent: float  # Базовая маржа (%)
    logistics_cost_percent: float  # Логистика (% от цены поставщика)
    platform_commission_percent: float  # Комиссия маркетплейса (%)
    fixed_costs_rub: float  # Фиксированные расходы за товар (руб)
    min_markup_percent: float = 15.0  # Минимальная маржа


@dataclass
class PricedProduct:
    """Товар с рассчитанной ценой"""
    product_id: str
    name: str
    supplier_price: float  # Цена поставщика
    cost_price: float  # Себестоимость (supplier + расходы)
    retail_price: float  # Розничная цена
    margin_rub: float  # Маржа в рублях
    margin_percent: float  # Маржа в процентах


class PricingCalculator:
    """Калькулятор цен товаров"""

    def __init__(self, config: PricingConfig):
        self.config = config

    def calculate_price(
        self,
        product_id: str,
        name: str,
        supplier_price: float,
        stock_qty: int = 1
    ) -> PricedProduct:
        """
        Рассчитать розничную цену товара

        Args:
            product_id: ID товара
            name: Название товара
            supplier_price: Цена поставщика (руб)
            stock_qty: Количество на складе

        Returns:
            PricedProduct с рассчитанной ценой
        """
        supplier_price = Decimal(str(supplier_price))

        # Расчет себестоимости
        logistics_cost = supplier_price * Decimal(
            str(self.config.logistics_cost_percent / 100)
        )
        platform_commission = supplier_price * Decimal(
            str(self.config.platform_commission_percent / 100)
        )
        fixed_costs = Decimal(str(self.config.fixed_costs_rub))

        cost_price = supplier_price + logistics_cost + platform_commission + fixed_costs

        # Расчет розничной цены с учетом маржи
        min_markup = Decimal(str(self.config.min_markup_percent / 100))
        base_markup = Decimal(str(self.config.base_margin_percent / 100))

        # Розничная цена = себестоимость * (1 + маржа)
        retail_price = cost_price * (1 + base_markup)

        # Проверка минимальной маржи
        min_price = cost_price * (1 + min_markup)
        if retail_price < min_price:
            retail_price = min_price

        # Округление до 99 (психологическое ценообразование)
        retail_price = self._round_price(float(retail_price))

        # Маржа в рублях и процентах
        margin_rub = float(retail_price - float(cost_price))
        margin_percent = (margin_rub / float(cost_price) * 100) if cost_price > 0 else 0

        return PricedProduct(
            product_id=product_id,
            name=name,
            supplier_price=float(supplier_price),
            cost_price=float(cost_price),
            retail_price=retail_price,
            margin_rub=margin_rub,
            margin_percent=margin_percent
        )

    def calculate_batch(
        self,
        products: List[Dict],
        stock_data: Optional[Dict[str, int]] = None
    ) -> List[PricedProduct]:
        """
        Рассчитать цены для группы товаров

        Args:
            products: Список товаров [{"id": "...", "name": "...", "price": 1000}, ...]
            stock_data: Данные об остатках {product_id: qty, ...}

        Returns:
            Список PricedProduct с рассчитанными ценами
        """
        priced_products = []

        for product in products:
            product_id = product.get("id") or product.get("product_id")
            name = product.get("name") or product.get("title")
            supplier_price = float(product.get("price", 0))

            if supplier_price <= 0:
                continue

            stock_qty = 1
            if stock_data:
                stock_qty = stock_data.get(product_id, 0)

            priced = self.calculate_price(
                product_id=product_id,
                name=name,
                supplier_price=supplier_price,
                stock_qty=stock_qty
            )
            priced_products.append(priced)

        return priced_products

    @staticmethod
    def _round_price(price: float) -> float:
        """Округление цены с психологическим эффектом (0.99)"""
        if price < 100:
            return price

        # Округляем до 100 и отнимаем 1 (психологическое ценообразование)
        base = round(price / 100) * 100
        return float(base - 1)

    def get_summary(self, products: List[PricedProduct]) -> Dict:
        """Получить итоговую статистику по ценам"""
        if not products:
            return {
                "total_products": 0,
                "avg_supplier_price": 0,
                "avg_retail_price": 0,
                "avg_margin_percent": 0,
                "total_margin_potential": 0
            }

        total_supplier = sum(p.supplier_price for p in products)
        total_retail = sum(p.retail_price for p in products)
        total_margin = sum(p.margin_rub for p in products)
        avg_margin_percent = sum(p.margin_percent for p in products) / len(products)

        return {
            "total_products": len(products),
            "avg_supplier_price": round(total_supplier / len(products), 2),
            "avg_retail_price": round(total_retail / len(products), 2),
            "avg_margin_percent": round(avg_margin_percent, 2),
            "total_margin_potential": round(total_margin, 2),
            "min_price": min(p.retail_price for p in products),
            "max_price": max(p.retail_price for p in products)
        }
