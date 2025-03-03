# Aiogram E-Commerce Bot & Django Admin

Этот проект включает в себя Telegram-бот для e-commerce, написанный на Aiogram 3, и админ-панель на Django. Оба приложения используют общую базу данных PostgreSQL и работают в Docker-контейнерах.

## 🚀 Функционал
- Каталог товаров с категориями и подкатегориями
- Добавление товаров в корзину и оформление заказа
- Оплата через YooKassa
- Экспорт заказов в Excel
- Админ-панель для управления пользователями и заказами

## 📦 Установка и запуск

### 1. Локальный запуск

#### 🔹 Настройка окружения
Перед запуском убедитесь, что у вас установлен Python 3.10+ и PostgreSQL. Создайте файл `.env` и добавьте в него переменные окружения:

```ini
DEBUG=True
DJANGO_SECRET_KEY=django_secret_key
POSTGRES_DB=db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
YOOKASSA_SECRET_KEY=test_secret
YOOKASSA_SHOP_ID=test_shop_id
TOKEN=telegram_bot_token
```

#### 🔹 Запуск Django
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Создание суперпользователя
python manage.py runserver  # Запуск сервера
```

#### 🔹 Запуск Telegram-бота
```sh
python bot/main.py
```

### 2. Запуск в Docker

#### 🔹 Сборка и запуск контейнеров
```sh
docker-compose up --build
```

При необходимости можно запустить сервис в фоновом режиме:
```sh
docker-compose up -d --build
```

#### 🔹 Остановка контейнеров
```sh
docker-compose down
```

## 📜 Полезные команды

#### Проверка логов контейнера
```sh
docker logs -f django  # Логи Django
```
```sh
docker logs -f telegram-bot  # Логи бота
```

#### Выполнение команд Django в контейнере
```sh
docker exec -it django python manage.py createsuperuser
```

## ✨ Доработки и будущие планы
- [ ] Улучшение логирования
- [ ] Добавление кеширования (Redis)
- [ ] Поддержка многовалютных платежей
