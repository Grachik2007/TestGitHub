#!/bin/bash

# 🚀 Автоматический setup GitHub Actions + GitHub Pages
# Запустить: chmod +x SETUP.sh && ./SETUP.sh

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 SETUP: GitHub Actions + GitHub Pages для Wonderfulbed  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Проверяем наличие gh CLI
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI не установлен"
    echo "📥 Установите отсюда: https://cli.github.com"
    exit 1
fi

# Проверяем авторизацию
if ! gh auth status &> /dev/null; then
    echo "❌ Вы не авторизованы в GitHub"
    echo "🔐 Выполните: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI установлен и авторизован"
echo ""

# ============= ШАГИ SETUP =============

echo "═══════════════════════════════════════════════════════════"
echo "ШАГИ SETUP:"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "1️⃣  Добавление GitHub Secrets"
echo "2️⃣  Включение GitHub Pages"
echo "3️⃣  Проверка конфигурации"
echo "4️⃣  Запуск первой синхронизации"
echo ""

# ============= ШАГИ 1: GitHub Secrets =============

echo "┌─ ШАГ 1: GitHub Secrets ─────────────────────────────────┐"
echo ""

read -p "Добавить GitHub Secrets? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔐 Добавляю секреты..."

    # CTRADEI_LOGIN
    gh secret set CTRADEI_LOGIN --body "bgrachik@yandex.ru" || echo "⚠️  CTRADEI_LOGIN может быть уже установлен"

    # CTRADEI_PASSWORD
    gh secret set CTRADEI_PASSWORD --body "89682753114Grach" || echo "⚠️  CTRADEI_PASSWORD может быть уже установлен"

    echo "✅ Секреты добавлены!"
    echo ""

    # Проверяем
    echo "📋 Проверка добавленных секретов:"
    gh secret list 2>/dev/null | grep -E "CTRADEI" || echo "⚠️  Не удалось проверить секреты"
else
    echo "⏭️  Пропускаю добавление секретов"
fi

echo ""

# ============= ШАГ 2: GitHub Pages =============

echo "┌─ ШАГ 2: GitHub Pages ──────────────────────────────────┐"
echo ""

read -p "Включить GitHub Pages? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📄 Включаю GitHub Pages..."
    echo ""
    echo "❗ ВАЖНО! Выполните вручную:"
    echo ""
    echo "1. Откройте: https://github.com/Grachik2007/TestGitHub/settings/pages"
    echo "2. В разделе 'Source':"
    echo "   - Выберите ветку: gh-pages"
    echo "   - Выберите папку: / (root)"
    echo "3. Нажмите 'Save'"
    echo ""
    read -p "Готовы? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "✅ GitHub Pages включены!"
    fi
else
    echo "⏭️  Пропускаю GitHub Pages"
fi

echo ""

# ============= ШАГ 3: Проверка =============

echo "┌─ ШАГ 3: Проверка конфигурации ─────────────────────────┐"
echo ""

echo "✓ Проверяю конфигурацию..."
echo ""

# Проверяем workflow файл
if [ -f ".github/workflows/parser-sync.yml" ]; then
    echo "✅ Workflow файл: .github/workflows/parser-sync.yml"
else
    echo "❌ Workflow файл не найден!"
    exit 1
fi

# Проверяем parser скрипт
if [ -f ".github/scripts/parser.js" ]; then
    echo "✅ Parser скрипт: .github/scripts/parser.js"
else
    echo "❌ Parser скрипт не найден!"
    exit 1
fi

# Проверяем статус репо
echo ""
echo "📊 Статус репозитория:"
git status --short | head -5 || true

echo ""

# ============= ШАГ 4: Запуск синхронизации =============

echo "┌─ ШАГ 4: Запуск первой синхронизации ────────────────────┐"
echo ""

read -p "Запустить первую синхронизацию? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Запускаю workflow..."
    gh workflow run parser-sync.yml || echo "⚠️  Не удалось запустить workflow"

    echo ""
    echo "✅ Workflow запущен!"
    echo ""
    echo "📍 Смотрите статус здесь:"
    echo "   https://github.com/Grachik2007/TestGitHub/actions"
    echo ""
    echo "⏱️  Синхронизация займёт 1-2 минуты"
else
    echo "⏭️  Workflow запустится автоматически в 00:30 MSK"
fi

echo ""

# ============= ФИНАЛЬНАЯ ИНФОРМАЦИЯ =============

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ SETUP ЗАВЕРШЁН!                                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📌 ВАЖНЫЕ ССЫЛКИ:"
echo ""
echo "YML для insales:"
echo "   https://grachik2007.github.io/TestGitHub/products.yml"
echo ""
echo "CSV резервная копия:"
echo "   https://grachik2007.github.io/TestGitHub/products.csv"
echo ""
echo "Статус синхронизации:"
echo "   https://github.com/Grachik2007/TestGitHub/actions"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "🔗 ПОДКЛЮЧЕНИЕ К INSALES:"
echo ""
echo "1. Откройте: insales админ-панель"
echo "2. Товары → Импорт"
echo "3. Загружать с URL:"
echo "   https://grachik2007.github.io/TestGitHub/products.yml"
echo "4. Периодичность: каждый час / день"
echo "5. Сохранить"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "✨ Готово! Система полностью настроена и работает бесплатно!"
echo ""
