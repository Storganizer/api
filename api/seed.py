#!/usr/bin/env python

from model.base import Base
from model.location import Location
from model.box import Box
#from model.item import item
from model.connection import engine, session

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session



# main loop
if __name__ == "__main__":
  print("start db setup")
  Base.metadata.create_all(bind=engine)
  print("db setup done")

  print("start seeding data")

  session.execute(text('''DELETE FROM location;'''))
  session.commit()
  session.execute(text('''VACUUM;'''))
  session.commit()

  airRaidShelter = Location(name="Luftschutzkeller", description="Luftschutzkeller", classification=1)
  
  session.add(airRaidShelter)   
  session.commit()

  print("seeding data done")