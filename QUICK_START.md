# ⚡ QUICK START - 3 МИНУТЫ ДО РАБОТАЮЩЕЙ СИСТЕМЫ

## **Вариант 1: Автоматический Setup (рекомендуется)**

```bash
chmod +x SETUP.sh
./SETUP.sh
```

Скрипт сделает всё автоматически (нужен GitHub CLI).

---

## **Вариант 2: Ручной Setup**

### **Шаг 1️⃣: Добавить GitHub Secrets (1 минута)**

Откройте: https://github.com/Grachik2007/TestGitHub/settings/secrets/actions

**Создайте 2 secret:**

**Secret #1: CTRADEI_LOGIN**
- Name: `CTRADEI_LOGIN`
- Value: `bgrachik@yandex.ru`
- Click "Add secret"

**Secret #2: CTRADEI_PASSWORD**
- Name: `CTRADEI_PASSWORD`
- Value: `89682753114Grach`
- Click "Add secret"

✅ Готово!

---

### **Шаг 2️⃣: Включить GitHub Pages (1 минута)**

Откройте: https://github.com/Grachik2007/TestGitHub/settings/pages

**Настройки:**
1. **Source:** Deploy from a branch
2. **Branch:** `gh-pages`
3. **Folder:** `/ (root)`
4. Click "Save"

✅ Готово! Через минуту будет доступна страница.

---

### **Шаг 3️⃣: Запустить первую синхронизацию (1 минута)**

Откройте: https://github.com/Grachik2007/TestGitHub/actions

1. Найти workflow: **"Daily Parser Sync"**
2. Click "Run workflow"
3. Подождать 1-2 минуты

✅ Готово! Товары загружены!

---

## **🔗 ССЫЛКИ ДЛЯ INSALES (после синхронизации)**

Скопируйте эту ссылку в insales:

```
https://grachik2007.github.io/TestGitHub/products.yml
```

### **В insales админ-панели:**

1. Товары → Импорт
2. Загружать с URL:
   ```
   https://grachik2007.github.io/TestGitHub/products.yml
   ```
3. Периодичность: **каждый час** (или день)
4. Сохранить

✅ Готово! insales теперь автоматически получает товары!

---

## **✨ ВСЁ РАБОТАЕТ!**

```
✅ Каждый день в 00:30 MSK:
   - Скачиваются файлы с ctradei
   - Merge и Smart Pricing
   - Публикация на GitHub Pages
   - insales получает обновления

✅ Полностью бесплатно
✅ Никаких платежей
✅ Никаких серверов
```

---

## **📊 МОНИТОРИНГ**

**Проверить статус:**
https://github.com/Grachik2007/TestGitHub/actions/workflows/parser-sync.yml

**Просмотреть логи:**
1. Actions → Daily Parser Sync
2. Кликнуть на последний run
3. Посмотреть все логи

---

## **❓ ПРОБЛЕМЫ?**

**Q: Workflow не запускается?**
- Проверьте что secrets добавлены (Settings → Secrets)
- Проверьте что gh-pages ветка существует

**Q: GitHub Pages не работает?**
- Подождите 1-2 минуты после включения
- Проверьте ссылку: https://grachik2007.github.io/TestGitHub/products.yml

**Q: insales не видит товары?**
- Убедитесь что синхронизация прошла (Actions → ✅ green)
- Проверьте что URL скопирован правильно
- Попробуйте импортировать вручную

---

## **✅ ЧЕКЛИСТ**

- [ ] Secrets добавлены (Settings → Secrets)
- [ ] GitHub Pages включены (Settings → Pages)
- [ ] Первая синхронизация запущена (Actions)
- [ ] YML ссылка скопирована в insales
- [ ] insales видит товары

---

**🎉 Готово! Система полностью настроена и работает!**

Товары будут обновляться автоматически каждый день в 00:30 МСК.
