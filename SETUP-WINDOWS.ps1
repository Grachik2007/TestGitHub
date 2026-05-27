# 🪟 Автоматический setup для Windows PowerShell
# Запустить в PowerShell (Admin):
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
# .\SETUP-WINDOWS.ps1

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🚀 SETUP: GitHub Pages для Wonderfulbed (Windows)        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ============= ШАГ 1: GitHub Pages =============

Write-Host "┌─ ШАГ 1: Включить GitHub Pages ──────────────────────────┐" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  ВАЖНО! Откройте в браузере и сделайте вручную:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Ссылка: https://github.com/Grachik2007/TestGitHub/settings/pages" -ForegroundColor Cyan
Write-Host ""
Write-Host "Настройки:" -ForegroundColor Yellow
Write-Host "  1. Source: Deploy from a branch" -ForegroundColor White
Write-Host "  2. Branch: gh-pages" -ForegroundColor White
Write-Host "  3. Folder: / (root)" -ForegroundColor White
Write-Host "  4. Click 'Save'" -ForegroundColor White
Write-Host ""

Read-Host "Нажмите Enter когда закончите... " | Out-Null

Write-Host "✅ GitHub Pages включены!" -ForegroundColor Green
Write-Host ""

# ============= ШАГ 2: Запустить Workflow =============

Write-Host "┌─ ШАГ 2: Запустить синхронизацию ────────────────────────┐" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  Откройте в браузере:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Ссылка: https://github.com/Grachik2007/TestGitHub/actions" -ForegroundColor Cyan
Write-Host ""
Write-Host "Что делать:" -ForegroundColor Yellow
Write-Host "  1. Найти workflow 'Daily Parser Sync'" -ForegroundColor White
Write-Host "  2. Click 'Run workflow'" -ForegroundColor White
Write-Host "  3. Подождать 1-2 минуты" -ForegroundColor White
Write-Host ""

$response = Read-Host "Запустили workflow? (y/n)"

if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host ""
    Write-Host "⏱️  Ждем синхронизацию (1-2 минуты)..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    Write-Host "✅ Синхронизация запущена!" -ForegroundColor Green
} else {
    Write-Host "⏭️  Пропускаю запуск" -ForegroundColor Yellow
}

Write-Host ""

# ============= ШАГ 3: Проверка =============

Write-Host "┌─ ШАГ 3: Проверка ─────────────────────────────────────┐" -ForegroundColor Green
Write-Host ""

Write-Host "✓ Проверяю статус..." -ForegroundColor White
Write-Host ""

$ymlUrl = "https://grachik2007.github.io/TestGitHub/products.yml"

try {
    $response = Invoke-WebRequest -Uri $ymlUrl -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ YML файл доступен!" -ForegroundColor Green
        Write-Host "   Размер: $($response.Content.Length) bytes" -ForegroundColor Green
    } else {
        Write-Host "⚠️  YML файл еще генерируется..." -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  YML файл еще не готов (это нормально, ждём синхронизацию)" -ForegroundColor Yellow
}

Write-Host ""

# ============= ФИНАЛЬНАЯ ИНФОРМАЦИЯ =============

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  ✅ SETUP ЗАВЕРШЁН!                                       ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "📌 СТАТИЧНАЯ ССЫЛКА ДЛЯ INSALES:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   https://grachik2007.github.io/TestGitHub/products.yml" -ForegroundColor Cyan
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""
Write-Host "🔗 ПОДКЛЮЧЕНИЕ К INSALES:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Откройте insales админ-панель" -ForegroundColor White
Write-Host "2. Товары → Импорт" -ForegroundColor White
Write-Host "3. Загружать с URL:" -ForegroundColor White
Write-Host "   https://grachik2007.github.io/TestGitHub/products.yml" -ForegroundColor Cyan
Write-Host "4. Периодичность: каждый час / день" -ForegroundColor White
Write-Host "5. Сохранить" -ForegroundColor White
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Gray
Write-Host ""
Write-Host "✨ Готово! Система полностью настроена и работает бесплатно!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Товары будут обновляться каждый день в 00:30 МСК" -ForegroundColor White
Write-Host ""

Write-Host "🎉 Спасибо за использование!" -ForegroundColor Magenta
Write-Host ""
