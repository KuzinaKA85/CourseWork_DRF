FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаём папки для статики и медиа
RUN mkdir -p /app/media /app/staticfiles

# Собираем статику (через poetry run)
RUN python manage.py collectstatic --noinput --no-input || true

# Открываем порт 8000 (внутри контейнера)
EXPOSE 8000

# Запускаем через poetry run
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]