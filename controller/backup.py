from model.location import Location as ModelLocation
from model.box import Box as ModelBox
from model.item import Item as ModelItem
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

    def get(self):
      return "restore"