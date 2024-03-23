#!/usr/bin/env python

"""
Example of Flask RESTFul integration.
requires: `pip install flask-restful`
"""
import sys

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_restful import Api
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

from flask_restful import Resource, abort, reqparse

from controller.locations import Locations, Location
from controller.boxes import Boxes, Box
from controller.items import Items, Item
from controller.persons import Persons, Person
from controller.backup import Backup, Restore
from controller.config import DefaultImages

app.config['SWAGGER'] = {
    'title': 'Storganizer RESTful',
    'uiversion': 3
}

api.add_resource(Locations, '/locations')
api.add_resource(Location, '/location/<id>')
api.add_resource(Boxes, '/boxes')
api.add_resource(Box, '/box/<id>')
api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<id>')
api.add_resource(Persons, '/persons')
api.add_resource(Person, '/person/<id>')
api.add_resource(Backup, '/backup')
api.add_resource(Restore, '/restore')
api.add_resource(DefaultImages, '/config/default-images')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

sys.exit(0)
