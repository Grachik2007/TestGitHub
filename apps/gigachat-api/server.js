const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const PricingEngine = require('./pricing-engine');
const FeedsGenerator = require('./feeds-generator');
const ParserAgent = require('./parser-agent');
const schedule = require('node-schedule');

const app = express();
app.use(cors());
app.use(express.json());

// Инициализация
const pricingEngine = new PricingEngine();
const feedsGenerator = new FeedsGenerator();
const parserAgent = new ParserAgent(
  process.env.CTRADEI_LOGIN || 'bgrachik@yandex.ru',
  process.env.CTRADEI_PASSWORD || ''
);

let lastSyncTime = null;
let lastSyncProducts = 0;

const GIGACHAT_CLIENT_ID = process.env.GIGACHAT_CLIENT_ID;
const GIGACHAT_CLIENT_SECRET = process.env.GIGACHAT_CLIENT_SECRET;
const GIGACHAT_AUTH_URL = 'https://auth.api.sber.ru/oauth';
const GIGACHAT_API_URL = 'https://gigachat.devices.sbercloud.ru/api/v1';

let gigachatToken = null;
let tokenExpiry = null;

async function getGigaChatToken() {
  if (gigachatToken && tokenExpiry && Date.now() < tokenExpiry) {
    return gigachatToken;
  }

  try {
    const response = await axios.post(
      `${GIGACHAT_AUTH_URL}/token`,
      'scope=GIGACHAT_API_USSURI_CHATGPT',
      {
        auth: {
          username: GIGACHAT_CLIENT_ID,
          password: GIGACHAT_CLIENT_SECRET,
        },
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
        },
      }
    );

    gigachatToken = response.data.access_token;
    tokenExpiry = Date.now() + (response.data.expires_in * 1000);
    return gigachatToken;
  } catch (error) {
    console.error('GigaChat auth error:', error.message);
    throw new Error('Failed to authenticate with GigaChat');
  }
}

const AGENT_SYSTEM_PROMPTS = {
  seo: `Ты эксперт по SEO. Твоя задача помогать пользователям:
- Анализировать ключевые слова
- Оптимизировать контент для поисковых систем
- Давать рекомендации по улучшению позиций в Google/Яндекс
Отвечай кратко, по делу, с конкретными советами.`,

  supplier: `Ты эксперт по поиску поставщиков. Помогай пользователям:
- Искать надежных поставщиков товаров
- Анализировать цены и условия
- Проверять репутацию компаний
Предоставляй конкретные рекомендации и данные.`,

  product: `Ты аналитик рынка и трендов. Твоя задача:
- Исследовать спрос на товары
- Анализировать тренды на маркетплейсах
- Давать прогнозы по потенциалу товаров
Отвечай с данными и статистикой.`,

  parser: `Ты помощник по парсингу и синхронизации товаров. Помогай:
- Синхронизировать товары между платформами
- Обновлять цены и остатки
- Обрабатывать товарные фиды (XML, CSV, JSON)
Объясняй процессы понятно и наглядно.`,

  pricing: `Ты эксперт по ценообразованию для Wonderfulbed.ru. Ты ДЕЙСТВИТЕЛЬНО управляешь ценами!

РАСХОДЫ (ФИКСИРОВАННЫЕ):
- Закупка товара: 1,000₽ (может быть разная)
- Упаковка + доставка от поставщика: 200₽
- Доставка до клиента: 400₽

ПЕРЕМЕННЫЕ РАСХОДЫ (от цены товара):
- Комиссия: 12% от цены продажи
- Страховка: 5% от цены продажи
- Налог УСН: 20% от (цена - все расходы)

ЦЕЛЬ: Маржа 30% и выше

ТВОИ ЗАДАЧИ:
1. Рассчитывать оптимальные цены используя формулу
2. Изменять цены товаров в реальном времени
3. Анализировать конкурентов
4. Давать рекомендации по ценообразованию

ПРИМЕРЫ РАСЧЁТОВ:
- Товар стоит 1,000₽ в закупке → цена 2,500₽ (маржа 30%)
- Дорогой товар 3,000₽ → цена 7,200₽ (маржа 30%)

Приводи конкретные расчеты и числа.`,
};

