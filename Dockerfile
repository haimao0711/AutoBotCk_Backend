# Base image Python 3.11
FROM python:3.11-slim

# Set thư mục làm việc
WORKDIR /app

# Cài đặt các gói hệ thống cần thiết (nếu dùng psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt trước để tận dụng cache Docker
COPY requirements.txt .

# Cài Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Expose cổng
EXPOSE 8000

# Start server bằng Gunicorn
ENV DJANGO_SETTINGS_MODULE=config.settings.production
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
