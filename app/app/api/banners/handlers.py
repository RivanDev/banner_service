from fastapi import APIRouter, Header

from .schemas import BannerOut

banner_router = APIRouter(prefix="/banner")


@banner_router.post("/", response_model=BannerOut, summary="Создание нового баннера")
async def create_banner(token: str = Header(..., description="Токен админа")): ...
