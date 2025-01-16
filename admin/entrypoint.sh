#!/bin/sh

# Очистка базы данных
python manage.py flush --no-input
# Применение миграций
python manage.py migrate


# Сборка статики
python manage.py collectstatic --no-input

# Запуск Gunicorn
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