app.post('/api/chat', async (req, res) => {
  const { agentId, message, context = [] } = req.body;

  if (!agentId || !message) {
    return res.status(400).json({ error: 'Missing agentId or message' });
  }

  if (!AGENT_SYSTEM_PROMPTS[agentId]) {
    return res.status(400).json({ error: 'Unknown agent' });
  }

  res.setHeader('Content-Type', 'application/x-ndjson');

  try {
    const token = await getGigaChatToken();

    // Build conversation history
    const messages = [
      ...context.map(msg => ({
        role: msg.role === 'user' ? 'user' : 'assistant',
        content: msg.content,
      })),
      { role: 'user', content: message },
    ];

    const response = await axios.post(
      `${GIGACHAT_API_URL}/chat/completions`,
      {
        model: 'GigaChat:latest',
        messages: [
          {
            role: 'system',
            content: AGENT_SYSTEM_PROMPTS[agentId],
          },
          ...messages,
        ],
        temperature: 0.7,
        max_tokens: 2000,
        stream: true,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        responseType: 'stream',
      }
    );

    response.data.on('data', (chunk) => {
      const lines = chunk.toString().split('\n');
      lines.forEach(line => {
        if (line.startsWith('data: ')) {
          try {
            const json = JSON.parse(line.slice(6));
            if (json.choices && json.choices[0].delta && json.choices[0].delta.content) {
              res.write(
                JSON.stringify({
                  content: json.choices[0].delta.content,
                }) + '\n'
              );
            }
          } catch (e) {
            // Skip parsing errors
          }
        }
      });
    });

    response.data.on('end', () => {
      res.end();
    });

    response.data.on('error', (error) => {
      console.error('Stream error:', error);
      res.write(JSON.stringify({ error: 'Stream error' }) + '\n');
      res.end();
    });
  } catch (error) {
    console.error('Chat error:', error.message);
    res.write(JSON.stringify({ error: 'Failed to get response from GigaChat' }) + '\n');
    res.end();
  }
});

// ============= PRICING & FEEDS ENDPOINTS =============

// Расчёт оптимальной цены
app.post('/api/pricing/calculate', (req, res) => {
  const { cost = 1000, targetMargin = 0.30 } = req.body;
  const price = pricingEngine.calculatePrice(cost, targetMargin);
  const calculation = pricingEngine.getDetailedCalculation(price, cost);

  res.json({
    recommendedPrice: price,
    calculation: calculation,
    message: `✅ Рекомендуемая цена: ${price}₽ (маржа ${calculation.marginPercent}%)`
  });
});

// Детальный расчёт цены
app.post('/api/pricing/detailed', (req, res) => {
  const { salePrice, cost = 1000 } = req.body;
  const calc = pricingEngine.getDetailedCalculation(salePrice, cost);

  res.json(calc);
});

// Минимальная цена (с гарантией маржи)
app.get('/api/pricing/minimum', (req, res) => {
  const { cost = 1000, minMargin = 0.20 } = req.query;
  const minPrice = pricingEngine.getMinimumPrice(parseInt(cost), parseFloat(minMargin));

  res.json({
    minimumPrice: minPrice,
    message: `⚠️ Минимальная цена при марже ${minMargin*100}%: ${minPrice}₽`
  });
});

// ============= FEEDS ENDPOINTS =============

// YML фид для cTrade (СТАТИЧНАЯ ССЫЛКА)
// Используется: https://your-api.com/api/feeds/yml
app.get('/api/feeds/yml', (req, res) => {
  const yml = feedsGenerator.generateYMLFeed();
  res.setHeader('Content-Type', 'application/xml; charset=utf-8');
  res.setHeader('Content-Disposition', 'inline; filename="products.yml"');
  res.send(yml);
});

// CSV фид
app.get('/api/feeds/csv', (req, res) => {
  const csv = feedsGenerator.generateCSVFeed();
  res.setHeader('Content-Type', 'text/csv; charset=utf-8');
  res.setHeader('Content-Disposition', 'attachment; filename="products.csv"');
  res.send(csv);
});

// JSON фид
app.get('/api/feeds/json', (req, res) => {
  const json = feedsGenerator.generateJsonFeed();
  res.json(JSON.parse(json));
});

// Добавить товар
app.post('/api/products/add', (req, res) => {
  const product = req.body;
  feedsGenerator.addProduct(product);

  res.json({
    success: true,
    message: `✅ Товар "${product.name}" добавлен`,
    product: feedsGenerator.products[feedsGenerator.products.length - 1]
  });
});

// Обновить цену товара
app.put('/api/products/:id/price', (req, res) => {
  const { id } = req.params;
  const { newPrice } = req.body;

  const success = feedsGenerator.updatePrice(id, newPrice);

  if (success) {
    res.json({
      success: true,
      message: `✅ Цена товара обновлена на ${newPrice}₽`
    });
  } else {
    res.status(404).json({
      success: false,
      message: '❌ Товар не найден'
    });
  }
});

