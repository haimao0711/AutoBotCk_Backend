#!/bin/sh
# Redis entrypoint script to ensure master mode
set -e

# Start Redis in background
redis-server /usr/local/etc/redis/redis.conf --daemonize yes

# Wait for Redis to be ready
sleep 2

# Force Redis to be master (remove any replica configuration)
redis-cli REPLICAOF NO ONE || true

# Save configuration to disk to persist the change
redis-cli CONFIG REWRITE || true

# Shutdown Redis gracefully
redis-cli SHUTDOWN NOSAVE || true

# Start Redis in foreground (main process)
exec redis-server /usr/local/etc/redis/redis.conf

