#!/usr/bin/env node

/**
 * Pricing Management API
 * Позволяет управлять параметрами ценообразования через HTTP API
 * Можно вызывать из Telegram бота или веб-интерфейса
 */

const express = require('express');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const app = express();
const PORT = process.env.PORT || 3001;
const PRICING_CONFIG = path.join(__dirname, 'config/pricing.json');

app.use(express.json());

// GET /api/v1/pricing - получить текущую конфигурацию
app.get('/api/v1/pricing', (req, res) => {
  try {
    const config = JSON.parse(fs.readFileSync(PRICING_CONFIG, 'utf-8'));
    res.json({
      success: true,
      data: config
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// POST /api/v1/pricing - обновить конфигурацию
app.post('/api/v1/pricing', (req, res) => {
  try {
    const { costs, commissions, expenses, margin } = req.body;
    const config = JSON.parse(fs.readFileSync(PRICING_CONFIG, 'utf-8'));

    if (costs) {
      Object.assign(config.costs, costs);
    }
    if (commissions) {
      Object.assign(config.commissions, commissions);
    }
    if (expenses) {
      Object.assign(config.expenses, expenses);
    }
    if (margin) {
      Object.assign(config.margin, margin);
    }

    config.metadata.lastUpdated = new Date().toISOString();
    fs.writeFileSync(PRICING_CONFIG, JSON.stringify(config, null, 2));

    res.json({
      success: true,
      message: 'Конфигурация обновлена',
      data: config
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      error: error.message
    });
  }
});

// POST /api/v1/pricing/recalculate - пересчитать цены и обновить feeds
app.post('/api/v1/pricing/recalculate', (req, res) => {
  try {
    console.log('🔄 Запущена пересчет цен...');

    // Запустить parser-test.js для пересчета
    execSync('node .github/scripts/parser-test.js', {
      stdio: 'inherit',
      cwd: __dirname
    });

    res.json({
      success: true,
      message: 'Цены пересчитаны и feeds обновлены',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Примеры использования из Telegram бота:
app.get('/api/v1/pricing/examples', (req, res) => {
  res.json({
    getCurrentPricing: {
      method: 'GET',
      url: '/api/v1/pricing'
    },
    updatePackaging: {
      method: 'POST',
      url: '/api/v1/pricing',
      body: {
        costs: {
          packaging: 300
        }
      }
    },
    updateMargin: {
      method: 'POST',
      url: '/api/v1/pricing',
      body: {
        margin: {
          target: 0.35
        }
      }
    },
    updateCommission: {
      method: 'POST',
      url: '/api/v1/pricing',
      body: {
        commissions: {
          acquiring: 0.04
        }
      }
    },
    recalculatePrices: {
      method: 'POST',
      url: '/api/v1/pricing/recalculate'
    }
  });
});

app.listen(PORT, () => {
  console.log(`\n💰 === PRICING API ЗАПУЩЕНА ===`);
  console.log(`🌐 http://localhost:${PORT}/api/v1/pricing`);
  console.log(`\n📚 Примеры использования:`);
  console.log(`   GET    ${PORT}/api/v1/pricing`);
  console.log(`   POST   ${PORT}/api/v1/pricing`);
  console.log(`   POST   ${PORT}/api/v1/pricing/recalculate`);
  console.log(`   GET    ${PORT}/api/v1/pricing/examples\n`);
});
