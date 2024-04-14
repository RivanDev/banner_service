from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import Response

from application.api.banners.dependencies import (
    admin_auth,
    create_banner,
    get_banners_filtered,
    get_user_banner_by_params,
    update_banner,
    user_auth,
)
from application.api.banners.schemas import BannerOut, CreateBanner, UserBannerOut, BannerOutFiltered
from application.db import crud
from application.db.db_helper import db_helper
from application.db.exceptions import BannerNotFoundException

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
    banner: UserBannerOut = Depends(get_user_banner_by_params),
    token: str = Depends(user_auth),
) -> UserBannerOut:
    return banner


@banner_router.post(
    "/",
    summary="Создание нового баннера",
    responses={
        status.HTTP_201_CREATED: {"model": BannerOut, "description": "Created"},
        status.HTTP_400_BAD_REQUEST: {"description": "Некорректные данные"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Пользователь не авторизован"},
        status.HTTP_403_FORBIDDEN: {"description": "Пользователь не имеет доступа"},
        status.HTTP_404_NOT_FOUND: {"description": "Баннер не найден"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Внутренняя ошибка сервера"},
    },
)
async def create_banner(
    banner: CreateBanner = Depends(create_banner),
    token: str = Depends(admin_auth),
) -> BannerOut:
    return banner


@banner_router.get(
    "/",
    summary="Получение всех баннеров с фильтрацией по фиче и/или тегу",
    responses={
        status.HTTP_200_OK: {"model": list[BannerOutFiltered], "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Пользователь не авторизован"},
        status.HTTP_403_FORBIDDEN: {"description": "Пользователь не имеет доступа"},
        status.HTTP_404_NOT_FOUND: {"description": "Баннер не найден"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Внутренняя ошибка сервера"},
    },
)
async def get_banners_by_filters(
    token: str = Depends(admin_auth),
    feature_id: int | None = None,
    tag_id: int | None = None,
    limit: int | None = None,
    offset: int | None = None,
    banners: list[BannerOutFiltered] = Depends(get_banners_filtered),
):
    return banners


@banner_router.patch(
    "/{id}",
    summary="Обновление содержимого баннера",
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_400_BAD_REQUEST: {"description": "Некорректные данные"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Пользователь не авторизован"},
        status.HTTP_403_FORBIDDEN: {"description": "Пользователь не имеет доступа"},
        status.HTTP_404_NOT_FOUND: {"description": "Баннер не найден"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Внутренняя ошибка сервера"},
    },
)
async def update_banner(
    banner_id: int = Path(..., alias="id"),
    token: str = Depends(admin_auth),
    banner: CreateBanner = Depends(update_banner),
):
    return banner


@banner_router.delete(
    "/{id}",
    summary="Удаление баннера по идентификатору",
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "OK"},
        status.HTTP_400_BAD_REQUEST: {"description": "Некорректные данные"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Пользователь не авторизован"},
        status.HTTP_403_FORBIDDEN: {"description": "Пользователь не имеет доступа"},
        status.HTTP_404_NOT_FOUND: {"description": "Баннер не найден"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Внутренняя ошибка сервера"},
    },
)
async def delete_banner(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    banner_id: int = Path(..., alias="id"),
    token: str = Depends(admin_auth),
):
    try:
        await crud.delete_banner(banner_id, session)
    except BannerNotFoundException:
        raise HTTPException(status_code=404)
    return Response(status_code=204)
