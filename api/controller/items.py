from model.item import Item as ModelItem
from model.connection import engine, session

from sqlalchemy import select
from flask_restful import Resource


class Items(Resource):
    def get(self):
        """
        Fetch all items
        ---
        tags:
          - items
        responses:
          200:
            description: All storage items
            schema:
              id: Items
              properties:
                task_id:
                  type: object
                  schema:
                    $ref: '#/definitions/Item'
        """
        items = []
        for item in session.scalars(select(ModelItem)):
          items.append(item.getDataTransferObject())

        return items

    def post(self):
        """
        Add a new Item
        ---
        tags:
          - items
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/Item'
        responses:
          201:
            description: The Item has been created
            schema:
              $ref: '#/definitions/Item'
        """
        return [""]





# Todo
# shows a single todo item and lets you delete a todo item
class Item(Resource):
    def get(self, id):
        """
        This is an example
        ---
        tags:
          - items
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
        item = session.query(ModelItem).get(id)
        if item:
          return item.getDataTransferObject(['box'])

        return ["Item not found"]

    def delete(self, id):
        """
        This is an example
        ---
        tags:
          - items
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
          - items
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
