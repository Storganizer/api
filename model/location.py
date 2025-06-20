from model.base import Base
from model.box import Box
from model.locationType import LocationType

from typing import List

from sqlalchemy import ForeignKey, Column, String, Integer, TEXT
from sqlalchemy.orm import Mapped, relationship


class Location(Base):

    __tablename__ = "location"
    dtoColumns = ["id", "name", "description", "image", "locationTypeId", "len boxes", "url /location/{id}"]

    id              = Column("id", Integer, primary_key=True, autoincrement=True)
    name            = Column("name", String)
    description     = Column("description", TEXT)
    image           = Column("image", String)

    locationTypeId  = Column(
                      Integer,
                      ForeignKey('location_type.id', ondelete='CASCADE'),
                      nullable=True,
                      index=True
                  )

    boxes = relationship("Box", back_populates = "location")
    locationType = relationship("LocationType", back_populates = "locations")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r}, description={self.description!r}, image={self.image!r})"
