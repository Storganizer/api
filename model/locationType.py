from model.base import Base

from typing import List
from typing import Optional

from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, TEXT, DateTime
from sqlalchemy.orm import relationship

class LocationType(Base):

    __tablename__ = "location_type"

    dtoColumns = ["id", "name", "description", "len locations", "url /location_type/{id}"]

    id          = Column("id", Integer, primary_key=True, autoincrement=True)
    name        = Column("name", String)
    description = Column("description", TEXT)

    locations = relationship("Location", back_populates = "locationType")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r}, description={self.description!r})"
