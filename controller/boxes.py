from model.box import Box as ModelBox
from model.connection import engine, session

import os
from sqlalchemy import select
from flask_restful import Resource
from flask import request
import json
import base64
import time

from pprint import pprint

class Boxes(Resource):
    def get(self):
      #time.sleep(8)

      boxes = []
      for box in session.scalars(select(ModelBox).order_by(ModelBox.name)):
        boxes.append(box.getDataTransferObject())
      session.commit()
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
        )

        if 'locationId' in box.keys():
          boxEntry.locationId=box['locationId']

        if 'personId' in box.keys():
          boxEntry.personId=box['personId']

        session.add(boxEntry)
        session.commit()

        # write picture after we know the database id
        boxImage = box['image'] if 'image' in box.keys() else ''
        if boxImage and boxImage != '':
          with open(f'static/images/box-{ boxEntry.id }.png', 'wb') as image_file:
            image_file.write(base64.b64decode(boxImage))
            boxEntry.image = f'/static/images/box-{ boxEntry.id }.png'
            session.commit()

        return {
          'error': False,
          'message': 'Box successfully stored'
        }, 201 # Created
      except Exception as e:
        pprint(e)
        raise e

        return {
          'error': True,
          'message': f'Exception: {str(e)}'
        }, 400 # Bad Request


class Box(Resource):
    def get(self, id):
      box = session.query(ModelBox).get(id)
      session.commit()
      if box:
        return box.getDataTransferObject(['items', 'location'])
      return {
        'error': True,
        'message': f'Box {id} not found'
      }, 404 # not found

    def delete(self, id):
      box = session.query(ModelBox).get(id)
      if box:
        session.delete(box)
        session.commit()

        if os.path.exists(f'static/images/box-{ id }.png'):
          os.remove(f'static/images/box-{ id }.png')

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


        imageLink = False
        boxImage = box['image'] if 'image' in box.keys() else ''
        if boxImage and boxImage != '':
          with open(f'static/images/box-{ box["id"] }.png', 'wb') as image_file:
            image_file.write(base64.b64decode(boxImage))
            imageLink = f'/static/images/box-{ box["id"] }.png'


        boxEntry = session.query(ModelBox).get(id)
        boxEntry.name = box['name']
        if imageLink:
          boxEntry.image = imageLink
        boxEntry.description = box['description']
        if 'locationId' in box.keys():
          boxEntry.locationId=box['locationId']

        if 'personId' in box.keys():
          boxEntry.personId=box['personId']

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
