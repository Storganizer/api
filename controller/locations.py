from model.location import Location as ModelLocation
from model.connection import engine, session

from sqlalchemy import select, text
from flask_restful import Resource, marshal_with
from flask import request
import json
import time


class Locations(Resource):
    def get(self):
      print(request.remote_addr)
      #time.sleep(2)
      locations = []
      for location in session.scalars(select(ModelLocation)):
        locations.append(location.getDataTransferObject())
      return locations, 200 # OK

    def post(self):
      try:
        location = json.loads(request.data)

        # Fail if name not set or name Empty
        if not 'name' in location.keys() or location['name'] == '':
          return {
            'error': True,
            'message': 'Name might not be empty'
          }, 400 # Bad Request

        if 'id' in location.keys() and location['id'] > 0:
          return {
            'error': True,
            'message': f'You cannot update location.id {location["id"]} by post, use put instead'
          }, 405 # Method not Allowed

        # {'classification': 1, 'description': 'Schlafzimmer', 'id': 0, 'name': 'Lorina'}
        locationDescription = location['description'] if 'description' in location.keys() else ''
        locationEntry = ModelLocation(
          name=location['name'],
          description=locationDescription,
          classification=location['classification']
        )
        session.add(locationEntry)
        session.commit()

        return {
          'error': False,
          'message': 'Location successfully stored'
        }, 201 # Created
      except Exception as e:
        return {
          'error': True,
          'message': f'Exception: {str(e)}'
        }, 400 # Bad Request

class Location(Resource):

    def get(self, id):
      location = session.query(ModelLocation).get(id)
      if location:
        return location.getDataTransferObject(["boxes"]), 200 # OK

      return {
        'error': True,
        'message': f'Location {id} not found'
      }, 404 # not found


    def delete(self, id):
      location = session.query(ModelLocation).get(id)
      if location:
        session.delete(location)
        session.commit()
        return {
          'error': False,
          'message': 'Location successfully deleted'
        }, 202 # accepted

      return {
        'error': True,
        'message': f'Location {id} not found'
      }, 404 # not found

    def put(self, id):
      try:
        location = json.loads(request.data)

        if not 'id' in location.keys():
          return {
            'error': True,
            'message': 'location.id not sent, not updating'
          }, 400 # Bad Request

        id = int(id)
        location['id'] = int(location['id'])

        # Fail if id is shady
        if id <= 0 or id != location['id']:
          return {
            'error': True,
            'message': 'location.id mismatch, not updating'
          }, 400 # Bad Request

        # Fail if name not set or name Empty
        if not 'name' in location.keys() or location['name'] == '':
          return {
            'error': True,
            'message': 'Name might not be empty'
          }, 400 # Bad Request

        if 'id' in location.keys() and location['id'] == 0:
          return {
            'error': True,
            'message': f'You cannot add location by put, use post instead'
          }, 405 # Method not Allowed

        locationEntry = session.query(ModelLocation).get(id)
        locationEntry.name = location['name']
        locationEntry.description = location['description']
        locationEntry.classification = location['classification']
        session.commit()

        return {
          'error': False,
          'message': 'Location successfully updated'
        }, 201 # Created
      except Exception as e:
        return {
          'error': True,
          'message': f'Exception: {str(e)}'
        }, 400 # Bad Request
