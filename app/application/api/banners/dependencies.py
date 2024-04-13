from fastapi import Depends, Header, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from application.api.banners.schemas import CreateBanner, UserBannerOut, BannerOut, BannerOutFiltered
from application.core.auth import fake_auth_db
from application.db import crud
from application.db.cache import CacheRepo
from application.db.db_helper import db_helper


async def admin_auth(
    token: str = Header(
        default=None,
        description="Токен админа",
        json_schema_extra={"example": "admin_token"},
    )
):
    if not token:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    if token != fake_auth_db.get("admin_token"):
        raise HTTPException(status_code=403, detail="Пользователь не имеет доступа")


async def user_auth(
    token: str = Header(
        default=None,
        description="Токен пользователя",
        json_schema_extra={"example": "user_token"},
    )
):
    if not token:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    if token != fake_auth_db.get("user_token"):
        raise HTTPException(status_code=403, detail="Пользователь не имеет доступа")


async def get_user_banner_by_params(
    tag_id: int = Query(..., description="Тэг пользователя"),
    feature_id: int = Query(..., description="Идетнификатор фичи"),
    use_last_revision: bool = Query(False, description="Получать актуальную информацию"),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    cacher: CacheRepo = Depends(CacheRepo),
) -> UserBannerOut:
    if not use_last_revision:
        banner_in_cache = await cacher.read_cache(f"Banner tag_id {tag_id}, feature_id {feature_id}")
        if banner_in_cache is not None:
            return banner_in_cache
    banner = await crud.get_banner(feature_id=feature_id, session=session)
    tag = await crud.get_tag(tag_id=tag_id, session=session)
    if not banner.is_active:
        raise HTTPException(status_code=404, detail="Баннер не найден")
    if banner is not None and tag in banner.tags:
        model_out = UserBannerOut(
            title=banner.title,
            text=banner.text,
            url=banner.url,
        )
        await cacher.create_cache(f"Banner tag_id {tag_id}, feature_id {feature_id}", model_out)
        return model_out
    raise HTTPException(status_code=404, detail="Баннер не найден")


async def get_banners_filtered(
    feature_id: int = None,
    tag_id: int = None,
    limit: int = None,
    offset: int = None,
    session: AsyncSession = Depends(
        db_helper.scoped_session_dependency,
    ),
) -> list[BannerOutFiltered]:
    banners = await crud.get_banners(tag_id=tag_id, feature_id=feature_id, session=session, limit=limit, offset=offset)
    if banners:
        banners_out = []
        for banner in banners:
            tags_ids = [tag.id for tag in banner.tags]
            data = BannerOutFiltered(
                banner_id=banner.id,
                tags_ids=tags_ids,
                feature_id=feature_id,
                content={
                    "title": banner.title,
                    "text": banner.text,
                    "url": banner.url,
                },
                is_active=banner.is_active,
                created_at=banner.created_at,
                updated_at=banner.updated_at,
            )
            banners_out.append(data)
        return banners_out
    raise HTTPException(status_code=404, detail="Баннер не найден")


async def create_banner(
    banner: CreateBanner, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> BannerOut:
    banner = await crud.create_banner(banner=banner, session=session)
    banner_out = BannerOut(banner_id=banner.id)
    return banner_out


async def update_banner(
    id: int, banner: CreateBanner, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    banner = await crud.update_banner(
        banner_id=id,
        banner=banner,
        session=session,
    )
    return banner


async def create_tag(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    tag = await crud.create_tag(session=session)
    return tag
