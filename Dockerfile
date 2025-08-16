FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy Pipfile và Pipfile.lock trước để tận dụng cache
COPY Pipfile Pipfile.lock /app/

# Cài pipenv
RUN pip install --upgrade pip && pip install pipenv

# Cài tất cả dependencies vào virtualenv
RUN pipenv install --deploy --ignore-pipfile

# Copy toàn bộ source code
COPY . /app/

# Copy file env
COPY ./.env.production /app/.env

EXPOSE 8000

# CMD chạy migrate trước rồi start server
CMD ["sh", "-c", "pipenv run dotenv run -- python manage.py makemigrations && pipenv run dotenv run -- python manage.py migrate && pipenv run dotenv run -- python manage.py runserver 0.0.0.0:8000"]
