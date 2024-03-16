from model.person import Person as ModelPerson
from model.connection import engine, session

import os
from sqlalchemy import select
from flask_restful import Resource
from flask import request
import json
import base64
import time


class Persons(Resource):
    def get(self):
        #time.sleep(6)
        persons = []
        for person in session.scalars(select(ModelPerson).order_by(ModelPerson.name)):
          persons.append(person.getDataTransferObject())
        session.commit()

        return persons

    def post(self):
      try:
        person = json.loads(request.data)

        # Fail if name not set or name Empty
        if 'name' not in person.keys() or person['name'] == '':
          return {
            'error': True,
            'message': 'Name might not be empty'
          }, 400 # Bad Request

        if 'id' in person.keys() and person['id'] > 0:
          return {
            'error': True,
            'message': f'You cannot update person.id {person["id"]} by post, use put instead'
          }, 405 # Method not Allowed

        description = person['description'] if 'description' in person.keys() else ''

        entry = ModelPerson(
          name=person['name'],
          description=description,
        )
        session.add(entry)
        session.commit()

        # write picture after we know the database id
        image = person['image'] if 'image' in person.keys() else ''
        if image and image != '':
          with open(f'static/images/person-{ entry.id }.png', 'wb') as image_file:
            image_file.write(base64.b64decode(image))
            entry.image = f'/static/images/person-{ entry.id }.png'
            session.commit()

        return {
          'error': False,
          'message': 'Person successfully stored'
        }, 201 # Created
      except Exception as e:
        return {
          'error': True,
          'message': f'Exception: {str(e)}'
        }, 400 # Bad Request


class Person(Resource):
    def get(self, id):
      person = session.query(ModelPerson).get(id)
      session.commit()
      if person:
        return person.getDataTransferObject()

      return {
        'error': True,
        'message': f'Person {id} not found'
      }, 404 # not found

    def delete(self, id):
      person = session.query(ModelPerson).get(id)
      if person:
        session.delete(person)
        session.commit()

        if os.path.exists(f'static/images/person-{ id }.png'):
          os.remove(f'static/images/person-{ id }.png')

        return {
          'error': False,
          'message': 'Person successfully deleted'
        }, 202 # accepted

      return {
        'error': True,
        'message': f'Person {id} not found'
      }, 404 # not found

    def put(self, id):
      try:
        person = json.loads(request.data)

        if 'id' not in person.keys():
          return {
            'error': True,
            'message': 'person.id not sent, not updating'
          }, 400 # Bad Request

        id = int(id)
        person['id'] = int(person['id'])

        # Fail if id is shady
        if id <= 0 or id != person['id']:
          return {
            'error': True,
            'message': 'person.id mismatch, not updating'
          }, 400 # Bad Request

        # Fail if name not set or name Empty
        if 'name' not in person.keys() or person['name'] == '':
          return {
            'error': True,
            'message': 'Name might not be empty'
          }, 400 # Bad Request

        if 'id' in person.keys() and person['id'] == 0:
          return {
            'error': True,
            'message': 'You cannot add person by put, use post instead'
          }, 405 # Method not Allowed


        image_link = False
        image = person['image'] if 'image' in person.keys() else ''
        if image and image != '':
          with open(f'static/images/person-{ person["id"] }.png', 'wb') as image_file:
            image_file.write(base64.b64decode(image))
            image_link = f'/static/images/person-{ person["id"] }.png'


        entry = session.query(ModelPerson).get(id)
        description = person['description'] if 'description' in person.keys() else ''

        entry.name = person['name']
        entry.description = description
        if image_link:
          entry.image = image_link
        session.commit()

        return {
          'error': False,
          'message': 'Person successfully updated'
        }, 201 # Created
      except Exception as e:
        return {
          'error': True,
          'message': f'Exception: {str(e)}'
        }, 400 # Bad Request
