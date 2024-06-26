from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .feature import Feature
    from .tag import Tag


class Banner(Base):
    title: Mapped[str]
    text: Mapped[str]
    url: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    feature_id: Mapped[int] = mapped_column(ForeignKey("features.id"))
    feature: Mapped["Feature"] = relationship(back_populates="banners")

    tags: Mapped[list["Tag"]] = relationship(
        secondary="bannertagassociations",
        back_populates="banners",
    )
