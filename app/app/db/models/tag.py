from sqlalchemy.orm import Mapped, mapped_column, relationship

from .banner import Banner
from .base import Base


class Tag(Base):
    banner_id: Mapped[int] = mapped_column("banners.id")
    banner: Mapped["Banner"] = relationship(back_populates="tags")
