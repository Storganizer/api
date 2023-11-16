from model.base import Base

from typing import List
from typing import Optional

from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, TEXT, DateTime
from sqlalchemy.orm import relationship

class Box(Base):

    __tablename__ = "box"

    #dtoColumns = ["id", "name", "description", "len items", "items"]
    dtoColumns = ["id", "name", "description", "image", "locationId", "len items", "url /box/{id}"]


    id          = Column("id", Integer, primary_key=True)
    name        = Column("name", String)
    description = Column("description", TEXT)
    image = Column("image", TEXT)
    lastAccess  = Column("lastAccess", DateTime)
    locationId  = Column(
                      Integer,
                      ForeignKey('location.id', ondelete='CASCADE'),
                      nullable=True,
                      index=True
                  )
    items = relationship("Item", back_populates = "box")
    location = relationship("Location", back_populates = "boxes")



    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r}, description={self.description!r}, image={self.image!r}, lastAccess={self.lastAccess!r})"
