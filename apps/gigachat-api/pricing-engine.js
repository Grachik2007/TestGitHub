// Smart Pricing Engine для Wonderfulbed
// Автоматический расчёт цен на основе расходов и маржи

class PricingEngine {
  constructor() {
    // Базовые расходы (в рублях)
    this.WHOLESALE_COST = 1000; // Закупочная цена товара
    this.PACKAGING_DELIVERY_IN = 200; // Упаковка + доставка от поставщика
    this.DELIVERY_OUT = 400; // Доставка до клиента
    this.COMMISSION_RATE = 0.12; // Комиссия 12% от цены
    this.INSURANCE_RATE = 0.05; // Страховка 5% от цены
    this.TAX_RATE = 0.20; // УСН 20% от (цена - расходы)
    this.TARGET_MARGIN = 0.30; // Целевая маржа 30%
  }

  // Главная функция расчёта цены
  calculatePrice(costOfGoods = this.WHOLESALE_COST, targetMargin = this.TARGET_MARGIN) {
    const fixedCosts = this.PACKAGING_DELIVERY_IN + this.DELIVERY_OUT;
    const totalFixedCosts = costOfGoods + fixedCosts;

    // Формула: цена = (фиксированные расходы + маржа) / (1 - переменные%)
    // Где переменные = комиссия + страховка + налог от (цена - фиксированные расходы)

    // Упрощённо: цена = фиксированные / (1 - (коммиссия + страховка + налог*маржинальность))
    const variableRatio = this.COMMISSION_RATE + this.INSURANCE_RATE +
                          (this.TAX_RATE * (1 - targetMargin));

    const salePrice = totalFixedCosts / (1 - variableRatio);

    return Math.round(salePrice);
  }

  // Детальный расчёт со всеми показателями
  getDetailedCalculation(salePrice, costOfGoods = this.WHOLESALE_COST) {
    const packaging = this.PACKAGING_DELIVERY_IN;
    const deliveryOut = this.DELIVERY_OUT;
    const commission = Math.round(salePrice * this.COMMISSION_RATE);
    const insurance = Math.round(salePrice * this.INSURANCE_RATE);

    const taxableIncome = salePrice - costOfGoods - packaging - deliveryOut - commission - insurance;
    const tax = Math.round(taxableIncome * this.TAX_RATE);

    const totalCosts = costOfGoods + packaging + deliveryOut + commission + insurance + tax;
    const profit = salePrice - totalCosts;
    const margin = profit / salePrice;

    return {
      salePrice,
      costs: {
        wholesale: costOfGoods,
        packagingDeliveryIn: packaging,
        deliveryOut: deliveryOut,
        commission: commission,
        insurance: insurance,
        tax: tax,
        total: totalCosts
      },
      profit,
      margin: Math.round(margin * 100) / 100,
      marginPercent: Math.round(margin * 100)
    };
  }

  // Расчёт с учётом конкурентов
  calculateCompetitivePrice(costOfGoods, minMarketPrice, maxMarketPrice) {
    const optimalPrice = this.calculatePrice(costOfGoods);
    const avgMarketPrice = (minMarketPrice + maxMarketPrice) / 2;

    // Если оптимальная цена выше средней - можем снизить
    if (optimalPrice > avgMarketPrice) {
      return {
        recommended: Math.round(avgMarketPrice * 0.95), // -5% от средней
        optimal: optimalPrice,
        position: 'competitive'
      };
    }

    return {
      recommended: optimalPrice,
      optimal: optimalPrice,
      position: 'strong'
    };
  }

  // Проверка минимальной маржи
  getMinimumPrice(costOfGoods = this.WHOLESALE_COST, minMargin = 0.20) {
    const fixedCosts = this.PACKAGING_DELIVERY_IN + this.DELIVERY_OUT;
    const totalFixedCosts = costOfGoods + fixedCosts;
    const variableRatio = this.COMMISSION_RATE + this.INSURANCE_RATE +
                          (this.TAX_RATE * (1 - minMargin));
    return Math.round(totalFixedCosts / (1 - variableRatio));
  }

  // Максимальная цена (с учётом конкуренции)
  getMaximumPrice(costOfGoods = this.WHOLESALE_COST) {
    return this.calculatePrice(costOfGoods, 0.45); // 45% маржа
  }

  // Рекомендация для агента
  getPriceRecommendation(product) {
    const price = this.calculatePrice(product.cost);
    const calc = this.getDetailedCalculation(price, product.cost);

    return {
      productId: product.id,
      productName: product.name,
      recommendedPrice: price,
      calculation: calc,
      message: `📊 Рекомендуемая цена: ${price}₽ | Маржа: ${calc.marginPercent}% | Прибыль: ${calc.profit}₽`
    };
  }
}

// Экспорт для использования в агентах
module.exports = PricingEngine;
