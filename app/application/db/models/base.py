from datetime import datetime

from sqlalchemy import sql
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(default=int, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=sql.func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=sql.func.now(),
                                                 onupdate=sql.func.now())
