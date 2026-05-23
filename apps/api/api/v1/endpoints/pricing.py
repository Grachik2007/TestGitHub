"""
Pricing Management API Endpoints
Управление ценообразованием и маржами
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
import json

router = APIRouter(prefix="/api/v1/pricing", tags=["pricing"])


class PricingConfigSchema(BaseModel):
    """Схема конфигурации цен"""
    base_margin_percent: float = Field(
        default=35.0,
        description="Базовая маржа в процентах"
    )
    logistics_cost_percent: float = Field(
        default=8.0,
        description="Стоимость логистики (% от цены поставщика)"
    )
    platform_commission_percent: float = Field(
        default=5.0,
        description="Комиссия маркетплейса (% от цены поставщика)"
    )
    fixed_costs_rub: float = Field(
        default=15.0,
        description="Фиксированные расходы на товар в рублях"
    )
    min_markup_percent: float = Field(
        default=15.0,
        description="Минимальная гарантированная маржа (%)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "base_margin_percent": 35.0,
                "logistics_cost_percent": 8.0,
                "platform_commission_percent": 5.0,
                "fixed_costs_rub": 15.0,
                "min_markup_percent": 15.0
            }
        }


class ProductPriceSchema(BaseModel):
    """Схема товара с расчетной ценой"""
    product_id: str
    name: str
    supplier_price: float = Field(description="Цена поставщика")
    cost_price: float = Field(description="Себестоимость")
    retail_price: float = Field(description="Розничная цена")
    margin_rub: float = Field(description="Маржа в рублях")
    margin_percent: float = Field(description="Маржа в процентах")


class PricingSummarySchema(BaseModel):
    """Итоговая статистика по ценам"""
    total_products: int
    avg_supplier_price: float
    avg_retail_price: float
    avg_margin_percent: float
    total_margin_potential: float
    min_price: float
    max_price: float


class PriceCalculationRequest(BaseModel):
    """Запрос на расчет цены"""
    products: List[dict] = Field(
        description="Список товаров [{'id': '...', 'name': '...', 'price': 1000}, ...]"
    )
    pricing_config: PricingConfigSchema = Field(
        default_factory=PricingConfigSchema,
        description="Конфигурация расчета цен"
    )


# Хранилище конфигурации (в production использовать БД)
_pricing_configs = {
    "default": PricingConfigSchema(),
    "wonderfulbed": PricingConfigSchema(
        base_margin_percent=40.0,
        logistics_cost_percent=10.0,
        platform_commission_percent=5.0,
        fixed_costs_rub=20.0,
        min_markup_percent=20.0
    )
}


@router.get("/config", response_model=PricingConfigSchema)
async def get_pricing_config(profile: str = Query("default", description="Профиль конфигурации")):
    """Получить конфигурацию цен"""
    if profile not in _pricing_configs:
        raise HTTPException(status_code=404, detail=f"Profile '{profile}' not found")
    return _pricing_configs[profile]


@router.post("/config", response_model=PricingConfigSchema)
async def update_pricing_config(
    config: PricingConfigSchema,
    profile: str = Query("default", description="Профиль конфигурации")
):
    """Обновить конфигурацию цен"""
    _pricing_configs[profile] = config
    return config


@router.post("/calculate", response_model=List[ProductPriceSchema])
async def calculate_prices(request: PriceCalculationRequest):
    """
    Рассчитать розничные цены для товаров

    Пример запроса:
    ```json
    {
      "products": [
        {
          "id": "WB-001",
          "name": "Комплект постельного белья",
          "price": 1500
        }
      ],
      "pricing_config": {
        "base_margin_percent": 35.0,
        "logistics_cost_percent": 8.0,
        "platform_commission_percent": 5.0,
        "fixed_costs_rub": 15.0,
        "min_markup_percent": 15.0
      }
    }
    ```
    """
    from apps.api.services.pricing_calculator import PricingCalculator, PricingConfig

    # Создаем конфиг
    pricing_config = PricingConfig(
        base_margin_percent=request.pricing_config.base_margin_percent,
        logistics_cost_percent=request.pricing_config.logistics_cost_percent,
        platform_commission_percent=request.pricing_config.platform_commission_percent,
        fixed_costs_rub=request.pricing_config.fixed_costs_rub,
        min_markup_percent=request.pricing_config.min_markup_percent
    )

    calculator = PricingCalculator(pricing_config)
    priced_products = calculator.calculate_batch(request.products)

    return [
        ProductPriceSchema(
            product_id=p.product_id,
            name=p.name,
            supplier_price=p.supplier_price,
            cost_price=p.cost_price,
            retail_price=p.retail_price,
            margin_rub=p.margin_rub,
            margin_percent=p.margin_percent
        )
        for p in priced_products
    ]


@router.post("/summary")
async def get_pricing_summary(request: PriceCalculationRequest) -> PricingSummarySchema:
    """Получить итоговую статистику по ценам"""
    from apps.api.services.pricing_calculator import PricingCalculator, PricingConfig

    pricing_config = PricingConfig(
        base_margin_percent=request.pricing_config.base_margin_percent,
        logistics_cost_percent=request.pricing_config.logistics_cost_percent,
        platform_commission_percent=request.pricing_config.platform_commission_percent,
        fixed_costs_rub=request.pricing_config.fixed_costs_rub,
        min_markup_percent=request.pricing_config.min_markup_percent
    )

    calculator = PricingCalculator(pricing_config)
    priced_products = calculator.calculate_batch(request.products)
    summary = calculator.get_summary(priced_products)

    return PricingSummarySchema(**summary)


@router.get("/profiles")
async def list_pricing_profiles():
    """Получить список всех профилей ценообразования"""
    return {
        "profiles": list(_pricing_configs.keys()),
        "default": "default"
    }
