from model.base import Base

import enum
from typing import List
from typing import Optional
from sqlalchemy import String
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class ItemStates(enum.Enum):
    stored = 1
    in_use = 2

class Item(Base):

    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    image: Mapped[Optional[str]]
    state: Column(Enum(ItemStates))
    lastUse: DateTime(timezone=True), server_default=func.now()

    tags: Mapped[List["Tag"]] = relationship(
        back_populates="tag", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r}, description={self.description!r}, image={self.image!r}, state={self.state!r}, lastUse={self.lastUse!r})"
