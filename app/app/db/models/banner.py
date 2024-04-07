from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .feature import Feature
    from .tag import Tag


class Banner(Base):
    is_active: bool = True

    feature_id: Mapped[int] = mapped_column(ForeignKey("features.id"))
    feature: Mapped["Feature"] = relationship(back_populates="banners")
    tags: Mapped[list["Tag"]] = relationship(back_populates="banner")
