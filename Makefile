DC = docker compose
APP_FILE = docker-compose.local.yaml
TEST_FILE = docker-compose.test.yaml
APP_CONTAINER = banners_app
EXEC = docker exec -it

lint:
	cd app && poetry run ruff check --fix application && poetry run black --check application

mypy:
	cd app && poetry run mypy application

up:
	${DC} -f ${APP_FILE} up --build -d

down:
	${DC} -f ${APP_FILE} down

.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest tests
