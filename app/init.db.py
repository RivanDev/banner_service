import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from application.db.models.banner import Banner
from application.db.models.banner_tag_association import BannerTagAssociation
from application.db.models.base import Base
from application.db.models.feature import Feature
from application.db.models.tag import Tag

engine = create_async_engine(
    url="postgresql+asyncpg://postgres_user:postgres_password@postgres:5432/banners", echo=False
)


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        for i in range(500):
            feature = Feature()
            session.add(feature)
            await session.commit()

        for i in range(500):
            tag = Tag()
            session.add(tag)
            await session.commit()

        # Create banners with associations
        for i in range(1, 400):
            banner = Banner(
                title=f"Banner {i}",
                text=f"Text for Banner {i}",
                url=f"https://example.com/banner/{i}",
                is_active=(True if i % 2 == 0 else False),  # Alternate between True and False
                feature_id=i,
            )
            session.add(banner)
            await session.commit()

            association = BannerTagAssociation(banner_id=banner.id, tag_id=i)
            session.add(association)
            await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
