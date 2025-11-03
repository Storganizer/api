from model.location import Location as ModelLocation
from model.connection import engine, session

import os
from sqlalchemy import select, text
from flask_restful import Resource, marshal_with
from flask import request
import json
import base64
import time

from login import oidc_required, getCurrentPersonId, isOidcEnabled


class Locations(Resource):
    
    @oidc_required
    def get(self):
      print(request.remote_addr)
      #time.sleep(2)
      locations = []
      query = select(ModelLocation).order_by(ModelLocation.name)

      # If OIDC is enabled, filter by current user's personId
      if isOidcEnabled():
        personId = getCurrentPersonId()
        query = query.where(ModelLocation.personId == personId)

      for location in session.scalars(query):
        locations.append(location.getDataTransferObject())
      session.commit()
      return locations, 200 # OK

    @oidc_required
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

        # Handle personId based on OIDC mode
        if isOidcEnabled():
          personId = getCurrentPersonId()
          # Validate that the sent personId matches the current user (if sent)
          if 'personId' in location and location['personId'] != personId:
            return {
              'error': True,
              'message': 'You can only create locations for yourself'
            }, 403 # Forbidden
          locationPersonId = personId
        else:
          # In non-OIDC mode, use the personId from the request (or None)
          locationPersonId = location.get('personId', None)

        locationEntry = ModelLocation(
          name=location['name'],
          description=locationDescription,
          locationTypeId=locationTypeId,
          personId=locationPersonId
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

    @oidc_required
    def get(self, id):
      location = session.query(ModelLocation).get(id)

      # If OIDC is enabled, verify ownership
      if isOidcEnabled() and location:
        personId = getCurrentPersonId()
        if location.personId != personId:
          return {
            'error': True,
            'message': 'Access denied'
          }, 403 # Forbidden

      session.commit()
      if location:
        return location.getDataTransferObject(["boxes"]), 200 # OK

      return {
        'error': True,
        'message': f'Location {id} not found'
      }, 404 # not found


    @oidc_required
    def delete(self, id):
      location = session.query(ModelLocation).get(id)

      if location:
        # If OIDC is enabled, verify ownership
        if isOidcEnabled():
          personId = getCurrentPersonId()
          if location.personId != personId:
            return {
              'error': True,
              'message': 'You can only delete your own locations'
            }, 403 # Forbidden

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

    @oidc_required
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

        if not locationEntry:
          return {
            'error': True,
            'message': f'Location {id} not found'
          }, 404 # not found

        # If OIDC is enabled, verify ownership
        if isOidcEnabled():
          personId = getCurrentPersonId()
          if locationEntry.personId != personId:
            return {
              'error': True,
              'message': 'You can only update your own locations'
            }, 403 # Forbidden

          # Validate that the sent personId matches the current user (if sent)
          if 'personId' in location and location['personId'] != personId:
            return {
              'error': True,
              'message': 'You cannot change the owner of a location'
            }, 403 # Forbidden

        imageLink = False
        image = location['image'] if 'image' in location.keys() else ''
        if image and image != '':
          with open(f'static/images/location-{ location["id"] }.png', 'wb') as image_file:
            image_file.write(base64.b64decode(image))
            imageLink = f'/static/images/location-{ location["id"] }.png'

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
