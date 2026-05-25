// Генератор товарных фидов для cTrade и других платформ
// Статичная ссылка которая всегда актуальна

const PricingEngine = require('./pricing-engine');

class FeedsGenerator {
  constructor() {
    this.pricingEngine = new PricingEngine();
    // Вот здесь будут храниться ваши товары из базы
    this.products = [];
  }

  // Добавить товар в каталог
  addProduct(product) {
    const priceCalc = this.pricingEngine.getDetailedCalculation(
      this.pricingEngine.calculatePrice(product.cost || 1000),
      product.cost || 1000
    );

    this.products.push({
      id: product.id || Date.now(),
      name: product.name,
      description: product.description || '',
      categoryId: product.categoryId || '1',
      cost: product.cost || 1000,
      salePrice: priceCalc.salePrice,
      oldPrice: product.oldPrice,
      quantity: product.quantity || 0,
      url: product.url || '',
      imageUrl: product.imageUrl || '',
      barcode: product.barcode || '',
      updatedAt: new Date().toISOString()
    });
  }

  // Обновить цену товара (AI агент это делает)
  updatePrice(productId, newPrice) {
    const product = this.products.find(p => p.id === productId);
    if (product) {
      product.oldPrice = product.salePrice;
      product.salePrice = newPrice;
      product.updatedAt = new Date().toISOString();
      return true;
    }
    return false;
  }

  // Обновить кол-во товара
  updateQuantity(productId, quantity) {
    const product = this.products.find(p => p.id === productId);
    if (product) {
      product.quantity = quantity;
      product.updatedAt = new Date().toISOString();
      return true;
    }
    return false;
  }

  // *** ГЕНЕРАТОР YML ФИДА для cTrade ***
  generateYMLFeed(shopName = 'Wonderfulbed') {
    const timestamp = new Date().toISOString();

    let yml = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE yml_catalog SYSTEM "shops.dtd">
<yml_catalog date="${timestamp}">
  <shop>
    <name>${shopName}</name>
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

    // Добавляем товары
    this.products.forEach(product => {
      yml += `      <offer id="${product.id}">
        <name>${this.escapeXml(product.name)}</name>
        <description>${this.escapeXml(product.description)}</description>
        <url>${product.url}</url>
        <price>${product.salePrice}</price>
        <currencyId>RUR</currencyId>
        <categoryId>${product.categoryId}</categoryId>
        <picture>${product.imageUrl}</picture>
        <barcode>${product.barcode}</barcode>
        <quantity>${product.quantity}</quantity>
        <oldprice>${product.oldPrice || product.salePrice}</oldprice>
        <updatedDate>${product.updatedAt}</updatedDate>
      </offer>
`;
    });

    yml += `    </offers>
  </shop>
</yml_catalog>`;

    return yml;
  }

  // *** ГЕНЕРАТОР CSV ФИДА ***
  generateCSVFeed() {
    let csv = 'ID,Название,Описание,Цена,Старая цена,Кол-во,URL,Артикул,Дата обновления\n';

    this.products.forEach(product => {
      csv += `"${product.id}","${this.escapeCsv(product.name)}","${this.escapeCsv(product.description)}",${product.salePrice},${product.oldPrice || product.salePrice},${product.quantity},"${product.url}","${product.barcode}","${product.updatedAt}"\n`;
    });

    return csv;
  }

  // *** ГЕНЕРАТОР JSON ФИДА ***
  generateJsonFeed() {
    return JSON.stringify({
      timestamp: new Date().toISOString(),
      shop: 'Wonderfulbed.ru',
      productsCount: this.products.length,
      products: this.products
    }, null, 2);
  }

  // Безопасность: экранирование XML
  escapeXml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&apos;');
  }

  // Безопасность: экранирование CSV
  escapeCsv(str) {
    if (!str) return '';
    if (str.includes(',') || str.includes('"') || str.includes('\n')) {
      return '"' + str.replace(/"/g, '""') + '"';
    }
    return str;
  }

  // Получить все товары
  getProducts() {
    return this.products;
  }

  // Статистика
  getStats() {
    const totalPrice = this.products.reduce((sum, p) => sum + p.salePrice, 0);
    const totalQuantity = this.products.reduce((sum, p) => sum + p.quantity, 0);

    return {
      productsCount: this.products.length,
      totalInventoryValue: totalPrice,
      totalQuantity: totalQuantity,
      avgPrice: Math.round(totalPrice / this.products.length),
      lastUpdated: this.products.length > 0 ? this.products[0].updatedAt : null
    };
  }
}

module.exports = FeedsGenerator;
