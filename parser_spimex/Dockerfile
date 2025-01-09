FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python setup.py install

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]