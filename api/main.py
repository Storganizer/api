#!/usr/bin/env python

from model.base import Base
from model.location import Location
from model.box import Box
from model.connection import engine, session
#from model.item import item


from sqlalchemy import select

import sys
import flask
import json



app = flask.Flask('storganizer-api')

def asJson(data):
  response = flask.make_response(
    flask.jsonify(data),
    200,
  )
  response.headers["Content-Type"] = "application/json"
  return response



# api routes
@app.route("/test", methods = ['GET'])
def test():
  locations = []
  for location in session.scalars(select(Location)):
    locations.append(location.getDataTransferObject())
  return asJson(locations)


# main loop
if __name__ == "__main__":
  try:
    app.run(host="0.0.0.0", debug=True)
  except Exception as e:
    pprint(e)
    sys.exit(1)