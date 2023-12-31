from model.item import Item as ModelItem
from model.connection import engine, session

from sqlalchemy import select
from flask_restful import Resource
from flask import request
import json
import time


class Items(Resource):
    def get(self):
        #time.sleep(6)
        items = []
        for item in session.scalars(select(ModelItem)):
          items.append(item.getDataTransferObject())

        return items

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

        # {'classification': 1, 'description': 'Schlafzimmer', 'id': 0, 'name': 'Lorina'}
        itemDescription = item['description'] if 'description' in item.keys() else ''
        itemEntry = ModelItem(
          name=item['name'],
          description=itemDescription,
          amount=item['amount'],
          boxId=item['boxId']
        )
        session.add(itemEntry)
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
    def get(self, id):
      item = session.query(ModelItem).get(id)
      if item:
        return item.getDataTransferObject(['box'])

      return {
        'error': True,
        'message': f'Item {id} not found'
      }, 404 # not found


    def delete(self, id):
      item = session.query(ModelItem).get(id)
      if item:
        session.delete(item)
        session.commit()
        return {
          'error': False,
          'message': 'Item successfully deleted'
        }, 202 # accepted

      return {
        'error': True,
        'message': f'Item {id} not found'
      }, 404 # not found

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

        boxEntry = session.query(ModelItem).get(id)
        boxEntry.name = item['name']
        boxEntry.description = item['description']
        boxEntry.amount = item['amount']
        boxEntry.boxId = item['boxId']
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
