# 🚀 Гайд развёртывания AI Backend для Wonderfulbed

## **Выбранная платформа: Railway.app**
- ✅ Полностью бесплатная ($5/месяц)
- ✅ Node.js 20 поддержка
- ✅ Автоматический деплой из GitHub
- ✅ Никогда не спит (в отличие от Render.com)

---

## **БЫСТРЫЙ СТАРТ (5 минут)**

### **1️⃣ Перейти на Railway.app**
https://railway.app/

### **2️⃣ Создать новый проект**
- Нажать "Start a New Project"
- Выбрать "Deploy from GitHub repo"
- Авторизоваться через GitHub

### **3️⃣ Выбрать репозиторий**
- Выбрать: `Grachik2007/TestGitHub`
- Ветка: `claude/ai-saas-agents-platform-bIaAc`

### **4️⃣ Добавить переменные окружения**

В Railway нажать "Variables" и добавить:

```
GIGACHAT_CLIENT_ID = [ваш client id от GigaChat]
GIGACHAT_CLIENT_SECRET = [ваш secret от GigaChat]
NODE_ENV = production
PORT = 5000
```

### **5️⃣ Указать директорию**

В настройках Service:
```
Root Directory: apps/gigachat-api
```

Или через `Procfile` в корне `apps/gigachat-api/`:
```
web: node server.js
```

### **6️⃣ Деплой**

Railway автоматически:
- ✅ Установит npm зависимости
- ✅ Запустит `npm start`
- ✅ Даст вам URL типа: `https://wonderfulbed-api-production.up.railway.app`

---

## **📌 ВАША СТАТИЧНАЯ YML ССЫЛКА:**

После деплоя ваша ссылка будет:

```
https://[ваш-домен-railway].up.railway.app/api/feeds/yml
```

**Пример:**
```
https://wonderfulbed-api-production.up.railway.app/api/feeds/yml
```

---

## **🔌 ПОДКЛЮЧЕНИЕ К INSALES**

После развёртывания у вас будет несколько способов:

### **Вариант 1: Прямая интеграция через Albato**
- Используйте Albato для синхронизации с insales
- Источник: Ваша YML ссылка
- Цель: insales

### **Вариант 2: Импорт в insales вручную**
В insales → Товары → Импорт:
- Загрузить YML с вашей ссылки: `/api/feeds/yml`
- Указать период обновления (каждый час)

### **Вариант 3: Webhook интеграция (продвинутая)**
- insales отправляет заказы на ваш сервер
- AI обновляет цены и товары в реальном времени

---

## **🧪 ПРОВЕРКА РАБОТОСПОСОБНОСТИ**

После развёртывания проверьте эндпоинты:

```bash
# Проверка здоровья
curl https://[ваш-домен]/health
→ {"status":"ok"}

# Получить YML фид
curl https://[ваш-домен]/api/feeds/yml
→ XML с товарами

# Расчёт цены
curl -X POST https://[ваш-домен]/api/pricing/calculate \
  -H "Content-Type: application/json" \
  -d '{"cost":1000,"targetMargin":0.30}'
→ {"recommendedPrice":2500, ...}
```

---

## **💾 ОБНОВЛЕНИЕ ТОВАРОВ**

### **Добавить товар:**
```bash
curl -X POST https://[ваш-домен]/api/products/add \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "name": "Кровать King",
    "description": "Красивая кровать",
    "cost": 1000,
    "quantity": 50
  }'
```

### **Изменить цену:**
```bash
curl -X PUT https://[ваш-домен]/api/products/1/price \
  -H "Content-Type: application/json" \
  -d '{"newPrice": 2800}'
```

### **Обновить остатки:**
```bash
curl -X PUT https://[ваш-домен]/api/products/1/quantity \
  -H "Content-Type: application/json" \
  -d '{"quantity": 35}'
```

---

## **⚙️ АЛЬТЕРНАТИВНЫЕ ПЛАТФОРМЫ**

Если Railway не подходит:

| Платформа | Бесплатный тариф | Минус |
|-----------|-----------------|-------|
| **Railway** | $5/месяц | ✅ РЕКОМЕНДУЕМ |
| Fly.io | Да | Спит после бездействия |
| Render.com | 0.1 compute unit | Спит после 15 мин бездействия |
| Heroku | Закрыл бесплатный | ❌ |
| Replit | Да | Медленнее |

---

## **🎯 ПОСЛЕ РАЗВЁРТЫВАНИЯ**

1. ✅ Скопируйте свою URL
2. ✅ Добавьте товары через API
3. ✅ Подключите YML фид в insales или Albato
4. ✅ Готово! Агенты будут управлять ценами автоматически

---

## **📞 ПОДДЕРЖКА**

Если что-то не работает:
- Проверьте переменные окружения (GIGACHAT_CLIENT_ID, SECRET)
- Посмотрите логи в Railway Dashboard
- Убедитесь что ветка `claude/ai-saas-agents-platform-bIaAc` свежая

---

**Готовы к развёртыванию? 🚀**

Дайте знать когда развернули, и я помогу с подключением к insales!
