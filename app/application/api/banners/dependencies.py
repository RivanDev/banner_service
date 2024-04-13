from fastapi import Depends, HTTPException, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession

from application.api.banners.schemas import CreateBanner
from application.core.auth import fake_auth_db
from application.db import crud
from application.db.db_helper import db_helper
from application.db.models.banner import Banner


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
    return token


async def get_user_banner_by_params(
    tag_id: int = Query(..., description="Тэг пользователя"),
    feature_id: int = Query(..., description="Идетнификатор фичи"),
    use_last_revision: bool = Query(False, description="Получать актуальную информацию"),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Banner:
    banner = await crud.get_banner(feature_id=feature_id, session=session)
    tag = await crud.get_tag(tag_id=tag_id, session=session)
    if banner is not None and tag in banner.tags:
        return banner
    raise HTTPException(status_code=404, detail="Баннер не найден")


async def get_banners_filtered(
    feature_id: int = None,
    tag_id: int = None,
    limit: int = None,
    offset: int = None,
    session: AsyncSession = Depends(
        db_helper.scoped_session_dependency,
    ),
) -> list[Banner]:
    banners = await crud.get_banners(tag_id=tag_id, feature_id=feature_id, session=session, limit=limit, offset=offset)
    if banners:
        return banners
    raise HTTPException(status_code=404, detail="Баннер не найден")


async def create_banner(banner: CreateBanner, session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    banner = await crud.create_banner(banner=banner, session=session)
    return banner


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
