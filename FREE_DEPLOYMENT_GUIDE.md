# 🆓 Бесплатное развёртывание с GitHub Actions

**Полностью бесплатное решение** - ничего платить не нужно!

---

## **🎯 Как это работает:**

```
GitHub Actions (бесплатно!)
    ↓ Каждый день в 00:30 MSK
    ↓
Скачивает файлы с ctradei
    ↓
Merge по product_id + Smart Pricing
    ↓
Публикует YML в GitHub Pages (бесплатно)
    ↓
insales берёт файл оттуда
```

---

## **⚡ БЫСТРЫЙ СТАРТ (3 шага)**

### **Шаг 1: Добавить secrets в GitHub**

1. Перейти на https://github.com/Grachik2007/TestGitHub
2. Settings → Secrets and variables → Actions
3. Создать два secret:
   - `CTRADEI_LOGIN` = `bgrachik@yandex.ru`
   - `CTRADEI_PASSWORD` = `89682753114Grach`

### **Шаг 2: Включить GitHub Pages**

1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages`
4. Folder: `/ (root)`
5. Save

### **Шаг 3: Подключить в insales**

Скопировать ссылку YML фида:
```
https://grachik2007.github.io/TestGitHub/products.yml
```

В insales:
- Товары → Импорт
- Загружать с URL: вставить ссылку выше
- Периодичность: каждый час / день

---

## **🔄 Как работает автоматизация:**

### **Расписание:**
- **Автоматическая синхронизация:** каждый день в 00:30 МСК
- **Ручная синхронизация:** Actions → Daily Parser → Run workflow

### **Что происходит:**

1. **Скачивание** (30 сек):
   - CSV: https://ctradei.com/f/ostatki_2020.csv (остатки)
   - YML: https://ctradei.com/x/shop2_1410641-yml.xml (описания)

2. **Merge** (15 сек):
   - Объединяет по product_id
   - Полные данные товара

3. **Smart Pricing** (10 сек):
   - Считает оптимальную цену
   - Применяет 30% маржу
   - Учитывает все расходы

4. **Публикация** (20 сек):
   - Генерирует YML
   - Генерирует CSV
   - Публикует на GitHub Pages

**Всё занимает < 2 минут!**

---

## **📊 Статистика**

После синхронизации доступна статистика:
- Количество товаров
- Стоимость инвентаря
- Средняя цена

---

## **🔗 СТАТИЧНЫЕ ССЫЛКИ ДЛЯ INSALES:**

```
YML для insales (обновляется автоматически):
https://grachik2007.github.io/TestGitHub/products.yml

CSV резервная копия:
https://grachik2007.github.io/TestGitHub/products.csv

JSON статистика:
https://grachik2007.github.io/TestGitHub/summary.json
```

---

## **⚙️ ПАРАМЕТРЫ ЦЕНООБРАЗОВАНИЯ**

Все расчёты в файле `.github/scripts/parser.js`:

```javascript
PRICING = {
  WHOLESALE_COST: 1000,           // Закупка
  PACKAGING_DELIVERY_IN: 200,      // Упаковка + доставка от поставщика
  DELIVERY_OUT: 400,               // Доставка до клиента
  COMMISSION_RATE: 0.12,           // Комиссия 12%
  INSURANCE_RATE: 0.05,            // Страховка 5%
  TAX_RATE: 0.20,                  // УСН 20%
  TARGET_MARGIN: 0.30              // Целевая маржа 30%
}
```

Если нужно изменить - отредактируйте файл `.github/scripts/parser.js`

---

## **🔍 МОНИТОРИНГ**

### **Проверить статус синхронизации:**

1. Перейти на https://github.com/Grachik2007/TestGitHub
2. Actions → Daily Parser Sync
3. Посмотреть последний run:
   - ✅ Green = успешно
   - ❌ Red = ошибка

### **Посмотреть логи:**

1. Actions → Daily Parser Sync
2. Кликнуть на последний workflow
3. Все логи с информацией о товарах

---

## **❓ FAQ**

**Q: Что если синхронизация не сработала?**
A: GitHub Actions имеет временные перебои. Можно запустить вручную:
   - Actions → Daily Parser → Run workflow

**Q: Как изменить время синхронизации?**
A: Отредактировать `.github/workflows/parser-sync.yml`, строка:
   ```yaml
   - cron: '30 21 * * *'  # 00:30 MSK
   ```

**Q: Как добавить новые товары?**
A: Они загружаются автоматически из ctradei. После синхронизации они появятся в YML.

**Q: Сколько это стоит?**
A: **Совершенно бесплатно!**
   - GitHub Actions: 2000 минут/месяц бесплатно
   - GitHub Pages: неограниченно бесплатно
   - Никаких платежей

---

## **✅ ЧЕКЛИСТ ГОТОВНОСТИ**

- [ ] Добавлены secrets (CTRADEI_LOGIN, CTRADEI_PASSWORD)
- [ ] Включены GitHub Pages
- [ ] Ссылка YML скопирована в insales
- [ ] Первая синхронизация прошла успешно
- [ ] insales видит товары с корректными ценами
- [ ] Автоматическое обновление работает

---

**Готово!** 🎉 Система полностью бесплатна и автоматизирована!
