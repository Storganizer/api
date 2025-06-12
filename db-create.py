#!/usr/bin/env python

import sys

from model.base import Base
from model.location import Location
from model.locationType import LocationType
from model.box import Box
from model.person import Person
from model.item import Item, Tag
from model.connection import engine, session

from sqlalchemy import text

# main loop
if __name__ == "__main__":
  print("start db setup")
  Base.metadata.create_all(bind=engine)
  print("db setup done")

  sys.exit(0)
