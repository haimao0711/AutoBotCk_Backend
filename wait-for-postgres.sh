#!/bin/bash
# Chờ Postgres sẵn sàng trước khi chạy app
host="$1"
shift
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done
echo "Postgres is up - executing command"
exec "$@"
