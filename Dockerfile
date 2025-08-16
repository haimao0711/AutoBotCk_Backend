FROM python:3.11

# Tối ưu log và tránh tạo file .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cài pipenv
RUN pip install --upgrade pip && pip install pipenv

# Tạo thư mục app và đặt làm working dir
WORKDIR /app

# Copy Pipfile trước để tối ưu layer cache
COPY Pipfile Pipfile.lock /app/

# Cài thư viện từ Pipfile.lock
RUN pipenv install --deploy --ignore-pipfile

# Copy toàn bộ code vào container
COPY . /app/

# Copy file env production (nếu muốn chạy trong container luôn)
COPY .env.production /app/.env

# Mở port Django/Gunicorn
EXPOSE 8000

# CMD cho production (gunicorn)
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "AutoBotCk_Backend.wsgi:application"]
