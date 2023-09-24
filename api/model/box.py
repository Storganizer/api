from model.base import Base

from typing import List
from typing import Optional

from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, TEXT, DateTime


class Box(Base):

    __tablename__ = "box"

    dtoColumns = ["id", "name", "description"]


    id          = Column("id", Integer, primary_key=True)
    name        = Column("name", String)
    description = Column("description", TEXT)
    lastAccess  = Column("lastAccess", DateTime)
    locationId  = Column(
                      Integer,
                      ForeignKey('location.id', ondelete='CASCADE'),
                      nullable=True,
                      index=True
                  )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r}, description={self.description!r}, lastAccess={self.lastAccess!r})"
