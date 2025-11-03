from model.locationType import LocationType as ModelLocationType
from model.connection import engine, session

import os
from sqlalchemy import select, text
from flask_restful import Resource, marshal_with
from flask import request
import json
import base64
import time

from login import oidc_required, getCurrentPersonId, isOidcEnabled


class LocationTypes(Resource):
    @oidc_required
    def get(self):
      print(request.remote_addr)
      #time.sleep(2)
      locationTypes = []
      query = select(ModelLocationType).order_by(ModelLocationType.name)

      # If OIDC is enabled, filter by current user's personId
      if isOidcEnabled():
        personId = getCurrentPersonId()
        query = query.where(ModelLocationType.personId == personId)

      for locationType in session.scalars(query):
        locationTypes.append(locationType.getDataTransferObject())
      session.commit()
      return locationTypes, 200 # OK

    @oidc_required
    def post(self):
      try:
        locationType = json.loads(request.data)

        # Fail if name not set or name Empty
        if not 'name' in locationType.keys() or locationType['name'] == '':
          return {
            'error': True,
            'message': 'Name might not be empty'
          }, 400 # Bad Request

        if 'id' in locationType.keys() and locationType['id'] > 0:
          return {
            'error': True,
            'message': f'You cannot update locationType.id {locationType["id"]} by post, use put instead'
          }, 405 # Method not Allowed

        # Handle personId based on OIDC mode
        if isOidcEnabled():
          personId = getCurrentPersonId()
          # Validate that the sent personId matches the current user (if sent)
          if 'personId' in locationType and locationType['personId'] != personId:
            return {
              'error': True,
              'message': 'You can only create location types for yourself'
            }, 403 # Forbidden
          locationTypePersonId = personId
        else:
          # In non-OIDC mode, use the personId from the request (or None)
          locationTypePersonId = locationType.get('personId', None)

        # {'classification': 1, 'description': 'Schlafzimmer', 'id': 0, 'name': 'Lorina'}
        locationTypeDescription = locationType['description'] if 'description' in locationType.keys() else ''
        locationTypeEntry = ModelLocationType(
          name=locationType['name'],
          description=locationTypeDescription,
          personId=locationTypePersonId
        )
        session.add(locationTypeEntry)
        session.commit()

        return {
          'error': False,
          'message': 'LocationType successfully stored'
        }, 201 # Created
      except Exception as e:
        return {
          'error': True,
          'message': f'Exception: {str(e)}'
        }, 400 # Bad Request

class LocationType(Resource):

    @oidc_required
    def get(self, id):
      locationType = session.query(ModelLocationType).get(id)

      # If OIDC is enabled, verify ownership
      if isOidcEnabled() and locationType:
        personId = getCurrentPersonId()
        if locationType.personId != personId:
          return {
            'error': True,
            'message': 'Access denied'
          }, 403 # Forbidden

      session.commit()
      if locationType:
        return locationType.getDataTransferObject(["locations"]), 200 # OK

      return {
        'error': True,
        'message': f'LocationType {id} not found'
      }, 404 # not found


    @oidc_required
    def delete(self, id):
      locationType = session.query(ModelLocationType).get(id)
      if locationType:
        # If OIDC is enabled, verify ownership
        if isOidcEnabled():
          personId = getCurrentPersonId()
          if locationType.personId != personId:
            return {
              'error': True,
              'message': 'You can only delete your own location types'
            }, 403 # Forbidden

        session.delete(locationType)
        session.commit()

        return {
          'error': False,
          'message': 'LocationType successfully deleted'
        }, 202 # accepted

      return {
        'error': True,
        'message': f'LocationType {id} not found'
      }, 404 # not found

    @oidc_required
    def put(self, id):
      try:
        locationType = json.loads(request.data)

        if not 'id' in locationType.keys():
          return {
            'error': True,
            'message': 'locationType.id not sent, not updating'
          }, 400 # Bad Request

        id = int(id)
        locationType['id'] = int(locationType['id'])

        # Fail if id is shady
        if id <= 0 or id != locationType['id']:
          return {
            'error': True,
            'message': 'locationType.id mismatch, not updating'
          }, 400 # Bad Request

        # Fail if name not set or name Empty
        if not 'name' in locationType.keys() or locationType['name'] == '':
          return {
            'error': True,
            'message': 'Name might not be empty'
          }, 400 # Bad Request

        if 'id' in locationType.keys() and locationType['id'] == 0:
          return {
            'error': True,
            'message': f'You cannot add locationType by put, use post instead'
          }, 405 # Method not Allowed

        locationTypeEntry = session.query(ModelLocationType).get(id)

        if not locationTypeEntry:
          return {
            'error': True,
            'message': f'LocationType {id} not found'
          }, 404 # not found

        # If OIDC is enabled, verify ownership
        if isOidcEnabled():
          personId = getCurrentPersonId()
          if locationTypeEntry.personId != personId:
            return {
              'error': True,
              'message': 'You can only update your own location types'
            }, 403 # Forbidden

          # Validate that the sent personId matches the current user (if sent)
          if 'personId' in locationType and locationType['personId'] != personId:
            return {
              'error': True,
              'message': 'You cannot change the owner of a location type'
            }, 403 # Forbidden

        locationTypeEntry.name = locationType['name']
        locationTypeEntry.description = locationType['description']
        session.commit()

        return {
          'error': False,
          'message': 'LocationType successfully updated'
        }, 201 # Created
      except Exception as e:
        return {
          'error': True,
          'message': f'Exception: {str(e)}'
        }, 400 # Bad Request
