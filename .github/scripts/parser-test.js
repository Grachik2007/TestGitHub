#!/usr/bin/env node

/**
 * Parser Agent Test Mode - локальные тестовые данные
 * Используется для разработки и тестирования логики
 */

const fs = require('fs');
const path = require('path');
const xml2js = require('xml2js');
const csv = require('csv-parse/sync');

const OUTPUT_DIR = 'feeds';

// Load pricing configuration from JSON
let PRICING;
try {
  const pricingConfigPath = path.join(__dirname, '../../config/pricing.json');
  const configData = JSON.parse(fs.readFileSync(pricingConfigPath, 'utf-8'));
  PRICING = {
    WHOLESALE_COST: configData.costs.defaultWholesaleCost,
    PACKAGING: configData.costs.packaging,
    ASSEMBLY: configData.costs.assembly,
    COMMISSION_RATE: configData.commissions.acquiring,
    MARKETING_RATE: configData.expenses.marketing,
    TAX_RATE: configData.expenses.tax,
    TARGET_MARGIN: configData.margin.target
  };
  console.log('✅ Загружена конфигурация ценообразования из config/pricing.json');
} catch (error) {
  console.warn('⚠️  Ошибка загрузки конфига ценообразования, используем значения по умолчанию');
  PRICING = {
    WHOLESALE_COST: 1000,
    PACKAGING: 250,
    ASSEMBLY: 100,
    COMMISSION_RATE: 0.055,
    MARKETING_RATE: 0.05,
    TAX_RATE: 0.20,
    TARGET_MARGIN: 0.30
  };
}

if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

console.log('\n🚀 === ТЕСТИРОВАНИЕ СИНХРОНИЗАЦИИ (LOCAL DATA) ===\n');
console.log(`⏰ Время: ${new Date().toISOString()}`);
console.log(`📁 Выходная директория: ${OUTPUT_DIR}\n`);

async function parseCSV(content) {
  console.log('\n📊 Парсю CSV (остатки и цены)...');
  try {
    const records = csv.parse(content, {
      columns: true,
      skip_empty_lines: true,
      delimiter: ',',
      encoding: 'utf-8'
    });

    const products = {};
    records.forEach(record => {
      const productId = record['ID'] || record['id'] || record['Товар ID'];
      if (productId) {
        products[productId] = {
          id: productId,
          cost: parseFloat(record['Цена'] || record['Price'] || record['cost'] || 1000),
          quantity: parseInt(record['Остаток'] || record['Stock'] || record['quantity'] || 0),
          barcode: record['Артикул'] || record['SKU'] || record['barcode'] || '',
          vendorCode: record['Код производителя'] || record['vendor_code'] || ''
        };
      }
    });

    console.log(`✅ Распарсено товаров: ${Object.keys(products).length}`);
    return products;
  } catch (error) {
    console.error(`❌ Ошибка парсинга CSV: ${error.message}`);
    throw error;
  }
}

async function parseYML(content) {
  console.log('\n📦 Парсю YML (описания товаров)...');
  try {
    const parser = new xml2js.Parser({
      mergeAttrs: true,
      explicitArray: false
    });

    const result = await parser.parseStringPromise(content);

    let offers = [];
    if (result.yml_catalog?.shop?.offers?.offer) {
      offers = Array.isArray(result.yml_catalog.shop.offers.offer)
        ? result.yml_catalog.shop.offers.offer
        : [result.yml_catalog.shop.offers.offer];
    }

    const products = {};
    offers.forEach(offer => {
      const productId = offer.id || offer.ID;
      if (productId) {
        products[productId] = {
          id: productId,
          name: offer.name || offer.title || '',
          description: offer.description || offer.desc || '',
          category: offer.categoryId || offer.category_id || '1',
          imageUrl: Array.isArray(offer.picture) ? offer.picture[0] : offer.picture || '',
          url: offer.url || '',
          manufacturer: offer.manufacturer || ''
        };
      }
    });

    console.log(`✅ Распарсено товаров: ${Object.keys(products).length}`);
    return products;
  } catch (error) {
    console.error(`❌ Ошибка парсинга YML: ${error.message}`);
    throw error;
  }
}

function mergeProducts(csvProducts, ymlProducts) {
  console.log('\n🔗 Объединяю товары...');

  const merged = {};

  Object.values(ymlProducts).forEach(product => {
    merged[product.id] = { ...product };
  });

  Object.entries(csvProducts).forEach(([id, csvData]) => {
    if (merged[id]) {
      merged[id].cost = csvData.cost;
      merged[id].quantity = csvData.quantity;
      merged[id].barcode = csvData.barcode || merged[id].barcode;
      merged[id].vendorCode = csvData.vendorCode || merged[id].vendorCode;
    } else {
      merged[id] = {
        id,
        name: `Товар ${id}`,
        description: '',
        category: '1',
        cost: csvData.cost,
        quantity: csvData.quantity,
        barcode: csvData.barcode,
        vendorCode: csvData.vendorCode
      };
    }
  });

  console.log(`✅ Всего объединено товаров: ${Object.keys(merged).length}`);
  return Object.values(merged);
}

function calculatePrice(cost = PRICING.WHOLESALE_COST) {
  const fixedCosts = cost + PRICING.PACKAGING + PRICING.ASSEMBLY;
  const variableRatio = PRICING.COMMISSION_RATE + PRICING.MARKETING_RATE +
                        (PRICING.TAX_RATE * (1 - PRICING.TARGET_MARGIN));
  return Math.round(fixedCosts / (1 - variableRatio));
}

