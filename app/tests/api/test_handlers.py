import pytest
from fastapi import FastAPI
from httpx import Response, AsyncClient


@pytest.mark.asyncio
async def test_get_user_banner_success(app: FastAPI, client: AsyncClient):
    url = app.url_path_for("get_user_banner")
    print(url)
    url = url + "?tag_id=1&feature_id=1&use_last_revision=false"
    print(url)
    response: Response = await client.post(
        url=url,
        headers={"token": "456"},
    )

    assert response.status_code == 200
