FROM python:3.12.3-slim

# Устанавливает необходимые зависимости для psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Переменные окружения для Poetry
ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Устанавливает poetry
RUN python3 -m venv $POETRY_VENV && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==$POETRY_VERSION

ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Устанавливает рабочую директорию
WORKDIR /app

# Копирует файлы проекта
COPY pyproject.toml poetry.lock ./

# Установка зависимостей с помощью Poetry
RUN poetry install

# Копирует приложение
COPY . .
