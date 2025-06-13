from model.locationType import LocationType as ModelLocationType
from model.connection import engine, session

import os
from sqlalchemy import select, text
from flask_restful import Resource, marshal_with
from flask import request
import json
import base64
import time


class LocationTypes(Resource):
    def get(self):
      print(request.remote_addr)
      #time.sleep(2)
      locationTypes = []
      for locationType in session.scalars(select(ModelLocationType).order_by(ModelLocationType.name)):
        locationTypes.append(location.getDataTransferObject())
      session.commit()
      return locationTypes, 200 # OK

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

        # {'classification': 1, 'description': 'Schlafzimmer', 'id': 0, 'name': 'Lorina'}
        locationTypeDescription = locationType['description'] if 'description' in locationType.keys() else ''
        locationTypeEntry = ModelLocationType(
          name=locationType['name'],
          description=locationTypeDescription
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

    def get(self, id):
      locationType = session.query(ModelLocationType).get(id)
      session.commit()
      if locationType:
        return locationType.getDataTransferObject(["locations"]), 200 # OK

      return {
        'error': True,
        'message': f'LocationType {id} not found'
      }, 404 # not found


    def delete(self, id):
      locationType = session.query(ModelLocationType).get(id)
      if locationType:
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
