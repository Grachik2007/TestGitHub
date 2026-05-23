@echo off
REM 🚀 AI Business SaaS Agents Platform - Quick Start (Windows)

echo 🚀 AI Business SaaS Agents Platform - Quick Start
echo ==================================================
echo.

REM Check Docker
docker --version > nul 2>&1
if errorlevel 1 (
    echo ⚠️  Docker не установлен!
    echo Установите Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✓ Docker найден
echo.

REM Check Docker Compose
docker-compose --version > nul 2>&1
if errorlevel 1 (
    echo ⚠️  Docker Compose не установлен!
    pause
    exit /b 1
)

echo ✓ Docker Compose найден
echo.

REM Step 1: Create .env
echo 1️⃣  Создание .env файла...
if not exist ".env" (
    copy .env.example .env
    echo ✅ .env создан
) else (
    echo ⚠️  .env уже существует
)
echo.

REM Step 2: Build images
echo 2️⃣  Сборка Docker образов...
docker-compose build --quiet
echo ✅ Образы собраны
echo.

REM Step 3: Start services
echo 3️⃣  Запуск сервисов...
docker-compose up -d
echo ✅ Сервисы запущены
echo.

REM Step 4: Wait for services
echo 4️⃣  Ожидание инициализации (30 сек)...
timeout /t 30 /nobreak
echo ✅ Сервисы готовы
echo.

REM Step 5: Database migrations
echo 5️⃣  Применение миграций БД...
docker-compose exec -T api alembic upgrade head 2>nul
echo ✅ Миграции применены
echo.

REM Done
echo ==================================================
echo ✅ ПРОЕКТ ГОТОВ!
echo ==================================================
echo.
echo 🌐 Доступные сервисы:
echo.
echo 📊 Dashboard (Web):
echo    http://localhost:3000
echo.
echo ⚙️  API (REST):
echo    http://localhost:8000
echo.
echo 📋 API Docs (Swagger):
echo    http://localhost:8000/api/docs
echo.
echo 📚 API Docs (ReDoc):
echo    http://localhost:8000/docs
echo.
echo 🔐 Demo Credentials:
echo    Email: demo@example.com
echo    Password: demo123456
echo.
echo 📖 Документация:
echo    - FINAL_GUIDE.md - Финальный гайд
echo    - README.md - Основная документация
echo    - ARCHITECTURE.md - Архитектура
echo.
echo 🛑 Остановить сервисы:
echo    docker-compose down
echo.
echo 📋 Смотреть логи:
echo    docker-compose logs -f api
echo.
echo ==================================================
echo Приятного использования! 🎉
echo ==================================================
echo.
pause
