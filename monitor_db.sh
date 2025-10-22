#!/bin/bash
# Script đơn giản để xem DB connections và scheduler threads

echo "=== Database & Scheduler Monitor ==="
echo "Timestamp: $(date)"
echo ""

# 1. Xem PgBouncer stats
echo "📊 PgBouncer Stats:"
docker-compose exec pgbouncer psql -h localhost -p 6432 -U postgres -d pgbouncer -c "
SELECT 
    'Client Connections' as metric,
    current_connections as value
FROM pg_stat_pooler;
"

echo ""
echo "📈 Database Connections:"
docker-compose exec stock-predict-postgres psql -U myuser -d stockdb -c "
SELECT 
    COUNT(*) as total_connections,
    COUNT(CASE WHEN state = 'active' THEN 1 END) as active_connections,
    COUNT(CASE WHEN state = 'idle' THEN 1 END) as idle_connections
FROM pg_stat_activity 
WHERE datname = 'stockdb';
"

echo ""
echo "🧵 Scheduler Threads:"
docker-compose exec stock-predict-api python -c "
import threading
print(f'Active Threads: {threading.active_count()}')
print(f'Thread Names: {[t.name for t in threading.enumerate()]}')
"

echo ""
echo "✅ Services Status:"
docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
