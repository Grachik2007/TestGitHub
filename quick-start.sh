#!/bin/bash

# 🚀 AI Business SaaS Agents Platform - Quick Start
# Этот скрипт настраивает проект за несколько секунд

set -e

echo "🚀 AI Business SaaS Agents Platform - Quick Start"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker не установлен!${NC}"
    echo "Установите Docker с: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo -e "${BLUE}✓ Docker найден${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker Compose не установлен!${NC}"
    exit 1
fi

echo -e "${BLUE}✓ Docker Compose найден${NC}"
echo ""

# Step 1: Create .env
echo -e "${BLUE}1️⃣  Создание .env файла...${NC}"
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ .env создан${NC}"
else
    echo -e "${YELLOW}⚠️  .env уже существует${NC}"
fi
echo ""

# Step 2: Build images
echo -e "${BLUE}2️⃣  Сборка Docker образов...${NC}"
docker-compose build --quiet
echo -e "${GREEN}✅ Образы собраны${NC}"
echo ""

# Step 3: Start services
echo -e "${BLUE}3️⃣  Запуск сервисов...${NC}"
docker-compose up -d
echo -e "${GREEN}✅ Сервисы запущены${NC}"
echo ""

# Step 4: Wait for services
echo -e "${BLUE}4️⃣  Ожидание инициализации (30 сек)...${NC}"
sleep 30
echo -e "${GREEN}✅ Сервисы готовы${NC}"
echo ""

# Step 5: Database migrations
echo -e "${BLUE}5️⃣  Применение миграций БД...${NC}"
docker-compose exec -T api alembic upgrade head || true
echo -e "${GREEN}✅ Миграции применены${NC}"
echo ""

# Done
echo "=================================================="
echo -e "${GREEN}✅ ПРОЕКТ ГОТОВ!${NC}"
echo "=================================================="
echo ""
echo "🌐 Доступные сервисы:"
echo ""
echo -e "${BLUE}📊 Dashboard (Web):${NC}"
echo "   http://localhost:3000"
echo ""
echo -e "${BLUE}⚙️  API (REST):${NC}"
echo "   http://localhost:8000"
echo ""
echo -e "${BLUE}📋 API Docs (Swagger):${NC}"
echo "   http://localhost:8000/api/docs"
echo ""
echo -e "${BLUE}📚 API Docs (ReDoc):${NC}"
echo "   http://localhost:8000/docs"
echo ""
echo "🔐 Demo Credentials:"
echo "   Email: demo@example.com"
echo "   Password: demo123456"
echo ""
echo "📖 Документация:"
echo "   - FINAL_GUIDE.md - Финальный гайд"
echo "   - README.md - Основная документация"
echo "   - ARCHITECTURE.md - Архитектура"
echo ""
echo "🛑 Остановить сервисы:"
echo "   docker-compose down"
echo ""
echo "📋 Смотреть логи:"
echo "   docker-compose logs -f api"
echo ""
echo "=================================================="
echo -e "${GREEN}Приятного использования! 🎉${NC}"
echo "=================================================="