function applySmartPricing(products) {
  console.log('\n💰 Применяю Smart Pricing (маржа 30%)...');

  products.forEach(product => {
    product.salePrice = calculatePrice(product.cost || PRICING.WHOLESALE_COST);
    product.updatedAt = new Date().toISOString();
  });

  console.log(`✅ Цены применены всем товарам`);
  return products;
}

function generateYML(products, shopName = 'Wonderfulbed') {
  console.log('\n📄 Генерирую YML...');

  const timestamp = new Date().toISOString();
  let yml = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE yml_catalog SYSTEM "shops.dtd">
<yml_catalog date="${timestamp}">
  <shop>
    <name>${escapeXml(shopName)}</name>
    <company>Wonderfulbed.ru</company>
    <url>https://wonderfulbed.ru</url>
    <currencies>
      <currency id="RUR" rate="1"/>
    </currencies>
    <categories>
      <category id="1">Товары</category>
    </categories>
    <offers>
`;

  products.forEach(product => {
    yml += `      <offer id="${product.id}">
        <name>${escapeXml(product.name)}</name>
        <description>${escapeXml(product.description)}</description>
        <url>${product.url || '#'}</url>
        <price>${product.salePrice}</price>
        <currencyId>RUR</currencyId>
        <categoryId>${product.category}</categoryId>
        <picture>${product.imageUrl || ''}</picture>
        <barcode>${product.barcode || ''}</barcode>
        <quantity>${product.quantity || 0}</quantity>
        <oldprice>${product.salePrice}</oldprice>
        <updatedDate>${product.updatedAt}</updatedDate>
      </offer>
`;
  });

  yml += `    </offers>
  </shop>
</yml_catalog>`;

  return yml;
}

function generateCSV(products) {
  console.log('\n📊 Генерирую CSV...');

  let csvContent = 'ID,Название,Описание,Цена,Остаток,Артикул,Изображение,URL,Категория,Дата обновления\n';

  products.forEach(product => {
    csvContent += `"${product.id}","${escapeCsv(product.name)}","${escapeCsv(product.description)}",${product.salePrice},${product.quantity || 0},"${product.barcode || ''}","${product.imageUrl || ''}","${product.url || ''}","${product.category || '1'}","${product.updatedAt}"\n`;
  });

  return csvContent;
}

function escapeXml(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function escapeCsv(str) {
  if (!str) return '';
  if (str.includes(',') || str.includes('"') || str.includes('\n')) {
    return '"' + str.replace(/"/g, '""') + '"';
  }
  return str;
}

async function main() {
  try {
    const csvPath = path.join('.github/test-data', 'sample.csv');
    const ymlPath = path.join('.github/test-data', 'sample.xml');

    const csvContent = fs.readFileSync(csvPath, 'utf-8');
    const ymlContent = fs.readFileSync(ymlPath, 'utf-8');

    const csvProducts = await parseCSV(csvContent);
    const ymlProducts = await parseYML(ymlContent);

    let products = mergeProducts(csvProducts, ymlProducts);
    products = applySmartPricing(products);

    const ymlOutput = generateYML(products);
    const csvOutput = generateCSV(products);

    fs.writeFileSync(path.join(OUTPUT_DIR, 'products.yml'), ymlOutput, 'utf-8');
    fs.writeFileSync(path.join(OUTPUT_DIR, 'products.csv'), csvOutput, 'utf-8');

    const summary = {
      timestamp: new Date().toISOString(),
      productsCount: products.length,
      stats: {
        totalInventoryValue: products.reduce((sum, p) => sum + (p.cost || 0), 0),
        totalQuantity: products.reduce((sum, p) => sum + (p.quantity || 0), 0),
        avgPrice: Math.round(products.reduce((sum, p) => sum + (p.salePrice || 0), 0) / products.length)
      },
      links: {
        yml: 'https://grachik2007.github.io/TestGitHub/products.yml',
        csv: 'https://grachik2007.github.io/TestGitHub/products.csv'
      }
    };

    fs.writeFileSync(path.join(OUTPUT_DIR, 'summary.json'), JSON.stringify(summary, null, 2), 'utf-8');

    console.log('\n' + '='.repeat(60));
    console.log('✅ === СИНХРОНИЗАЦИЯ УСПЕШНА! ===');
    console.log('='.repeat(60));
    console.log(`\n📊 Статистика:`);
    console.log(`   Товаров: ${products.length}`);
    console.log(`   Стоимость инвентаря: ${summary.stats.totalInventoryValue.toLocaleString()}₽`);
    console.log(`   Средняя цена: ${summary.stats.avgPrice}₽`);
    console.log(`\n🔗 Ссылки:`);
    console.log(`   YML: ${summary.links.yml}`);
    console.log(`   CSV: ${summary.links.csv}`);
    console.log(`\n⏰ Время синхронизации: ${new Date().toISOString()}`);
    console.log('\n');

  } catch (error) {
    console.error('\n' + '='.repeat(60));
    console.error('❌ === ОШИБКА СИНХРОНИЗАЦИИ ===');
    console.error('='.repeat(60));
    console.error(`\nОшибка: ${error.message}`);
    console.error(`\n⏰ Время ошибки: ${new Date().toISOString()}`);
    console.error('\n');
    process.exit(1);
  }
}

main();
