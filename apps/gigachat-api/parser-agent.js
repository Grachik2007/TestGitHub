// Parser Agent - автоматическое скачивание и merge товаров с ctradei
// Скачивает: CSV (остатки) + YML (описания) → объединённый YML для insales

const axios = require('axios');
const xml2js = require('xml2js');
const csv = require('csv-parse/sync');
const fs = require('fs');
const path = require('path');

class ParserAgent {
  constructor(ctradeiLogin, ctradeiPassword) {
    this.login = ctradeiLogin;
    this.password = ctradeiPassword;
    this.csvUrl = 'https://ctradei.com/f/ostatki_2020.csv';
    this.ymlUrl = 'https://ctradei.com/x/shop2_1410641-yml.xml';
    this.products = [];
    this.sessionId = null;
  }

  // Скачать файл через HTTP
  async downloadFile(url) {
    try {
      console.log(`📥 Скачиваю файл: ${url}`);
      const response = await axios.get(url, {
        timeout: 30000,
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
      });
      console.log(`✅ Файл скачан успешно`);
      return response.data;
    } catch (error) {
      console.error(`❌ Ошибка скачивания ${url}:`, error.message);
      throw error;
    }
  }

  // Парсить CSV (остатки и цены)
  async parseCSV(csvContent) {
    console.log('📊 Парсю CSV (остатки)...');
    try {
      const records = csv.parse(csvContent, {
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
            cost: parseFloat(record['Цена'] || record['Price'] || record['cost'] || 0),
            quantity: parseInt(record['Остаток'] || record['Stock'] || record['quantity'] || 0),
            barcode: record['Артикул'] || record['SKU'] || record['barcode'] || '',
            vendorCode: record['Код производителя'] || record['vendor_code'] || ''
          };
        }
      });

      console.log(`✅ Распарсено товаров из CSV: ${Object.keys(products).length}`);
      return products;
    } catch (error) {
      console.error('❌ Ошибка парсинга CSV:', error.message);
      throw error;
    }
  }

  // Парсить YML (описания товаров)
  async parseYML(ymlContent) {
    console.log('📦 Парсю YML (описания)...');
    try {
      const parser = new xml2js.Parser({
        mergeAttrs: true,
        explicitArray: false
      });

      const result = await parser.parseStringPromise(ymlContent);

      // Найти офферы в YML структуре
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

      console.log(`✅ Распарсено товаров из YML: ${Object.keys(products).length}`);
      return products;
    } catch (error) {
      console.error('❌ Ошибка парсинга YML:', error.message);
      throw error;
    }
  }

  // Объединить товары из двух файлов
  mergeProducts(csvProducts, ymlProducts) {
    console.log('🔗 Объединяю товары...');

    const merged = {};

    // Сначала добавляем все товары из YML
    Object.values(ymlProducts).forEach(product => {
      merged[product.id] = { ...product };
    });

    // Затем добавляем/обновляем данные из CSV
    Object.entries(csvProducts).forEach(([id, csvData]) => {
      if (merged[id]) {
        // Товар существует - добавляем данные о цене и остатке
        merged[id].cost = csvData.cost;
        merged[id].quantity = csvData.quantity;
        merged[id].barcode = csvData.barcode || merged[id].barcode;
        merged[id].vendorCode = csvData.vendorCode || merged[id].vendorCode;
      } else {
        // Товара нет в YML - добавляем из CSV
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

    console.log(`✅ Объединено товаров: ${Object.keys(merged).length}`);
    return Object.values(merged);
  }

  // Главный метод - скачать, распарсить, merge
  async sync() {
    try {
      console.log('\n🚀 НАЧИНАЮ СИНХРОНИЗАЦИЮ С CTRADEI\n');

      // Скачиваем оба файла
      const csvContent = await this.downloadFile(this.csvUrl);
      const ymlContent = await this.downloadFile(this.ymlUrl);

      // Парсим файлы
      const csvProducts = await this.parseCSV(csvContent);
      const ymlProducts = await this.parseYML(ymlContent);

      // Объединяем
      this.products = this.mergeProducts(csvProducts, ymlProducts);

      console.log(`\n✅ СИНХРОНИЗАЦИЯ ЗАВЕРШЕНА!`);
      console.log(`📊 Всего товаров: ${this.products.length}`);

      return this.products;
    } catch (error) {
      console.error('\n❌ ОШИБКА СИНХРОНИЗАЦИИ:', error.message);
      throw error;
    }
  }

  // Получить товары
  getProducts() {
    return this.products;
  }

  // Получить статистику
  getStats() {
    const totalCost = this.products.reduce((sum, p) => sum + (p.cost || 0), 0);
    const totalQuantity = this.products.reduce((sum, p) => sum + (p.quantity || 0), 0);

    return {
      productsCount: this.products.length,
      totalInventoryValue: totalCost,
      totalQuantity: totalQuantity,
      avgPrice: Math.round(totalCost / this.products.length),
      lastUpdated: new Date().toISOString()
    };
  }
}

module.exports = ParserAgent;
