#!/bin/bash

set -e

echo "🚀 Setting up AI Agents Platform..."

# Check prerequisites
command -v docker &> /dev/null || { echo "Docker is required"; exit 1; }
command -v docker-compose &> /dev/null || { echo "Docker Compose is required"; exit 1; }

# Copy environment files if they don't exist
if [ ! -f .env ]; then
    echo "📋 Creating .env from template..."
    cp .env.example .env
fi

if [ ! -f apps/api/.env ]; then
    echo "📋 Creating apps/api/.env from template..."
    cp apps/api/.env.example apps/api/.env
fi

if [ ! -f apps/web/.env.local ]; then
    echo "📋 Creating apps/web/.env.local from template..."
    cp apps/web/.env.example apps/web/.env.local
fi

if [ ! -f apps/telegram/.env ]; then
    echo "📋 Creating apps/telegram/.env from template..."
    cp apps/telegram/.env.example apps/telegram/.env
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env files with your configuration"
echo "2. Run: docker-compose up -d"
echo "3. Visit: http://localhost:3000"
