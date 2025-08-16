#!/bin/bash
set -e  # exit ngay khi có lỗi

echo "🔧 Running environment setup..."

# Chờ database sẵn sàng
echo "⏳ Waiting for PostgreSQL to be ready..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 2
done
echo "✅ PostgreSQL is ready!"

# Áp dụng migrations
python manage.py migrate --noinput

# Thu thập static files
python manage.py collectstatic --noinput

# Khởi động lại schedulers (nếu có)
if python manage.py restart_schedulers 2>/dev/null; then
    echo "✅ Schedulers restarted"
fi

# Khởi động Gunicorn với settings chính xác
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
