DC = docker compose
APP_FILE = docker-compose.local.yaml
APP_CONTAINER = banners_app

lint:
	poetry run ruff check --fix app && poetry run black --check app

mypy:
	poetry run mypy app

up:
	${DC} -f ${APP_FILE} up --build -d

down:
	${DC} -f ${APP_FILE} down
