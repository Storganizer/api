from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.collections import InstrumentedList
from flask_restful import marshal
from pprint import pprint

class DataTransferObject(object):
    pass


class Base(DeclarativeBase):
    schema = None
    dtoColumns = ["id"]
    
    def getDataTransferObject(self, additionalColumns: list = []) -> object:
        dto = DataTransferObject()
        self.dtoColumns =  self.dtoColumns + additionalColumns
        for dtoColumn in self.dtoColumns:

            if " " in dtoColumn:
                parts = dtoColumn.split()
                func = parts[0]
                parts.remove(parts[0])
                dtoColumn = " ".join(parts)
                #dtoColumn = parts[1]

                match func:
                    case "len":
                        setattr(dto, func + dtoColumn.capitalize(), len(getattr(self, dtoColumn)))
                    case "url":
                        #setattr(dto, func, dtoColumn.format(getattr(self, "id")))
                        id = 2
                        setattr(dto, func, dtoColumn.replace("{id}", str(getattr(self, "id"))))
                    case _:
                        pass

            else:
                attribute = getattr(self, dtoColumn)

                if type(attribute) is InstrumentedList:

                    items = []
                    for item in attribute:
                        if hasattr(item, 'getDataTransferObject'):
                            items.append(item.getDataTransferObject())

                    attribute = items

                if isinstance(attribute, object) and hasattr(attribute, 'getDataTransferObject'):
                    attribute = attribute.getDataTransferObject()


                setattr(dto, dtoColumn, attribute)


        return dto.__dict__
