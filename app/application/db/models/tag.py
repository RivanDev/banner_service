from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .banner import Banner


class Tag(Base):
    banners: Mapped[list["Banner"]] = relationship(
        secondary="bannertagassociations",
        back_populates="tags",
    )
