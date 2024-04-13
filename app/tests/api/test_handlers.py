import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import Response


@pytest.mark.asyncio
async def test_get_user_banner_200(app: FastAPI, client: TestClient):
    url = app.url_path_for("get_user_banner")
    url = url + "?tag_id=1&feature_id=1&use_last_revision=false"
    response: Response = client.get(
        url=url,
        headers={"token": "a38f7f6a-5466-4edd-8bd0-f32cc2beb3bd"},
    )
    assert response.status_code == 200
