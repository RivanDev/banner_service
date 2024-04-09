from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .banner import Banner


class Tag(Base):
    banner_id: Mapped[int] = mapped_column("banners.id")
    banner: Mapped["Banner"] = relationship(back_populates="tags")
