# Sử dụng Python 3.11 slim
FROM python:3.11-slim

# Cài các công cụ cần thiết
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements trước để cache
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Thêm script chờ DB sẵn sàng
COPY wait-for-postgres.sh /usr/local/bin/wait-for-postgres.sh
RUN chmod +x /usr/local/bin/wait-for-postgres.sh

# Expose port
EXPOSE 8000

# Command chạy Gunicorn sau khi DB ready
CMD ["bash", "-c", "/usr/local/bin/wait-for-postgres.sh && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
