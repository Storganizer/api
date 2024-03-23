from model.base import Base
from model.connection import engine, session

from typing import List
from typing import Optional

from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, TEXT, DateTime
from sqlalchemy.orm import relationship

class Box(Base):

    __tablename__ = "box"

    dtoColumns = ["id", "name", "description", "image", "locationId", "boxId", "personId", "len items", "url /box/{id}"]


    id          = Column("id", Integer, primary_key=True, autoincrement=True)
    name        = Column("name", String)
    description = Column("description", TEXT)
    image       = Column("image", String)
    lastAccess  = Column("lastAccess", DateTime)
    locationId  = Column(
                      Integer,
                      ForeignKey('location.id', ondelete='CASCADE'),
                      nullable=True,
                      index=True
                  )
    boxId  = Column(
                      Integer,
                      ForeignKey('box.id', ondelete='CASCADE'),
                      nullable=True,
                      index=True
                  )
    personId  = Column(
                      Integer,
                      ForeignKey('person.id', ondelete='CASCADE'),
                      nullable=True,
                      index=True
                  )

    items = relationship("Item", back_populates = "box")
    location = relationship("Location", back_populates = "boxes")
    person = relationship("Person", back_populates = "boxes")
    parentLocationId = 0

    def __repr__(self) -> str:
      return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r}, description={self.description!r}, image={self.image!r}, lastAccess={self.lastAccess!r})"

    def getDataTransferObject(self, additionalColumns: list = [], isRecursive: bool = False):
      self.parentLocationId = self.getLocationId()
      return super().getDataTransferObject(additionalColumns, isRecursive)

    def getLocationId(self) -> int:
      if self.locationId:
        return self.locationId

      if self.boxId:
        parentBox = session.query(Box).get(self.boxId)
        return parentBox.getLocationId()
