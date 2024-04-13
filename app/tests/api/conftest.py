import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from application.main import create_app


@pytest.fixture()
def app() -> FastAPI:
    app = create_app()
    return app


@pytest.fixture()
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
