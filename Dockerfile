# Используем базовый образ Python
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем poetry
RUN pip install poetry

# Копируем зависимости в контейнер
COPY poetry.lock pyproject.toml /app/

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-root

# Копируем код приложения в контейнер
COPY . /app/
