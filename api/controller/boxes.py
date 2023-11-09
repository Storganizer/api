from model.box import Box as ModelBox
from model.connection import engine, session

from sqlalchemy import select
from flask_restful import Resource
from flask import request
import json

import time



class Boxes(Resource):
    def get(self):
      time.sleep(4)

      boxes = []
      for box in session.scalars(select(ModelBox)):
        boxes.append(box.getDataTransferObject())

      return boxes

    def post(self):
      try:
        box = json.loads(request.data)

        # Fail if name not set or name Empty
        if not 'name' in box.keys() or box['name'] == '':
          return {
            'error': True,
            'message': 'Name might not be empty'
          }, 400 # Bad Request

        if 'id' in box.keys() and box['id'] > 0:
          return {
            'error': True,
            'message': f'You cannot update box.id {box["id"]} by post, use put instead'
          }, 405 # Method not Allowed

        # {'classification': 1, 'description': 'Schlafzimmer', 'id': 0, 'name': 'Lorina'}
        boxDescription = box['description'] if 'description' in box.keys() else ''
        boxEntry = ModelBox(
          name=box['name'],
          description=boxDescription,
          locationId=box['locationId']
        )
        session.add(boxEntry)
        session.commit()

        return {
          'error': False,
          'message': 'Box successfully stored'
        }, 201 # Created
      except Exception as e:
        return {
          'error': True,
          'message': f'Exception: {str(e)}'
        }, 400 # Bad Request


class Box(Resource):
    def get(self, id):
        box = session.query(ModelBox).get(id)
        if box:
          return box.getDataTransferObject(['items', 'location'])

        return ["Box not found"]


    def delete(self, id):
      box = session.query(ModelBox).get(id)
      if box:
        session.delete(box)
        session.commit()
        return {
          'error': False,
          'message': 'Box successfully deleted'
        }, 202 # accepted

      return {
        'error': True,
        'message': f'Box {id} not found'
      }, 404 # not found

    def put(self, id):
      try:
        box = json.loads(request.data)

        if not 'id' in box.keys():
          return {
            'error': True,
            'message': 'box.id not sent, not updating'
          }, 400 # Bad Request

        id = int(id)
        box['id'] = int(box['id'])

        # Fail if id is shady
        if id <= 0 or id != box['id']:
          return {
            'error': True,
            'message': 'box.id mismatch, not updating'
          }, 400 # Bad Request

        # Fail if name not set or name Empty
        if not 'name' in box.keys() or box['name'] == '':
          return {
            'error': True,
            'message': 'Name might not be empty'
          }, 400 # Bad Request

        if 'id' in box.keys() and box['id'] == 0:
          return {
            'error': True,
            'message': f'You cannot add box by put, use post instead'
          }, 405 # Method not Allowed

        boxEntry = session.query(ModelBox).get(id)
        boxEntry.name = box['name']
        boxEntry.description = box['description']
        boxEntry.locationId = box['locationId']
        session.commit()

        return {
          'error': False,
          'message': 'Box successfully updated'
        }, 201 # Created
      except Exception as e:
        return {
          'error': True,
          'message': f'Exception: {str(e)}'
        }, 400 # Bad Request
