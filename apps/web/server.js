const express = require('express');
const next = require('next');
const path = require('path');
const fs = require('fs');

const dev = process.env.NODE_ENV !== 'production';
const app = next({ dev });
const handle = app.getRequestHandler();

const AGENTS_DATA = {
  seo: {
    id: 'seo',
    name: '🔍 SEO Agent',
    type: 'seo',
    description: 'Анализ ключевых слов и оптимизация контента',
    status: 'active',
    tasks: 1234,
    successRate: 98.5,
    created_at: '2024-01-01T00:00:00Z',
  },
  supplier: {
    id: 'supplier',
    name: '🏭 Supplier Agent',
    type: 'supplier',
    description: 'Поиск и анализ поставщиков',
    status: 'active',
    tasks: 567,
    successRate: 95.2,
    created_at: '2024-01-01T00:00:00Z',
  },
  product: {
    id: 'product',
    name: '📦 Product Agent',
    type: 'product',
    description: 'Исследование трендов и товаров',
    status: 'active',
    tasks: 892,
    successRate: 96.8,
    created_at: '2024-01-01T00:00:00Z',
  },
  parser: {
    id: 'parser',
    name: '🛒 Wonderfulbed Parser',
    type: 'parser',
    description: 'Парсинг товаров с ctradei для wonderfulbed.ru',
    status: 'active',
    tasks: 45,
    successRate: 99.1,
    created_at: '2024-01-01T00:00:00Z',
  },
  pricing: {
    id: 'pricing',
    name: '💰 Pricing Agent',
    type: 'pricing',
    description: 'Оптимизация цен и анализ конкурентов',
    status: 'idle',
    tasks: 234,
    successRate: 94.7,
    created_at: '2024-01-01T00:00:00Z',
  },
};

async function generateAgentResponse(agentId, message) {
  const agent = AGENTS_DATA[agentId];
  if (!agent) {
    return [{ error: 'Agent not found' }];
  }

  const responses = {
    seo: [
      `Анализирую ваш запрос '${message}' с точки зрения SEO... `,
      'Ключевые слова: найдено 15 релевантных терминов ',
      'Рекомендация 1: Оптимизация заголовков H1 ',
      'Рекомендация 2: Увеличение внутренних ссылок ',
      'Рекомендация 3: Улучшение скорости загрузки страницы',
    ],
    supplier: [
      `Ищу поставщиков для '${message}'... `,
      'Найдено 12 потенциальных поставщиков ',
      "Топ 1: ООО 'ТрейдПро' - цена $45, количество 1000 шт ",
      "Топ 2: ИП 'Логистик+' - цена $38, количество 5000 шт ",
      "Топ 3: Компания 'БизнесПлюс' - цена $42, количество 2000 шт",
    ],
    product: [
      `Исследую тренды для '${message}'... `,
      'Текущий спрос: высокий (↑ 23% за неделю) ',
      'Конкурентность: средняя (15 основных конкурентов) ',
      'Рекомендуемая цена: $45-55 ',
      'Прогноз: спрос будет расти в течение 3 месяцев',
    ],
    parser: [
      `Парсю товары по запросу '${message}'... `,
      'Найдено 342 товара в ctradei ',
      'Обновляю цены и остатки... ',
      'Синхронизирую с wonderfulbed.ru... ',
      '✅ Синхронизация завершена успешно. Обновлено 342 товара',
    ],
    pricing: [
      `Оптимизирую цены для '${message}'... `,
      'Анализирую конкурентов... ',
      'Базовая цена: $100 ',
      'После расчета маржи и расходов: $156.50 ',
      'Рекомендация: установить цену $155 для конкурентности',
    ],
  };

  return responses[agentId] || [
    `Обработка запроса '${message}'...`,
    'Анализ завершен',
    '✅ Готово',
  ];
}

app.prepare().then(() => {
  const server = express();

  server.use(express.json());

  // API Routes
  server.get('/api/v1/agents', (req, res) => {
    res.json(Object.values(AGENTS_DATA));
  });

  server.get('/api/v1/agents/:agentId', (req, res) => {
    const agent = AGENTS_DATA[req.params.agentId];
    if (!agent) {
      return res.status(404).json({ error: 'Agent not found' });
    }
    res.json(agent);
  });

  server.post('/api/v1/agents/:agentId/chat', async (req, res) => {
    const agent = AGENTS_DATA[req.params.agentId];
    if (!agent) {
      return res.status(404).json({ error: 'Agent not found' });
    }

    const { message } = req.body;
    const responses = await generateAgentResponse(req.params.agentId, message);

    res.setHeader('Content-Type', 'application/x-ndjson');

    for (const line of responses) {
      res.write(JSON.stringify({ content: line }) + '\n');
    }

    res.end();
  });

  server.get('/api/v1/agents/:agentId/tasks', (req, res) => {
    const agent = AGENTS_DATA[req.params.agentId];
    if (!agent) {
      return res.status(404).json({ error: 'Agent not found' });
    }

    const tasks = [
      {
        task_id: 'task-1',
        agent_id: req.params.agentId,
        status: 'completed',
        result: { response: 'Task result 1' },
      },
      {
        task_id: 'task-2',
        agent_id: req.params.agentId,
        status: 'completed',
        result: { response: 'Task result 2' },
      },
      {
        task_id: 'task-3',
        agent_id: req.params.agentId,
        status: 'completed',
        result: { response: 'Task result 3' },
      },
    ];

    res.json(tasks);
  });

  server.post('/api/v1/agents/:agentId/execute', (req, res) => {
    const agent = AGENTS_DATA[req.params.agentId];
    if (!agent) {
      return res.status(404).json({ error: 'Agent not found' });
    }

    res.json({
      task_id: `task-${Date.now()}`,
      agent_id: req.params.agentId,
      status: 'completed',
      result: { response: 'Task executed successfully' },
    });
  });

  // Health checks
  server.get('/health', (req, res) => {
    res.json({ status: 'ok' });
  });

  server.get('/ready', (req, res) => {
    res.json({ status: 'ready' });
  });

  // Serve Next.js pages
  server.all('*', (req, res) => {
    return handle(req, res);
  });

  const PORT = process.env.PORT || 3000;
  server.listen(PORT, (err) => {
    if (err) throw err;
    console.log(`✅ Server ready on http://localhost:${PORT}`);
    console.log(`🔌 API: http://localhost:${PORT}/api/v1/agents`);
    console.log(`🌐 Frontend: http://localhost:${PORT}`);
  });
});
