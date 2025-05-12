# Используем Python 3.12 как базовый образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Экспонируем порт, на котором будет работать Flask-приложение
EXPOSE 5000

# Команда для запуска Flask приложения
CMD ["python", "app/crawler.py"]
