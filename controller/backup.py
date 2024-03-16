from model.location import Location as ModelLocation
from model.box import Box as ModelBox
from model.item import Item as ModelItem
from model.person import Person as ModelPerson
from model.connection import engine, session

import os
from sqlalchemy import select
from flask_restful import Resource
from flask import request, make_response
import json
import base64
import time

from pprint import pprint

class Backup(Resource):
    
    def get(self):
      locations = []
      for location in session.scalars(select(ModelLocation).order_by(ModelLocation.name)):
        locations.append(location.getDataTransferObject())

      boxes = []
      for box in session.scalars(select(ModelBox).order_by(ModelBox.name)):
        boxes.append(box.getDataTransferObject())
    
      items = []
      for item in session.scalars(select(ModelItem).order_by(ModelItem.name)):
        items.append(item.getDataTransferObject())

      persons = []
      for person in session.scalars(select(ModelPerson).order_by(ModelPerson.name)):
        persons.append(person.getDataTransferObject())


      allData = {
        "locations": locations,
        "boxes": boxes,
        "items": items
      }

      response = make_response(json.dumps(allData))
      response.headers['Content-Type'] = 'application/force-download'
      response.headers['Content-Disposition'] = 'attachment; filename=backup.json'
      response.status_code = 200

      return response



class Restore(Resource):

    def post(self):
      if 'backup' not in request.files:
          return 'No backup sent'
      uploadFile = request.files['backup']

      allElements = json.loads(uploadFile.read())
      keys = allElements.keys()


      if 'locations' in keys:
        for location in allElements['locations']:
          locationObject = ModelLocation(
            id = location['id'],
            name = location['name'],
            description = location['description'],
            image = location['image'],
            classification = location['classification']
          )
          session.add(locationObject)
          session.commit()


      if 'boxes' in keys:
       for box in allElements['boxes']:
         boxObject = ModelBox(
           id = box['id'],
           name = box['name'],
           description = box['description'],
           image = box['image'],
           #lastAccess = box['lastAccess'],
           locationId = box['locationId']
         )
         session.add(boxObject)
         session.commit()

      if 'items' in keys:
        for item in allElements['items']:
          itemObject = ModelItem(
            id = item['id'],
            amount = item['amount'],
            name = item['name'],
            description = item['description'],
            image = item['image'],
            #lastUsage = item['lastUsage'],
            #state = item['state'],
            boxId = item['boxId']
          )
          session.add(itemObject)
          session.commit()



      return "restore"
