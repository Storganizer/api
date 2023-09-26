#!/usr/bin/env python

from model.base import Base
from model.location import Location
from model.box import Box
from model.item import Item, Tag
from model.connection import engine, session

from sqlalchemy import text
from sqlalchemy.sql import func

from pprint import pprint
import yaml


# main loop
if __name__ == "__main__":
  


  print("start db setup")
  Base.metadata.create_all(bind=engine)
  print("db setup done")
 
  print("Truncate everything first / very sqlite specific")
  session.execute(text('''DELETE FROM location;'''))
  session.execute(text('''DELETE FROM box;'''))
  session.execute(text('''DELETE FROM item;'''))
  session.commit()
  session.execute(text('''VACUUM;'''))
  session.commit()


  print("start seeding data")
  airRaidShelter = Location(name="Luftschutzkeller", description="Luftschutzkeller - ungeheizt - nicht so gut belüftet", classification=1)
  cellar = Location(name="Naturkeller", description="Naturkeller - ungeheizt - gut belüftet", classification=3)

  session.add(airRaidShelter)
  session.add(cellar)
  session.commit()


  # add boxes and items from yaml
  with open('../../storganizer-data/yaml/stuff.yaml', 'r') as file:
    boxes = yaml.safe_load(file)

    for box in boxes['boxes']:
      box = boxes['boxes'][box]
      boxNotes = box['notes'] if 'notes' in box.keys() else ''
      boxEntry = Box(
        name=box['name'],
        description=boxNotes,
        lastAccess=func.now(),
        locationId=airRaidShelter.id
      )
      session.add(boxEntry)
      session.commit()
      
      items = []
      for item in box['items']:
        itemNotes = item['notes'] if 'notes' in item.keys() else ''
        
        itemEntry = Item(
          name=item['name'],
          amount=item['amount'],
          description=itemNotes,
          image="",
          state='stored',
          lastUsage=func.now(),
          box=boxEntry
        )
        session.add(itemEntry)
        session.commit()



  print("seeding data done")
