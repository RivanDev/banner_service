DC = docker compose
APP_FILE = docker-compose.local.yaml
APP_CONTAINER = banners_app

lint:
	cd app && poetry run ruff check --fix application && poetry run black --check application

mypy:
	cd app && poetry run mypy application

up:
	${DC} -f ${APP_FILE} up --build -d

down:
	${DC} -f ${APP_FILE} down
