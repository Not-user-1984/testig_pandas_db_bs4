FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

RUN pip install gunicorn

COPY . .


RUN chmod +x entrypoint.sh

CMD ["/bin/sh", "app/entrypoint.sh"]


