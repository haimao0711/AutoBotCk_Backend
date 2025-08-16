FROM python:3.11-slim

# Cài các công cụ cần thiết + psql client
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

COPY wait-for-postgres.sh /usr/local/bin/wait-for-postgres.sh
RUN chmod +x /usr/local/bin/wait-for-postgres.sh

EXPOSE 8000

CMD ["bash", "-c", "/usr/local/bin/wait-for-postgres.sh stock-predict-postgres && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
