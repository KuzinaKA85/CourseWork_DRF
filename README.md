# CourseWork_DRF — Трекер привычек

API для трекера привычек с интеграцией Telegram-бота. Напоминания приходят автоматически через Celery.

## Технологии

- Django + DRF
- PostgreSQL
- Redis + Celery
- Docker + Docker Compose
- Nginx
- GitHub Actions (CI/CD)

---

## Локальный запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/KuzinaKA85/CourseWork_DRF.git
cd CourseWork_DRF
```
### 2. Настройте переменные окружения
Скопируйте файл .env.example в .env:

```bash
cp .env.example .env
```
Отредактируйте .env, указав свои значения.

### 3. Запустите проект
```bash
docker-compose up -d --build
```

### 4. Откройте приложение
- API: http://localhost:8000

- Админка: http://localhost:8000/admin

- Swagger документация: http://localhost:8000/swagger/

- Redoc документация: http://localhost:8000/redoc/

### 5. Проверка работоспособности сервисов
5.1 Проверка Web сервиса (Django)
```bash
# Проверить статус контейнера
docker ps | grep web

# Проверить доступность API
curl http://localhost:8000/

# Открыть в браузере
start http://localhost:8000
```
5.2 Проверка PostgreSQL

```bash
# Проверить подключение к БД
docker-compose exec db pg_isready -U postgres

# Ожидаемый ответ: /var/run/postgresql:5432 - accepting connections
```
5.3 Проверка Redis
```bash
# Проверить, что Redis работает
docker-compose exec redis redis-cli ping

# Ожидаемый ответ: PONG
```
5.4 Проверка Celery Worker
```bash
# Проверить статус Celery
docker-compose exec celery celery -A config status

# Ожидаемый вывод: celery@... OK
```
5.5 Проверка всех сервисов одной командой
```bash
docker-compose ps
```
*Все сервисы должны быть в статусе Up (кроме celery-beat, он может перезапускаться).*

5.6 Остановка проекта
```bash
docker compose down
```
5.7 Остановка проекта с полной очисткой
```bash
docker compose down -v
```
### 6. Переменные окружения
Все чувствительные переменные вынесены в файл .env
- SECRET_KEY=
- DEBUG=
- DATABASE_NAME=
- DATABASE_USER=
- DATABASE_PASSWORD=
- DATABASE_HOST=
- DATABASE_PORT=
- CELERY_BROKER_URL=
- CELERY_RESULT_BACKEND=
- EMAIL_HOST_USER=
- EMAIL_HOST_PASSWORD=

### 7. Структура проекта

---
    CourseWork_DRF/
    ├── .venv/                 # Виртуальное окружение (не включается в Git)
    ├── .github/               # CI/CD конфигурация
    ├── config/                # Настройки проекта
    ├── habits/                # Приложение привычки
    ├── nginx/                 # Конфигурация Nginx (nginx.conf, Dockerfile)
    ├── static/                # Статические файлы (разработка)
    ├── staticfiles/           # Статические файлы (собранные)
    ├── telegram_bot/          # Telegram-бот
    ├── users/                 # Пользователи + JWT
    ├── docker-compose.yaml    # Оркестрация сервисов
    ├── Dockerfile             # Инструкция для сборки образа
    ├── .env.example           # Шаблон переменных окружения
    ├── manage.py              # Утилита командной строки Django
    ├── requirements.txt       # Зависимости проекта
    └── README.md              # Документация
---

### Важно

В Docker:
- PostgreSQL доступен по хосту `db`
- Redis доступен по хосту `redis`

Использование `localhost` внутри контейнеров не работает.

## Деплой на удалённый сервер (Ubuntu)

### 1. Подготовка сервера

Подключитесь к серверу по SSH:

```bash
ssh пользователь@ip_адрес
```
 Установите Docker
```bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```
Выйдете и зайдите заново
```bash
exit
ssh пользователь@ip_адрес
```
Проверьте Docker
```bash
docker ps
```
### 2. Настройка GitHub Secrets
В репозитории: Settings → Secrets and variables → Actions
Добавьте секреты:

- DOCKER_HUB_USERNAME	- логин на Docker Hub
- DOCKER_HUB_ACCESS_TOKEN	Токен (Docker Hub → Settings → New Access Token)
- SSH_USER - имя пользователя на сервере
- SERVER_IP - IP вашего сервера
- SSH_KEY - содержимое приватного ключа (cat ~/.ssh/id_ed25519)

### 3. GitHub Actions (уже настроен)
В вашем проекте есть файл .github/workflows/ci.yml. Он автоматически:
- Запускает линтеры
- Запускает тесты
- Собирает Docker-образ
- Отправляет образ в Docker Hub
- Подключается к серверу и запускает контейнер

### 4. Запуск деплоя
Просто запушите изменения в любую ветку:
```bash
git add .
git commit -m "Deploy"
git push origin название_ветки
```
Статус смотрите на вкладке Actions в GitHub.
### 5. Проверка
Откройте в браузере:
```
http://IP_вашего_сервера
```
### 6. Команды на сервере
```bash
# Просмотр контейнеров
docker ps

# Логи приложения
docker-compose logs web --tail 50

# Перезапуск
cd ~/CourseWork_DRF && docker-compose restart web

# Создание суперпользователя
docker-compose exec web python manage.py csu
```

