from model.base import Base

from typing import List
from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Location(Base):
    
    __tablename__ = "location"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    image: Mapped[Optional[str]]
    classification: Mapped[int]

    boxes: Mapped[List["Box"]] = relationship(
        back_populates="box", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r}, description={self.description!r}, image={self.image!r}, classification={self.classification!r})"
