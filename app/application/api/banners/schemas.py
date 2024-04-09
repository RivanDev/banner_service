from pydantic import BaseModel


class BannerIn(BaseModel):
    ...


class BannerOut(BaseModel):
    banner_id: int
