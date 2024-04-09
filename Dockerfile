FROM python:3.12-slim
WORKDIR /app
RUN pip install poetry
COPY app/poetry.lock /app/poetry.lock
COPY app/pyproject.toml /app/pyproject.toml
RUN apt update -y && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root
COPY /app/* /app
EXPOSE 8003
COPY /docker-build/entrypoint.sh /app/entrypoint.sh
RUN chmod +x entrypoint.sh