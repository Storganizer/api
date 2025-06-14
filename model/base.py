from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.collections import InstrumentedList
from flask_restful import marshal
from pprint import pprint
import socket


class DataTransferObject(object):
    pass


class Base(DeclarativeBase):
    schema = None
    dtoColumns = ["id"]

    def getDataTransferObject(self, additionalColumns: list = [], isRecursive: bool = False) -> object:

        hostname = socket.gethostname()

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
                        dtoColumn = dtoColumn.replace("{id}", str(getattr(self, "id")))
                        dtoColumn = dtoColumn.replace("{host}", socket.gethostname())
                        setattr(dto, func, dtoColumn)
                    case _:
                        pass

            else:
                attribute = getattr(self, dtoColumn)
                # children elements
                if type(attribute) is InstrumentedList:
                    items = []
                    for item in attribute:
                        if not isRecursive and isinstance(item, Base) and hasattr(item, 'getDataTransferObject'):
                            items.append(item.getDataTransferObject(isRecursive = True))

                    attribute = items

                if not isRecursive and isinstance(attribute, Base) and hasattr(attribute, 'getDataTransferObject'):
                     attribute = attribute.getDataTransferObject(isRecursive = True)



                if not isinstance(attribute, Base) and not hasattr(attribute, 'getDataTransferObject'):
                    setattr(dto, dtoColumn, attribute)


        dictionary = dto.__dict__

        if self.__tablename__ != "location_type" and not dictionary['image']:
            dictionary['image'] = f'/static/images/_default-{self.__tablename__}.jpg'
        return dto.__dict__
