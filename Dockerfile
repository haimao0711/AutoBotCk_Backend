# Base image Python 3.11
FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements và install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Cấp quyền thực thi cho entrypoint
RUN chmod +x entrypoint.sh

# Expose port Gunicorn
EXPOSE 8000

# Set env cho Django
ENV DJANGO_SETTINGS_MODULE=config.settings.production

# Start script entrypoint.sh (bao gồm migrate, collectstatic, scheduler, Gunicorn)
CMD ["./entrypoint.sh"]
