from pydantic import BaseModel, constr, ConfigDict


class BannerIn(BaseModel): ...


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


class Tag(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Feature(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)
