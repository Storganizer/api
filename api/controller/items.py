from model.item import Item as ModelItem
from model.connection import engine, session

from sqlalchemy import select
from flask_restful import Resource
import time


class Items(Resource):
    def get(self):
        time.sleep(6)
        items = []
        for item in session.scalars(select(ModelItem)):
          items.append(item.getDataTransferObject())

        return items

    def post(self):
        return [""]


class Item(Resource):
    def get(self, id):
        item = session.query(ModelItem).get(id)
        if item:
          return item.getDataTransferObject(['box'])

        return ["Item not found"]

    def delete(self, id):
        return '', 204

    def put(self, id):
        return [""]
