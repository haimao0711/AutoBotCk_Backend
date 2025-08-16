#!/bin/bash
set -e

# Kiểm tra environment variables
: "${POSTGRES_HOST:?Need to set POSTGRES_HOST}"
: "${POSTGRES_USER:?Need to set POSTGRES_USER}"
: "${POSTGRES_PASSWORD:?Need to set POSTGRES_PASSWORD}"
: "${POSTGRES_DB:?Need to set POSTGRES_DB}"

host="${1:-$POSTGRES_HOST}"
shift || true

echo "Waiting for PostgreSQL at $host ..."

until PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' >/dev/null 2>&1; do
  echo "Postgres is unavailable - sleeping 2s"
  sleep 2
done

echo "Postgres is up - executing command"
exec "$@"
