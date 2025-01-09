#!/bin/sh

cd app
# Очистка базы данных
python manage.py flush --no-input
# Применение миграций
python manage.py migrate

# Запуск Gunicorn
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
