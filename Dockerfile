FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Cài pipenv và python-dotenv với CLI
RUN pip install --upgrade pip && pip install pipenv "python-dotenv[cli]"

WORKDIR /app

# Copy Pipfile trước để tận dụng cache
COPY Pipfile Pipfile.lock /app/

RUN pipenv install --deploy --ignore-pipfile

# Copy toàn bộ source code
COPY . /app/

# Copy .env production vào container
COPY ./.env.production /app/.env

EXPOSE 8000

# Chạy app với dotenv load .env
CMD ["pipenv", "run", "python", "-m", "dotenv", "run", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
