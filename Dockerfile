# Используем официальный образ Python
FROM python:3.13

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Запуск проекта
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
