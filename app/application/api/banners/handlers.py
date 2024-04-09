from fastapi import APIRouter, Header

from .schemas import BannerOut

banner_router = APIRouter()


@banner_router.post("/", response_model=BannerOut, summary="Создание нового баннера")
async def create_banner(
    token: str = Header(description="Токен админа", json_schema_extra={"example": "admin_token"})
): ...
