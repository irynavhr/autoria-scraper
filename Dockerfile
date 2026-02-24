# 1. Базовий образ Python
FROM python:3.11-slim

# 2. Робоча папка контейнера
WORKDIR /app

# 3. Скопіювати список залежностей
COPY requirements.txt .

# 4. Встановити залежності
RUN pip install --no-cache-dir -r requirements.txt

# 5. Скопіювати весь проєкт у контейнер
COPY . .

# 6. Запуск застосунку
CMD ["python", "app/main.py"]