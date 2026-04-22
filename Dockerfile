# Используем официальный slim-образ Python 3.11
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Копируем pyproject.toml и poetry.lock для установки зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости Python с помощью Poetry
# RUN poetry install --no-root

# Устанавливаем зависимости
RUN poetry install --no-interaction --no-ansi --no-root

# Копируем исходный код приложения в контейнер
COPY . .

# # Определяем переменные окружения
# ENV SECRET_KEY="SECRET_KEY"
# ENV CELERY_BROKER_URL="CELERY_BROKER_URL"
# ENV CELERY_BACKEND="CELERY_RESULT_BACKEND"

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media /app/staticfiles

# Собираем статику (если есть manage.py)
RUN poetry run python manage.py collectstatic --noinput || true

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000

# Команда для запуска приложения
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["poetry", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]