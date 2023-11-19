from model.base import Base

import enum
from typing import List
from typing import Optional

from sqlalchemy import Table, ForeignKey, Column, String, Integer, CHAR, TEXT, DateTime, Enum
from sqlalchemy.orm import relationship

association_table = Table(
    "item_tag",
    Base.metadata,
    Column("item_id", ForeignKey("item.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)


class Tag(Base):

    __tablename__ = "tag"

    id          = Column("id", Integer, primary_key=True)
    name        = Column("name", String)


class ItemStates(enum.Enum):
    stored = 1
    in_use = 2

class Item(Base):

    __tablename__ = "item"

    dtoColumns = ["id", "name", "image", "description", "boxId", "amount", "url http://10.1.10.79:5000/item/{id}"]


    id          = Column("id", Integer, primary_key=True)
    amount      = Column("amount", Integer)
    name        = Column("name", String)
    description = Column("description", TEXT)
    image       = Column("image", String)
    state       = Column("state", Enum(ItemStates))
    lastUsage   = Column("lastUsage", DateTime)
    boxId  = Column(
                      Integer,
                      ForeignKey('box.id', ondelete='CASCADE'),
                      nullable=True,
                      index=True
                  )
    box = relationship("Box", back_populates = "items")

    # tags = relationship(
    #     secondary=association_table
    # )


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r}, description={self.description!r}, image={self.image!r}, state={self.state!r}, lastUsage={self.lastUsage!r})"
