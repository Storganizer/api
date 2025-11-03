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
from login import oidc_required, getCurrentPersonId, isOidcEnabled

class Boxes(Resource):
    @oidc_required
    def get(self):
      #time.sleep(8)

      boxes = []
      query = select(ModelBox).order_by(ModelBox.name)

      # If OIDC is enabled, filter by current user's personId
      if isOidcEnabled():
        personId = getCurrentPersonId()
        query = query.where(ModelBox.personId == personId)

      for box in session.scalars(query):
        boxes.append(box.getDataTransferObject(['parentLocationId']))
      session.commit()
      return boxes

    @oidc_required
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

        # Handle personId based on OIDC mode
        if isOidcEnabled():
          personId = getCurrentPersonId()
          # Validate that the sent personId matches the current user (if sent)
          if 'personId' in box and box['personId'] != personId:
            return {
              'error': True,
              'message': 'You can only create boxes for yourself'
            }, 403 # Forbidden
          boxPersonId = personId
        else:
          # In non-OIDC mode, use the personId from the request (or None)
          boxPersonId = box.get('personId', None)

        # {'classification': 1, 'description': 'Schlafzimmer', 'id': 0, 'name': 'Lorina'}
        boxDescription = box['description'] if 'description' in box.keys() else ''

        boxEntry = ModelBox(
          name=box['name'],
          description=boxDescription,
          personId=boxPersonId
        )


        if 'locationId' in box.keys():
          boxEntry.boxId = None
          boxEntry.locationId = box['locationId']

        if 'boxId' in box.keys():
          boxEntry.locationId = None
          boxEntry.boxId = box['boxId']

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
    @oidc_required
    def get(self, id):
      box = session.query(ModelBox).get(id)

      # If OIDC is enabled, verify ownership
      if isOidcEnabled() and box:
        personId = getCurrentPersonId()
        if box.personId != personId:
          return {
            'error': True,
            'message': 'Access denied'
          }, 403 # Forbidden

      session.commit()
      if box:
        return box.getDataTransferObject(['items', 'parentLocationId'])
      return {
        'error': True,
        'message': f'Box {id} not found'
      }, 404 # not found

    @oidc_required
    def delete(self, id):
      box = session.query(ModelBox).get(id)
      if box:
        # If OIDC is enabled, verify ownership
        if isOidcEnabled():
          personId = getCurrentPersonId()
          if box.personId != personId:
            return {
              'error': True,
              'message': 'You can only delete your own boxes'
            }, 403 # Forbidden

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

    @oidc_required
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

        if not boxEntry:
          return {
            'error': True,
            'message': f'Box {id} not found'
          }, 404 # not found

        # If OIDC is enabled, verify ownership
        if isOidcEnabled():
          personId = getCurrentPersonId()
          if boxEntry.personId != personId:
            return {
              'error': True,
              'message': 'You can only update your own boxes'
            }, 403 # Forbidden

          # Validate that the sent personId matches the current user (if sent)
          if 'personId' in box and box['personId'] != personId:
            return {
              'error': True,
              'message': 'You cannot change the owner of a box'
            }, 403 # Forbidden

        imageLink = False
        boxImage = box['image'] if 'image' in box.keys() else ''
        if boxImage and boxImage != '':
          with open(f'static/images/box-{ box["id"] }.png', 'wb') as image_file:
            image_file.write(base64.b64decode(boxImage))
            imageLink = f'/static/images/box-{ box["id"] }.png'


        boxEntry.name = box['name']
        if imageLink:
          boxEntry.image = imageLink
        boxEntry.description = box['description']
        if 'locationId' in box.keys():
          boxEntry.boxId = None
          boxEntry.locationId = box['locationId']

        if 'boxId' in box.keys():
          boxEntry.locationId = None
          boxEntry.boxId = box['boxId']

        if 'personId' in box.keys() and not isOidcEnabled():
          boxEntry.personId = box['personId']

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
