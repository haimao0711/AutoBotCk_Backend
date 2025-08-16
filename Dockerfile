FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy Pipfile trước để tận dụng cache
COPY Pipfile Pipfile.lock /app/

# Cài pipenv trong system Python
RUN pip install --upgrade pip && pip install pipenv

# Cài dependencies vào pipenv, bao gồm python-dotenv[cli] trong virtualenv
RUN pipenv install --deploy --ignore-pipfile python-dotenv[cli]

# Copy toàn bộ source code
COPY . /app/

# Copy .env.production vào container
COPY ./.env.production /app/.env

EXPOSE 8000

# Chạy app, pipenv sẽ load .env trực tiếp
CMD ["pipenv", "run", "python", "-m", "dotenv", "run", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
