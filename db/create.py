#!/usr/bin/env python

import sys
import os

# Add parent directory to path to import from api module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

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
