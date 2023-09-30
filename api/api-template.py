"""
Example of Flask RESTFul integration.
requires: `pip install flask-restful`
"""
import sys

from flask import Flask
from flask_restful import Api, Resource, abort, reqparse
from flasgger import APISpec, Swagger, swag_from

from controller.locations import Locations, Location
from controller.boxes import Boxes, Box
from controller.items import Items, Item

from dataTransferObject.schemas import LocationSchema

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin


app = Flask(__name__)
api = Api(app)


api.add_resource(Locations, '/locations')
api.add_resource(Location, '/location/<id>')
api.add_resource(Boxes, '/boxes/<location_id>')
api.add_resource(Box, '/box/<id>')
api.add_resource(Items, '/items/<box_id>')
api.add_resource(Item, '/item/<id>')

spec = APISpec(
    title='Storganizer RESTful',
    version='1.0.10',
    openapi_version='2.0',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)
app.config['SWAGGER'] = {'uiversion': 3}



template = spec.to_flasgger(
    app,
    definitions=[LocationSchema],
    paths=[Locations.get]
)


# start Flasgger using a template from apispec
swag = Swagger(app, template=template)
















if __name__ == '__main__':
    app.run(debug=True)


sys.exit(0)
