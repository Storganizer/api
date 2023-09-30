from model.location import Location as ModelLocation
from model.connection import engine, session

from sqlalchemy import select, text
from flask_restful import Resource, marshal_with



class Locations(Resource):
    """
    Location definition to use in this classes
    ---
    responses:
      200:
        description: Schema
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
              type: int
            boxes:
              type: list
    """

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
                list:
                  type: list
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
          - locations
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
              $ref: '#/definitions/Location'
        """
        return session.query(ModelLocation).get(id).getDataTransferObject()

    def delete(self, id):
        """
        Delete a location
        ---
        tags:
          - locations
        parameters:
          - in: path
            name: id
            required: true
            description: The Location ID to delete
            type: string
        responses:
          204:
            description: Location deleted
        """
        return '', 204

    def put(self, id):
        """
        Update a location
        ---
        tags:
          - locations
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/Location'
          - in: path
            name: id
            required: true
            description: The location ID to be updated
            type: string
        responses:
          201:
            description: Updated location data
            schema:
              $ref: '#/definitions/Location'
        """
        return [""]
