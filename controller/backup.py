from model.locationType import LocationType as ModelLocationType
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


class Backup(Resource):
    
    def get(self):
      locationTypes = []
      for locationType in session.scalars(select(ModelLocationType).order_by(ModelLocationType.id)):
        locationTypes.append(locationType.getDataTransferObject())

      locations = []
      for location in session.scalars(select(ModelLocation).order_by(ModelLocation.id)):
        locations.append(location.getDataTransferObject())


      boxes = []
      for box in session.scalars(select(ModelBox).order_by(ModelBox.id)):
        boxes.append(box.getDataTransferObject())
    
      items = []
      for item in session.scalars(select(ModelItem).order_by(ModelItem.id)):
        items.append(item.getDataTransferObject())

      persons = []
      for person in session.scalars(select(ModelPerson).order_by(ModelPerson.id)):
        persons.append(person.getDataTransferObject())

      allData = {
        "locationTypes": locationTypes,
        "locations": locations,
        "persons": persons,
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


      session.query(ModelLocationType).delete()
      session.commit()

      session.query(ModelLocation).delete()
      session.commit()

      session.query(ModelPerson).delete()
      session.commit()

      session.query(ModelBox).delete()
      session.commit()

      session.query(ModelItem).delete()
      session.commit()

      if 'locationTypes' in keys:
        for locationType in allElements['locationTypes']:
          locationTypeObject = ModelLocationType(
            id = locationType['id'],
            name = locationType['name'],
            description = locationType['description']
          )
          session.add(locationTypeObject)
          session.commit()


      if 'locations' in keys:
        for location in allElements['locations']:
          locationObject = ModelLocation(
            id = location['id'],
            name = location['name'],
            description = location['description'],
            image = location['image'],
          )
          session.add(locationObject)
          session.commit()

      if 'persons' in keys:
        for person in allElements['persons']:
          personObject = ModelPerson(
            id = person['id'],
            name = person['name'],
            description = person['description'],
            image = person['image'],
          )
          session.add(personObject)
          session.commit()


      if 'boxes' in keys:
       for box in allElements['boxes']:
         boxObject = ModelBox(
           id = box['id'],
           name = box['name'],
           description = box['description'],
           image = box['image'],
           boxId = box['boxId'],
           locationId = box['locationId'],
           personId = box['personId']
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
