from model.base import Base
from model.box import Box

from typing import List

from sqlalchemy import Column, String, Integer, TEXT
from sqlalchemy.orm import Mapped, relationship


class Location(Base):

    __tablename__ = "location"
    dtoColumns = ["id", "name", "description", "image", "classification", "len boxes", "url http://localhost:5000/location/{id}"]


    id              = Column("id", Integer, primary_key=True)
    name            = Column("name", String)
    description     = Column("description", TEXT)
    image           = Column("image", String)
    classification  = Column("classification", Integer)

    boxes = relationship("Box", back_populates = "location")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r}, description={self.description!r}, image={self.image!r}, classification={self.classification!r})"
