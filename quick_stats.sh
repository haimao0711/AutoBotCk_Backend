#!/bin/bash
# Script nhanh để xem stats

echo "🔍 Quick Stats Check"
echo "==================="

# PgBouncer connections
echo "PgBouncer Connections:"
docker-compose exec pgbouncer psql -h localhost -p 6432 -U postgres -d pgbouncer -c "SELECT current_connections FROM pg_stat_pooler;" 2>/dev/null || echo "PgBouncer not accessible"

# Database connections
echo "PostgreSQL Connections:"
docker-compose exec stock-predict-postgres psql -U myuser -d stockdb -c "SELECT COUNT(*) as total FROM pg_stat_activity WHERE datname = 'stockdb';" 2>/dev/null || echo "PostgreSQL not accessible"

# Scheduler threads
echo "Scheduler Threads:"
docker-compose exec stock-predict-api python -c "import threading; print(f'Active: {threading.active_count()}')" 2>/dev/null || echo "API not accessible"

echo "==================="
