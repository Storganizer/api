from model.base import Base

from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Box(Base):

    __tablename__ = "box"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    lastAccess: DateTime(timezone=True), server_default=func.now()

    items: Mapped[List["Item"]] = relationship(
        back_populates="item", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r}, description={self.description!r}, lastAccess={self.lastAccess!r})"
