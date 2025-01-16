FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install gunicorn


RUN chmod +x entrypoint.sh

CMD ["/bin/sh", "entrypoint.sh"]


