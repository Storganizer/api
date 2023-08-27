from model.base import Base

from typing import List
from typing import Optional

from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, TEXT

from sqlalchemy.orm import relationship


class Location(Base):
    
    __tablename__ = "location"
    
    id              = Column("id", Integer, primary_key=True)
    name            = Column("name", String)
    description     = Column("description", TEXT)
    image           = Column("image", String)
    classification  = Column("classification", Integer)

    #boxes: Mapped[List["Box"]] = relationship(
    #    back_populates="box", cascade="all, delete-orphan"
    #)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r}, description={self.description!r}, image={self.image!r}, classification={self.classification!r})"