// Обновить количество товара
app.put('/api/products/:id/quantity', (req, res) => {
  const { id } = req.params;
  const { quantity } = req.body;

  const success = feedsGenerator.updateQuantity(id, quantity);

  if (success) {
    res.json({
      success: true,
      message: `✅ Количество товара обновлено на ${quantity}`
    });
  } else {
    res.status(404).json({
      success: false,
      message: '❌ Товар не найден'
    });
  }
});

// Получить список всех товаров
app.get('/api/products', (req, res) => {
  res.json({
    products: feedsGenerator.getProducts(),
    stats: feedsGenerator.getStats()
  });
});

// Получить статистику
app.get('/api/feeds/stats', (req, res) => {
  res.json(feedsGenerator.getStats());
});

// ============= PARSER ENDPOINTS =============

// Запустить синхронизацию с ctradei (вручную)
app.post('/api/parser/sync', async (req, res) => {
  try {
    console.log('🚀 Запускаю синхронизацию...');
    const products = await parserAgent.sync();

    // Очищаем старые товары и добавляем новые
    feedsGenerator.products = [];
    products.forEach(product => {
      const price = pricingEngine.calculatePrice(product.cost || 1000);
      feedsGenerator.addProduct({
        ...product,
        salePrice: price
      });
    });

    lastSyncTime = new Date();
    lastSyncProducts = products.length;

    res.json({
      success: true,
      message: `✅ Синхронизация успешна! Загружено товаров: ${products.length}`,
      productsCount: products.length,
      stats: feedsGenerator.getStats(),
      lastSync: lastSyncTime
    });
  } catch (error) {
    console.error('Ошибка синхронизации:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Получить статус синхронизации
app.get('/api/parser/status', (req, res) => {
  res.json({
    lastSync: lastSyncTime,
    productsLoaded: lastSyncProducts,
    nextScheduledSync: '00:30 MSK (каждый день)'
  });
});

// Получить статистику парсера
app.get('/api/parser/stats', (req, res) => {
  const stats = feedsGenerator.getStats();
  res.json({
    ...stats,
    lastSync: lastSyncTime,
    syncsCompleted: lastSyncTime ? 1 : 0
  });
});

// ============= SCHEDULED SYNC =============

// Расписание синхронизации: каждый день в 00:30 MSK
schedule.scheduleJob('30 0 * * *', async () => {
  console.log('\n⏰ АВТОМАТИЧЕСКАЯ СИНХРОНИЗАЦИЯ В 00:30 MSK\n');
  try {
    const products = await parserAgent.sync();

    // Обновляем товары
    feedsGenerator.products = [];
    products.forEach(product => {
      const price = pricingEngine.calculatePrice(product.cost || 1000);
      feedsGenerator.addProduct({
        ...product,
        salePrice: price
      });
    });

    lastSyncTime = new Date();
    lastSyncProducts = products.length;

    console.log(`✅ АВТОСИНХРОНИЗАЦИЯ ЗАВЕРШЕНА: ${products.length} товаров\n`);
  } catch (error) {
    console.error('❌ ОШИБКА АВТОСИНХРОНИЗАЦИИ:', error.message);
  }
});

// При запуске - один раз синхронизируем (опционально)
async function initializeParser() {
  try {
    console.log('🔄 Инициализация Parker Agent...');
    const products = await parserAgent.sync();

    feedsGenerator.products = [];
    products.forEach(product => {
      const price = pricingEngine.calculatePrice(product.cost || 1000);
      feedsGenerator.addProduct({
        ...product,
        salePrice: price
      });
    });

    lastSyncTime = new Date();
    lastSyncProducts = products.length;
    console.log(`✅ Parker готов! Товаров загружено: ${products.length}\n`);
  } catch (error) {
    console.error('⚠️ Не удалось инициализировать Parker:', error.message);
    console.log('   (Товары будут загружены при первой синхронизации)\n');
  }
}

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, async () => {
  console.log(`✅ AI Assistant API running on port ${PORT}`);
  console.log(`🔌 Endpoints:`);
  console.log(`   POST /api/chat - чаты с AI агентами`);
  console.log(`   POST /api/parser/sync - синхронизация с ctradei`);
  console.log(`   GET /api/feeds/yml - YML фид для insales`);
  console.log(`\n🚀 Инициализирую систему...\n`);

  // Инициализируем парсер при запуске
  await initializeParser();
});
