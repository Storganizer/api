"""
Example of Flask RESTFul integration.
requires: `pip install flask-restful`
"""
import sys

from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

from flask_restful import Resource, abort, reqparse
from flasgger import Swagger, swag_from

from controller.locations import Locations, Location
from controller.boxes import Boxes, Box
from controller.items import Items, Item





from flasgger import Schema, fields

app.config['SWAGGER'] = {
    'title': 'Storganizer RESTful',
    'uiversion': 3
}
swag = Swagger(app)


api.add_resource(Locations, '/locations')
api.add_resource(Location, '/location/<id>')
api.add_resource(Boxes, '/boxes/<location_id>')
api.add_resource(Box, '/box/<id>')
api.add_resource(Items, '/items/<box_id>')
api.add_resource(Item, '/item/<id>')

if __name__ == '__main__':
    app.run(debug=True)


sys.exit(0)
