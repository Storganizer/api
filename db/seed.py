#!/usr/bin/env python

import sys
import os

# Add parent directory to path to import from api module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from model.base import Base
from model.location import Location
from model.box import Box
from model.person import Person
from model.item import Item, Tag
from model.connection import engine, session

from sqlalchemy import text


# main loop
if __name__ == "__main__":
  # print("Truncate everything first / very sqlite specific")
  # session.execute(text('''DELETE FROM location;'''))
  # session.commit()
  # session.execute(text('''VACUUM;'''))
  # session.commit()

  print("start seeding data")
  airRaidShelter = Location(name="Luftschutzkeller", description="Luftschutzkeller - ungeheizt - nicht so gut belüftet", classification=1)
  cellar = Location(name="Naturkeller", description="Naturkeller - ungeheizt - gut belüftet", classification=3)

  session.add(airRaidShelter)
  session.add(cellar)
  session.commit()

  print("seeding data done")
