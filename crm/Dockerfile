# Используем базовый образ Python
FROM python:3.12.2

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY pyproject.toml poetry.lock /app/

# Устанавливаем Poetry для управления зависимостями
RUN python -m pip install --no-cache-dir poetry==1.4.2 \
    && poetry config virtualenvs.create false \
    && poetry install --without dev,tests --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

# Копируем код проекта в контейнер
COPY . /app

# Выполняем миграции базы данных
#RUN python manage.py migrate

# Команда для запуска приложения
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh
CMD ["./wait-for-it.sh", "db:5432", "--", "gunicorn", "crm.wsgi:application", "--bind", "0.0.0.0:8000"]
