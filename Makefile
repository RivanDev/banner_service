lint:
	poetry run ruff check --fix app && poetry run black --check app

mypy:
	poetry run mypy app
