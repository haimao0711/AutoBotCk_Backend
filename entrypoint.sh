#!/bin/bash

# Thiết lập môi trường, nếu cần
echo "🔧 Running environment setup..."

# Migrate database (áp dụng các migration của Django)
python manage.py migrate

# Thu thập các file static của Django
python manage.py collectstatic --noinput

# Restart tất cả các schedulers (nếu có)
python manage.py restart_schedulers

# Khởi động Gunicorn (hoặc server web bạn sử dụng)
exec gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
