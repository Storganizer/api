from model.item import Item as ModelItem
from model.connection import engine, session
from login import oidc_required, getCurrentPersonId, isOidcEnabled

import os
from sqlalchemy import select
from flask_restful import Resource
from flask import request
import json
import base64
import time


class Items(Resource):
    @oidc_required
    def get(self):
        #time.sleep(6)
        items = []
        query = select(ModelItem).order_by(ModelItem.name)

        # Filter by personId if OIDC is enabled
        if isOidcEnabled():
            personId = getCurrentPersonId()
            query = query.where(ModelItem.personId == personId)

        for item in session.scalars(query):
          items.append(item.getDataTransferObject())
        session.commit()

        return items

    @oidc_required
    def post(self):
      try:
        item = json.loads(request.data)

        # Fail if name not set or name Empty
        if not 'name' in item.keys() or item['name'] == '':
          return {
            'error': True,
            'message': 'Name might not be empty'
          }, 400 # Bad Request

        if 'id' in item.keys() and item['id'] > 0:
          return {
            'error': True,
            'message': f'You cannot update item.id {item["id"]} by post, use put instead'
          }, 405 # Method not Allowed

        # Set personId in OIDC mode, validate in OIDC mode
        if isOidcEnabled():
            personId = getCurrentPersonId()
            if 'personId' in item.keys() and item['personId'] != personId:
                return {
                    'error': True,
                    'message': 'You can only create items for yourself'
                }, 403 # Forbidden
            item['personId'] = personId

        # {'classification': 1, 'description': 'Schlafzimmer', 'id': 0, 'name': 'Lorina'}
        itemDescription = item['description'] if 'description' in item.keys() else ''
        itemEntry = ModelItem(
          name=item['name'],
          description=itemDescription,
          amount=item['amount'],
          boxId=item['boxId'],
          personId=item.get('personId')
        )
        session.add(itemEntry)
        session.commit()

        # write picture after we know the database id
        itemImage = item['image'] if 'image' in item.keys() else ''
        if itemImage and itemImage != '':
          with open(f'static/images/item-{ itemEntry.id }.png', 'wb') as image_file:
            image_file.write(base64.b64decode(itemImage))
            itemEntry.image = f'/static/images/item-{ itemEntry.id }.png'
            session.commit()


        return {
          'error': False,
          'message': 'Item successfully stored'
        }, 201 # Created
      except Exception as e:
        return {
          'error': True,
          'message': f'Exception: {str(e)}'
        }, 400 # Bad Request


class Item(Resource):
    @oidc_required
    def get(self, id):
      item = session.query(ModelItem).get(id)

      # Verify ownership in OIDC mode
      if item and isOidcEnabled():
          personId = getCurrentPersonId()
          if item.personId != personId:
              return {
                  'error': True,
                  'message': f'Item {id} not found'
              }, 404 # not found

      session.commit()
      if item:
        return item.getDataTransferObject(['box'])

      return {
        'error': True,
        'message': f'Item {id} not found'
      }, 404 # not found


    @oidc_required
    def delete(self, id):
      item = session.query(ModelItem).get(id)

      # Verify ownership in OIDC mode
      if item and isOidcEnabled():
          personId = getCurrentPersonId()
          if item.personId != personId:
              return {
                  'error': True,
                  'message': f'Item {id} not found'
              }, 404 # not found

      if item:
        session.delete(item)
        session.commit()

        if os.path.exists(f'static/images/item-{ id }.png'):
          os.remove(f'static/images/item-{ id }.png')

        return {
          'error': False,
          'message': 'Item successfully deleted'
        }, 202 # accepted

      return {
        'error': True,
        'message': f'Item {id} not found'
      }, 404 # not found

    @oidc_required
    def put(self, id):
      try:
        item = json.loads(request.data)

        if not 'id' in item.keys():
          return {
            'error': True,
            'message': 'item.id not sent, not updating'
          }, 400 # Bad Request

        id = int(id)
        item['id'] = int(item['id'])

        # Fail if id is shady
        if id <= 0 or id != item['id']:
          return {
            'error': True,
            'message': 'item.id mismatch, not updating'
          }, 400 # Bad Request

        # Fail if name not set or name Empty
        if not 'name' in item.keys() or item['name'] == '':
          return {
            'error': True,
            'message': 'Name might not be empty'
          }, 400 # Bad Request

        if 'id' in item.keys() and item['id'] == 0:
          return {
            'error': True,
            'message': f'You cannot add item by put, use post instead'
          }, 405 # Method not Allowed

        itemEntry = session.query(ModelItem).get(id)

        # Verify ownership in OIDC mode
        if itemEntry and isOidcEnabled():
            personId = getCurrentPersonId()
            if itemEntry.personId != personId:
                return {
                    'error': True,
                    'message': f'Item {id} not found'
                }, 404 # not found

            # Validate personId if provided
            if 'personId' in item.keys() and item['personId'] != personId:
                return {
                    'error': True,
                    'message': 'You cannot change item ownership'
                }, 403 # Forbidden

        imageLink = False
        itemImage = item['image'] if 'image' in item.keys() else ''
        if itemImage and itemImage != '':
          with open(f'static/images/item-{ item["id"] }.png', 'wb') as image_file:
            image_file.write(base64.b64decode(itemImage))
            imageLink = f'/static/images/item-{ item["id"] }.png'

        itemEntry.name = item['name']
        if imageLink:
          itemEntry.image = imageLink
        itemEntry.description = item['description']
        itemEntry.amount = item['amount']
        itemEntry.boxId = item['boxId']
        session.commit()

        return {
          'error': False,
          'message': 'Item successfully updated'
        }, 201 # Created
      except Exception as e:
        return {
          'error': True,
          'message': f'Exception: {str(e)}'
        }, 400 # Bad Request
