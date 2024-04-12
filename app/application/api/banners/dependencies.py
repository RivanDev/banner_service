from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from application.api.banners.schemas import UserBannerOut, CreateBanner
from application.db import crud
from application.db.db_helper import db_helper
from application.db.models.banner import Banner


async def get_banner_by_ids(
    tag_id: int, feature_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> Banner:
    banner = await crud.get_banner(feature_id=feature_id, session=session)
    if banner is not None and tag_id in banner.tags:
        return banner
    raise HTTPException(status_code=404, detail="Баннер не найден")


async def get_banners_filtered(
    limit: int,
    offset: int,
    tag_id: int,
    feature_id: int,
    session: AsyncSession = Depends(
        db_helper.scoped_session_dependency,
    ),
) -> list[Banner]:
    banners = await crud.get_banners(tag_id=tag_id, feature_id=feature_id, session=session, limit=limit, offset=offset)
    if banners is not None:
        return banners
    raise HTTPException(status_code=404, detail="Баннер не найден")


async def create_banner(banner: CreateBanner, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    banner = await crud.create_banner(banner=banner, session=session)
    return banner


async def create_tag(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    tag = await crud.create_tag(session=session)
    return tag
