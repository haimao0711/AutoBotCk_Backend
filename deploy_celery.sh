#!/bin/bash
set -e

echo "🚀 Starting Celery Migration Deployment..."

# 1. Pull latest code
echo "📥 Pulling latest code..."
git pull origin dev

# 2. Stop existing services
echo "⏹️ Stopping existing services..."
docker-compose down || true

# 3. Build new images
echo "🔨 Building new images..."
docker-compose build --no-cache

# 4. Start services
echo "🚀 Starting services..."
docker-compose up -d

# 5. Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# 6. Run migrations
echo "📊 Running migrations..."
docker-compose exec stock-predict-api python manage.py migrate

# 7. Run Celery migration
echo "🔄 Migrating to Celery..."
docker-compose exec stock-predict-api python manage.py migrate_to_celery

# 8. Check service status
echo "✅ Checking service status..."
docker-compose ps

echo "🎉 Deployment completed successfully!"
echo "📊 Monitor at: http://your-vps-ip:5555 (Flower UI)"
echo "🔧 API available at: http://your-vps-ip:8000"
