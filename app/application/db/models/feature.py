from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from .banner import Banner


class Feature(Base):
    banners: Mapped[list["Banner"]] = relationship(back_populates="feature")
