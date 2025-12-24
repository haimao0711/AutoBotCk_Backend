#!/bin/sh
# Redis entrypoint script to ensure master mode
set -e

# Start Redis in background
redis-server /usr/local/etc/redis/redis.conf --daemonize yes

# Wait for Redis to be ready
sleep 2

# Force Redis to be master (remove any replica configuration)
redis-cli REPLICAOF NO ONE || true

# Verify Redis is in master mode
ROLE=$(redis-cli INFO replication | grep "role:" | cut -d: -f2 | tr -d '\r\n ')
if [ "$ROLE" != "master" ]; then
    echo "WARNING: Redis is not in master mode, forcing master mode..."
    redis-cli REPLICAOF NO ONE
    sleep 1
fi

# Save configuration to disk to persist the change
redis-cli CONFIG REWRITE || true

# Shutdown Redis gracefully
redis-cli SHUTDOWN NOSAVE || true

# Start Redis in foreground (main process)
exec redis-server /usr/local/etc/redis/redis.conf

