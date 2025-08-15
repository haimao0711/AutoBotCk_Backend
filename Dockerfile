FROM python:3.11

# Tối ưu log và tránh tạo file .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Cài pipenv và python-dotenv với CLI
RUN pip install --upgrade pip && pip install pipenv "python-dotenv[cli]"

# Tạo thư mục app và đặt làm working dir
WORKDIR /app

# Copy Pipfile trước để tối ưu layer cache
COPY Pipfile Pipfile.lock /app/

# Cài thư viện từ Pipfile.lock (trong đó đã có pandas)
RUN pipenv install --deploy --ignore-pipfile

# Copy toàn bộ code vào container
COPY . /app/

# Copy .env production vào container
COPY ./.env.production /app/.env

# Mở port mặc định Django
EXPOSE 8000

# Chạy app bằng pipenv và Django dev server, load .env
CMD ["pipenv", "run", "python", "-m", "dotenv", "run", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
