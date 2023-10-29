from model.box import Box as ModelBox
from model.connection import engine, session

from sqlalchemy import select
from flask_restful import Resource


class Boxes(Resource):
    def get(self, location_id):
        """
        Fetch all boxes
        ---
        tags:
          - boxes
        responses:
          200:
            description: All storage boxes
            schema:
              id: Boxes
              properties:
                task_id:
                  type: object
                  schema:
                    $ref: '#/definitions/Box'
        """
        boxes = []
        for box in session.scalars(select(ModelBox)):
          boxes.append(box.getDataTransferObject())

        return boxes

    def post(self):
        """
        Add a new box
        ---
        tags:
          - boxes
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/Box'
        responses:
          201:
            description: The Box has been created
            schema:
              $ref: '#/definitions/Box'
        """
        return [""]





# Todo
# shows a single todo item and lets you delete a todo item
class Box(Resource):
    def get(self, id):
        """
        This is an example
        ---
        tags:
          - boxes
        parameters:
          - in: path
            name: todo_id
            required: true
            description: The ID of the task, try 42!
            type: string
        responses:
          200:
            description: The task data
            schema:
              id: Task
              properties:
                task:
                  type: string
                  default: My Task
        """
        box = session.query(ModelBox).get(id)
        if box:
          return box.getDataTransferObject(["items"])

        return ["Box not found"]

    def delete(self, id):
        """
        This is an example
        ---
        tags:
          - boxes
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
          - boxes
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
