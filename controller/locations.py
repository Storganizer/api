from model.location import Location as ModelLocation
from model.connection import engine, session

import os
from sqlalchemy import select, text
from flask_restful import Resource, marshal_with
from flask import request
import json
import base64
import time


class Locations(Resource):
    def get(self):
      print(request.remote_addr)
      #time.sleep(2)
      locations = []
      for location in session.scalars(select(ModelLocation).order_by(ModelLocation.name)):
        locations.append(location.getDataTransferObject())
      session.commit()
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

        # {'locationTypeId': 1, 'description': 'Schlafzimmer', 'id': 0, 'name': 'Lorina'}
        locationDescription = location['description'] if 'description' in location.keys() else ''
        locationTypeId = location['locationType'] if location['locationType'] > 0 else None
        locationEntry = ModelLocation(
          name=location['name'],
          description=locationDescription,
          locationTypeId=locationTypeId
        )
        session.add(locationEntry)
        session.commit()

        # write picture after we know the database id
        image = location['image'] if 'image' in location.keys() else ''
        if image and image != '':
          with open(f'static/images/location-{ locationEntry.id }.png', 'wb') as image_file:
            image_file.write(base64.b64decode(image))
            locationEntry.image = f'/static/images/location-{ locationEntry.id }.png'
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
      session.commit()
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

        if os.path.exists(f'static/images/location-{ id }.png'):
          os.remove(f'static/images/location-{ id }.png')


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

        imageLink = False
        image = location['image'] if 'image' in location.keys() else ''
        if image and image != '':
          with open(f'static/images/location-{ location["id"] }.png', 'wb') as image_file:
            image_file.write(base64.b64decode(image))
            imageLink = f'/static/images/location-{ location["id"] }.png'

        locationEntry = session.query(ModelLocation).get(id)
        locationEntry.name = location['name']
        if imageLink:
          locationEntry.image = imageLink
        locationEntry.description = location['description']
        locationTypeId = location['locationType'] if location['locationType'] > 0 else None

        locationEntry.locationTypeId = locationTypeId
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
