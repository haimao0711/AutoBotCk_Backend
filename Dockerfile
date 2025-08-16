FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install --upgrade pip && pip install pipenv

RUN pipenv install --deploy --ignore-pipfile

COPY . /app/
COPY ./.env.production /app/.env

EXPOSE 8000

CMD ["pipenv", "run", "python", "-m", "dotenv", "run", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
