#!/bin/sh
# Celery worker entrypoint - Ensure Redis is ready and in master mode
set -e

REDIS_HOST="${REDIS_HOST:-redis}"
REDIS_PORT="${REDIS_PORT:-6379}"
MAX_RETRIES=30
RETRY_COUNT=0

echo "Waiting for Redis to be ready and in master mode..."

# Use Python to check Redis (more reliable than redis-cli which may not be installed)
python3 << EOF
import sys
import socket
import time

redis_host = "${REDIS_HOST}"
redis_port = int("${REDIS_PORT}")
max_retries = ${MAX_RETRIES}

for i in range(max_retries):
    try:
        # Check if Redis is responding
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((redis_host, redis_port))
        sock.close()
        
        if result == 0:
            # Try to connect with redis-py if available
            try:
                import redis
                r = redis.Redis(host=redis_host, port=redis_port, socket_timeout=1)
                r.ping()
                
                # Check if Redis is in master mode
                info = r.info('replication')
                role = info.get('role', '')
                
                if role == 'master':
                    print("✓ Redis is ready and in master mode")
                    sys.exit(0)
                else:
                    print(f"⚠ Redis is not in master mode (role: {role}), forcing master mode...")
                    try:
                        r.replicaof()
                    except:
                        pass
                    time.sleep(1)
            except ImportError:
                # redis-py not available, just check connection
                print("✓ Redis is responding (cannot verify master mode without redis-py)")
                sys.exit(0)
            except Exception as e:
                print(f"Waiting for Redis... (attempt {i+1}/{max_retries}) - {e}")
        else:
            print(f"Waiting for Redis to be available... (attempt {i+1}/{max_retries})")
    except Exception as e:
        print(f"Waiting for Redis... (attempt {i+1}/{max_retries}) - {e}")
    
    time.sleep(1)

print("ERROR: Redis is not ready after", max_retries, "attempts")
sys.exit(1)
EOF

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to verify Redis readiness"
    exit 1
fi

# Start Celery worker
exec celery -A config worker -l info -Q trading,trading_high_priority,default "$@"

