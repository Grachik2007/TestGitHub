#!/bin/bash

set -e

echo "🚀 Deploying AI Agents Platform..."

ENVIRONMENT=${1:-production}
echo "Environment: $ENVIRONMENT"

# Build Docker images
echo "🔨 Building Docker images..."
docker-compose build

# Start services
echo "🟢 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check health
echo "🏥 Checking health..."
curl -f http://localhost:8000/health || {
    echo "❌ API health check failed"
    docker-compose logs api
    exit 1
}

echo "✅ Deployment complete!"
echo ""
echo "Services:"
echo "- API: http://localhost:8000"
echo "- Web: http://localhost:3000"
echo "- Nginx: http://localhost"
