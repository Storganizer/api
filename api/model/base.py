from sqlalchemy.orm import DeclarativeBase

class DataTransferObject(object):
    pass


class Base(DeclarativeBase):
    
    dtoColumns = ["id"]
    
    def getDataTransferObject(self) -> object:
        dto = DataTransferObject()

        for dtoColumn in self.dtoColumns:
            setattr(dto, dtoColumn, getattr(self, dtoColumn))

        return dto.__dict__
