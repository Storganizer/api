from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.collections import InstrumentedList
from flask_restful import marshal
from pprint import pprint

class DataTransferObject(object):
    pass


class Base(DeclarativeBase):
    schema = None
    dtoColumns = ["id"]
    
    def getDataTransferObject(self) -> object:
        dto = DataTransferObject()

        for dtoColumn in self.dtoColumns:

            if " " in dtoColumn:
                parts = dtoColumn.split()
                func = parts[0]
                dtoColumn = parts[1]

                match func:
                    case "len":
                        setattr(dto, func + dtoColumn.capitalize(), len(getattr(self, dtoColumn)))
                    case _:
                        pass
            else:
                attribute = getattr(self, dtoColumn)

                if type(attribute) is InstrumentedList:

                    items = []
                    for item in attribute:
                        items.append(item.getDataTransferObject())

                    attribute = items

                setattr(dto, dtoColumn, attribute)

                #print("Get Type of" + dtoColumn)
                #pprint(type(getattr(self, dtoColumn)))


        return dto.__dict__
