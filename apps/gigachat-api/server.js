const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

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

  pricing: `Ты эксперт по ценообразованию и оптимизации маржи. Помогай:
- Рассчитывать оптимальные цены
- Анализировать конкурентов
- Оптимизировать маржу и прибыль
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

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`✅ AI Assistant API running on port ${PORT}`);
  console.log(`🔌 Endpoint: POST /api/chat`);
});
