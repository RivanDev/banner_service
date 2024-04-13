from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BannerOut(BaseModel):
    banner_id: int

    model_config = ConfigDict(from_attributes=True)


class UserBannerOut(BaseModel):
    title: str
    text: str
    url: str

    model_config = ConfigDict(from_attributes=True)


class CreateBanner(BaseModel):
    tag_ids: list = [0]
    feature_id: int
    content: UserBannerOut
    is_active: bool = True


class BannerOutFiltered(BaseModel):
    banner_id: int
    tags_ids: list
    feature_id: int
    content: UserBannerOut
    is_active: bool
    created_at: datetime
    updated_at: datetime
