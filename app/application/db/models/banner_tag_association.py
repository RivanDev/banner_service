import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class BannerTagAssociation(Base):
    banner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("banners.id"))
    tag_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tags.id"))
