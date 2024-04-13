from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.api.banners.schemas import CreateBanner
from application.db.exceptions import BannerNotFoundException
from application.db.models.banner import Banner
from application.db.models.banner_tag_association import BannerTagAssociation
from application.db.models.feature import Feature
from application.db.models.tag import Tag


async def get_banner_by_id(banner_id: int, session: AsyncSession) -> Banner:
    banner = await session.scalar(select(Banner).filter(Banner.id == banner_id).options(selectinload(Banner.tags)))
    if not banner:
        raise BannerNotFoundException
    return banner


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


async def update_banner(banner_id: int, banner: CreateBanner, session: AsyncSession):
    data = banner.model_dump()
    tag_ids = data.pop("tag_ids")
    content = data.pop("content")
    tags = await get_tags_by_ids(tag_ids=tag_ids, session=session)
    for key, val in content.items():
        data[key] = val

    banner_stm = select(Banner).options(selectinload(Banner.tags)).filter(Banner.id == banner_id)
    res = await session.execute(banner_stm)
    banner_instance = res.scalar()

    banner_instance.tags.clear()
    for tag in tags:
        banner_instance.tags.append(tag)

    for field, value in data.items():
        setattr(banner_instance, field, value)
    await session.commit()

    return banner


async def delete_banner(banner_id: id, session: AsyncSession):
    banner = await get_banner_by_id(banner_id=banner_id, session=session)
    await session.delete(banner)
    await session.commit()


async def get_tags_by_ids(tag_ids: list, session: AsyncSession):
    stmt = select(Tag).filter(Tag.id.in_(tag_ids))
    result: Result = await session.execute(stmt)
    tags = result.scalars().all()
    return list(tags)
