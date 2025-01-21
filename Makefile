# Variables
COMPOSE_FILE := docker-compose.yml
SERVICE_WEB := django_web
SERVICE_FASTAPI := fastapi
SERVICE_DB := postgres_db
SERVICE_REDIS := redis

# Commands
.PHONY: build up down restart logs web-logs fastapi-logs db-logs redis-logs shell-web shell-fastapi

# Build the containers
bd:
	docker-compose -f $(COMPOSE_FILE) build

# Start the containers
up:
	docker-compose -f $(COMPOSE_FILE) up -d

# Stop and remove the containers
down:
	docker-compose -f $(COMPOSE_FILE) dow
	

# Restart the containers
restart:
	docker-compose -f $(COMPOSE_FILE) restart

# Show logs for all services
logs:
	docker-compose -f $(COMPOSE_FILE) logs -f

# Show logs for the web service
web-logs:
	docker-compose -f $(COMPOSE_FILE) logs -f $(SERVICE_WEB)

# Show logs for the FastAPI service
fastapi-logs:
	docker-compose -f $(COMPOSE_FILE) logs -f $(SERVICE_FASTAPI)

# Show logs for the database service
db-logs:
	docker-compose -f $(COMPOSE_FILE) logs -f $(SERVICE_DB)

# Show logs for the Redis service
redis-logs:
	docker-compose -f $(COMPOSE_FILE) logs -f $(SERVICE_REDIS)

# Open a shell in the web container
shell-web:
	docker-compose -f $(COMPOSE_FILE) exec $(SERVICE_WEB) /bin/sh

# Open a shell in the FastAPI container
shell-fastapi:
	docker-compose -f $(COMPOSE_FILE) exec $(SERVICE_FASTAPI) /bin/sh

# Run Django management commands (e.g., make manage cmd="migrate")
manage:
	docker-compose -f $(COMPOSE_FILE) exec $(SERVICE_WEB) python manage.py $(cmd)

# Collect static files
collectstatic:
	docker-compose -f $(COMPOSE_FILE) exec $(SERVICE_WEB) python manage.py collectstatic --no-input

# Run tests
tests:
	docker-compose -f $(COMPOSE_FILE) exec $(SERVICE_FASTAPI) /bin/sh -c "pytest -vv"

# Remove all unused Docker objects (images, volumes, networks)
clean:
	docker system prune -f