import os
from sqlalchemy import select
from flask_restful import Resource
from flask import request, make_response
import json
import base64
import time


class DefaultImages(Resource):
    
    def get(self):
      defaultImages = {
        "location": '/static/images/_default-location.jpg',
        "box": '/static/images/_default-box.jpg',
        "item": '/static/images/_default-item.jpg',
        "person": '/static/images/_default-person.jpg'
      }
      return defaultImages
