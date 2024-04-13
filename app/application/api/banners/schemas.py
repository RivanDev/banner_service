from fastapi import Header, Path
from pydantic import BaseModel, ConfigDict, Field


class BannerInFiltered(BaseModel):

    token: str = Field(
        Header(
            default=None,
            description="Токен админа",
            json_schema_extra={"example": "admin_token"},
        )
    )
    feature_id: int | None = None
    tag_id: int | None = None
    limit: int | None = None
    offset: int | None = None


class BannerOut(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserBannerOut(BaseModel):
    title: str
    text: str
    url: str


class CreateBanner(BaseModel):
    tag_ids: list = [0]
    feature_id: int
    content: UserBannerOut
    is_active: bool = True


class BannerId(BaseModel):

    banner_id: int = Field(default=Path(...), alias="id")


class Tag(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Feature(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)
