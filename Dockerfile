FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy Pipfile và lockfile trước để tận dụng cache
COPY Pipfile Pipfile.lock /app/

# Cài pipenv
RUN pip install --upgrade pip && pip install pipenv

# Cài tất cả dependencies vào virtualenv
RUN pipenv install --deploy --ignore-pipfile

# Copy source code
COPY . /app/

# Copy .env.production vào container
COPY ./.env.production /app/.env

EXPOSE 8000

# Chạy app qua pipenv và dotenv CLI
CMD ["pipenv", "run", "dotenv", "run", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
