from fastapi import APIRouter, Header, Query, Depends
from starlette import status

from application.api.banners.dependencies import get_banner_by_ids, create_banner
from application.api.banners.schemas import BannerOut, UserBannerOut, CreateBanner

banner_router = APIRouter()
user_banner_router = APIRouter()


@user_banner_router.get(
    "/",
    summary="Получение баннера для пользователя",
    responses={
        status.HTTP_200_OK: {"model": UserBannerOut, "description": "Баннер пользователя"},
        status.HTTP_400_BAD_REQUEST: {"description": "Некорректные данные"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Пользователь не авторизован"},
        status.HTTP_403_FORBIDDEN: {"description": "Пользователь не имеет доступа"},
        status.HTTP_404_NOT_FOUND: {"description": "Баннер не найден"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Внутренняя ошибка сервера"},
    },
)
async def get_user_banner(
    banner: BannerOut = Depends(get_banner_by_ids),
    tag_id: int = Query(..., description="Тэг пользователя"),
    feature_id: int = Query(..., description="Идетнификатор фичи"),
    use_last_revision: bool = Query(False, description="Получать актуальную информацию"),
    token: str = Header(description="Токен пользователя", json_schema_extra={"example": "user_token"}),
):
    return banner


@banner_router.post("/", response_model=BannerOut, summary="Создание нового баннера")
async def create_banner(
    banner: CreateBanner = Depends(create_banner),
    token: str = Header(description="Токен админа", json_schema_extra={"example": "admin_token"}),
):
    return banner


async def get_user_role(
    token: str = Header(
        default=None,
        description="Токен админа",
        json_schema_extra={"example": "admin_token"},
    )
):
    return token


@banner_router.get(
    "/",
    summary="Получение всех баннеров с фильтрацией по фиче и/или тегу",
    response_description="OK",
)
async def get_banners_by_filters(
    token: str = Depends(get_user_role),
    test: int = Query(None),
    # feature_id: int | None = None,
    # tag_id: int | None = None,
    # limit: int | None = None,
    # offset: int | None = None,
    # banners: list[BannerOut] = Depends(get_banners_filtered),
):
    print(token)
    return 1  # banners
