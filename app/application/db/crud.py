from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.api.banners.schemas import CreateBanner
from application.db.models.banner import Banner
from application.db.models.banner_tag_association import BannerTagAssociation
from application.db.models.feature import Feature
from application.db.models.tag import Tag


async def get_banner(feature_id: int, session: AsyncSession) -> Banner:
    stmt = select(Banner).options(selectinload(Banner.tags)).filter(Banner.feature_id == feature_id)
    result: Result = await session.execute(stmt)
    banner = result.scalar().all()
    return banner


async def get_banners(
    tag_id: int,
    feature_id: int,
    session: AsyncSession,
    limit: int | None,
    offset: int | None,
) -> list[Banner]:
    stmt = (
        select(Banner)
        .filter(Banner.feature_id == feature_id)
        .join(BannerTagAssociation)
        .filter(
            BannerTagAssociation.tag_id == tag_id,
        )
        .limit(limit=limit)
        .offset(offset=offset)
    )
    result: Result = await session.execute(stmt)
    banners = result.scalars().all()
    return list(banners)


async def create_tag(session: AsyncSession):
    instance = Tag()
    session.add(instance)
    await session.commit()
    return instance


async def create_feature(session: AsyncSession):
    instance = Feature()
    session.add(instance)
    await session.commit()
    return instance


async def create_banner(banner: CreateBanner, session: AsyncSession):
    data = banner.model_dump()
    tag_ids = data.pop("tag_ids")
    content = data.pop("content")
    tags = await get_tags_by_ids(tag_ids, session)
    data["tags"] = tags
    for key, val in content.items():
        data[key] = val
    instance = Banner(**data)
    session.add(instance)
    await session.commit()
    return instance


async def get_tags_by_ids(tag_ids: list, session: AsyncSession):
    stmt = select(Tag).filter(Tag.id.in_(tag_ids))
    result: Result = await session.execute(stmt)
    tags = result.scalars().all()
    return list(tags)
