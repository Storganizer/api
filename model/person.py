from model.base import Base

from typing import List
from typing import Optional

from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, TEXT, DateTime
from sqlalchemy.orm import relationship

class Person(Base):

    __tablename__ = "person"

    #dtoColumns = ["id", "name", "description", "len items", "items"]
    dtoColumns = ["id", "name", "url /person/{id}"]


    id          = Column("id", Integer, primary_key=True, autoincrement=True)
    name        = Column("name", String)


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r})"
