'use client';

import { useState } from 'react';

interface PricingConfig {
  base_margin_percent: number;
  logistics_cost_percent: number;
  platform_commission_percent: number;
  fixed_costs_rub: number;
  min_markup_percent: number;
}

interface ProductPrice {
  product_id: string;
  name: string;
  supplier_price: number;
  cost_price: number;
  retail_price: number;
  margin_rub: number;
  margin_percent: number;
}

interface PricingSummary {
  total_products: number;
  avg_supplier_price: number;
  avg_retail_price: number;
  avg_margin_percent: number;
  total_margin_potential: number;
  min_price: number;
  max_price: number;
}

const SAMPLE_PRODUCTS = [
  { id: 'WB-001', name: 'Комплект постельного белья хлопок 1,5-спального', price: 2999 },
  { id: 'WB-002', name: 'Евро комплект постельного белья сатин', price: 5999 },
  { id: 'WB-003', name: 'Детское постельное белье с рисунками', price: 1999 },
  { id: 'WB-004', name: 'Полутораспальное белье из бязи', price: 2499 },
  { id: 'WB-005', name: 'Полутораспальное белье из поплина', price: 2799 },
];

export default function PricingPage() {
  const [config, setConfig] = useState<PricingConfig>({
    base_margin_percent: 35.0,
    logistics_cost_percent: 8.0,
    platform_commission_percent: 5.0,
    fixed_costs_rub: 15.0,
    min_markup_percent: 15.0,
  });

  const [prices, setPrices] = useState<ProductPrice[]>([]);
  const [summary, setSummary] = useState<PricingSummary | null>(null);
  const [loading, setLoading] = useState(false);

  const handleConfigChange = (field: keyof PricingConfig, value: number) => {
    setConfig(prev => ({ ...prev, [field]: value }));
  };

  const calculatePrices = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/v1/pricing/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          products: SAMPLE_PRODUCTS.map(p => ({ id: p.id, name: p.name, price: p.price })),
          pricing_config: config,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setPrices(data);

        // Получаем сводку
        const summaryResponse = await fetch('/api/v1/pricing/summary', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            products: SAMPLE_PRODUCTS.map(p => ({ id: p.id, name: p.name, price: p.price })),
            pricing_config: config,
          }),
        });

        if (summaryResponse.ok) {
          const summaryData = await summaryResponse.json();
          setSummary(summaryData);
        }
      }
    } catch (error) {
      console.error('Error calculating prices:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">💰 Smart Pricing Engine</h1>
          <p className="text-slate-400">Управление ценообразованием и маржами</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Configuration Panel */}
          <div className="lg:col-span-1">
            <div className="bg-white/10 backdrop-blur-xl rounded-2xl p-8 border border-white/20 sticky top-6">
              <h2 className="text-2xl font-bold text-white mb-6">⚙️ Конфигурация</h2>

              <div className="space-y-6">
                {/* Base Margin */}
                <div>
                  <label className="block text-sm font-semibold text-slate-300 mb-3">
                    📊 Базовая маржа: {config.base_margin_percent}%
                  </label>
                  <input
                    type="range"
                    min="10"
                    max="100"
                    step="1"
                    value={config.base_margin_percent}
                    onChange={e => handleConfigChange('base_margin_percent', parseFloat(e.target.value))}
                    className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
                  />
                </div>

                {/* Logistics Cost */}
                <div>
                  <label className="block text-sm font-semibold text-slate-300 mb-3">
                    🚚 Логистика: {config.logistics_cost_percent}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="30"
                    step="0.5"
                    value={config.logistics_cost_percent}
                    onChange={e => handleConfigChange('logistics_cost_percent', parseFloat(e.target.value))}
                    className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-green-500"
                  />
                </div>

                {/* Platform Commission */}
                <div>
                  <label className="block text-sm font-semibold text-slate-300 mb-3">
                    🏪 Комиссия маркетплейса: {config.platform_commission_percent}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="20"
                    step="0.5"
                    value={config.platform_commission_percent}
                    onChange={e => handleConfigChange('platform_commission_percent', parseFloat(e.target.value))}
                    className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-yellow-500"
                  />
                </div>

                {/* Fixed Costs */}
                <div>
                  <label className="block text-sm font-semibold text-slate-300 mb-3">
                    💵 Фиксированные расходы: {config.fixed_costs_rub}₽
                  </label>
                  <input
                    type="number"
                    min="0"
                    max="500"
                    step="1"
                    value={config.fixed_costs_rub}
                    onChange={e => handleConfigChange('fixed_costs_rub', parseFloat(e.target.value))}
                    className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                  />
                </div>

                {/* Minimum Markup */}
                <div>
                  <label className="block text-sm font-semibold text-slate-300 mb-3">
                    📈 Минимальная маржа: {config.min_markup_percent}%
                  </label>
                  <input
                    type="range"
                    min="5"
                    max="50"
                    step="1"
                    value={config.min_markup_percent}
                    onChange={e => handleConfigChange('min_markup_percent', parseFloat(e.target.value))}
                    className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
                  />
                </div>

                {/* Calculate Button */}
                <button
                  onClick={calculatePrices}
                  disabled={loading}
                  className="w-full mt-8 px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-lg hover:shadow-lg disabled:opacity-50 transition-all"
                >
                  {loading ? '⏳ Расчет...' : '🧮 Рассчитать цены'}
                </button>
              </div>
            </div>
          </div>

          {/* Results Panel */}
          <div className="lg:col-span-2 space-y-6">
            {/* Summary Stats */}
            {summary && (
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                <div className="bg-blue-500/20 border border-blue-500/50 rounded-xl p-4">
                  <div className="text-sm text-blue-300 mb-1">Товаров</div>
                  <div className="text-2xl font-bold text-blue-100">{summary.total_products}</div>
                </div>
                <div className="bg-green-500/20 border border-green-500/50 rounded-xl p-4">
                  <div className="text-sm text-green-300 mb-1">Сред. маржа</div>
                  <div className="text-2xl font-bold text-green-100">{summary.avg_margin_percent.toFixed(1)}%</div>
                </div>
                <div className="bg-purple-500/20 border border-purple-500/50 rounded-xl p-4">
                  <div className="text-sm text-purple-300 mb-1">Потенциал</div>
                  <div className="text-2xl font-bold text-purple-100">{summary.total_margin_potential.toLocaleString('ru-RU')}₽</div>
                </div>
                <div className="bg-yellow-500/20 border border-yellow-500/50 rounded-xl p-4">
                  <div className="text-sm text-yellow-300 mb-1">Мин цена</div>
                  <div className="text-2xl font-bold text-yellow-100">{summary.min_price.toLocaleString('ru-RU')}₽</div>
                </div>
                <div className="bg-orange-500/20 border border-orange-500/50 rounded-xl p-4">
                  <div className="text-sm text-orange-300 mb-1">Макс цена</div>
                  <div className="text-2xl font-bold text-orange-100">{summary.max_price.toLocaleString('ru-RU')}₽</div>
                </div>
                <div className="bg-indigo-500/20 border border-indigo-500/50 rounded-xl p-4">
                  <div className="text-sm text-indigo-300 mb-1">Сред. розница</div>
                  <div className="text-2xl font-bold text-indigo-100">{summary.avg_retail_price.toLocaleString('ru-RU')}₽</div>
                </div>
              </div>
            )}

            {/* Price Table */}
            {prices.length > 0 && (
              <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 overflow-hidden">
                <div className="px-8 py-6 border-b border-white/20">
                  <h3 className="text-xl font-bold text-white">📋 Рассчитанные цены</h3>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b border-white/20">
                        <th className="px-6 py-4 text-left text-slate-300 font-semibold">Товар</th>
                        <th className="px-6 py-4 text-right text-slate-300 font-semibold">Поставщик</th>
                        <th className="px-6 py-4 text-right text-slate-300 font-semibold">Себестоимость</th>
                        <th className="px-6 py-4 text-right text-slate-300 font-semibold">Розница</th>
                        <th className="px-6 py-4 text-right text-slate-300 font-semibold">Маржа</th>
                      </tr>
                    </thead>
                    <tbody>
                      {prices.map(price => (
                        <tr key={price.product_id} className="border-b border-white/10 hover:bg-white/5 transition">
                          <td className="px-6 py-4 text-slate-200 font-medium">{price.name}</td>
                          <td className="px-6 py-4 text-right text-slate-300">
                            {price.supplier_price.toLocaleString('ru-RU')}₽
                          </td>
                          <td className="px-6 py-4 text-right text-slate-300">
                            {price.cost_price.toLocaleString('ru-RU', { maximumFractionDigits: 0 })}₽
                          </td>
                          <td className="px-6 py-4 text-right text-blue-300 font-semibold">
                            {price.retail_price.toLocaleString('ru-RU')}₽
                          </td>
                          <td className="px-6 py-4 text-right">
                            <span className="bg-green-500/20 text-green-300 px-3 py-1 rounded-full text-xs font-semibold">
                              {price.margin_rub.toLocaleString('ru-RU', { maximumFractionDigits: 0 })}₽ ({price.margin_percent.toFixed(1)}%)
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {prices.length === 0 && (
              <div className="bg-white/5 border border-dashed border-white/20 rounded-2xl p-12 text-center">
                <p className="text-slate-400 text-lg">Нажмите кнопку "Рассчитать цены" чтобы увидеть результаты</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
