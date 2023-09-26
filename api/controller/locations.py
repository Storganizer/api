from model.location import Location as ModelLocation
from model.connection import engine, session

from sqlalchemy import select, text
from flask_restful import Resource


class Locations(Resource):
    def get(self):
        """
        Fetch all locations
        ---
        tags:
          - locations
        responses:
          200:
            description: All storage locations
            schema:
              id: Locations
              properties:
                task_id:
                  type: object
                  schema:
                    $ref: '#/definitions/Location'
        """
        locations = []
        for location in session.scalars(select(ModelLocation)):
          locations.append(location.getDataTransferObject())


        return locations

    def post(self):
        """
        Add a new location
        ---
        tags:
          - locations
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/Location'
        responses:
          201:
            description: The Location has been created
            schema:
              $ref: '#/definitions/Location'
        """
        return [""]





# Todo
# shows a single todo item and lets you delete a todo item
class Location(Resource):

    def get(self, id):
        """
        Get single location
        ---
        tags:
          - location
        parameters:
          - in: path
            name: id
            required: true
            description: Location ID
            type: string
        responses:
          200:
            description: The location data transfer object
            schema:
              id: Location
              properties:
                name:
                  type: string
                description:
                  type: string
                image:
                  type: string
                classification:
                  type: string
                boxes:
                  type: list
        """
        return session.query(ModelLocation).get(id).getDataTransferObject()

    def delete(self, id):
        """
        This is an example
        ---
        tags:
          - location
        parameters:
          - in: path
            name: todo_id
            required: true
            description: The ID of the task, try 42!
            type: string
        responses:
          204:
            description: Task deleted
        """
        return '', 204

    def put(self, id):
        """
        This is an example
        ---
        tags:
          - location
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/Task'
          - in: path
            name: todo_id
            required: true
            description: The ID of the task, try 42!
            type: string
        responses:
          201:
            description: The task has been updated
            schema:
              $ref: '#/definitions/Task'
        """
        return [""]
