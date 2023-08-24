#!/usr/bin/env python

from app.test import Test

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
  test = Test()
  return asJson(test.getValues())




# main loop
if __name__ == "__main__":
  try:
    app.run(host="0.0.0.0", debug=True)
  except Exception as e:
    pprint(e)
    sys.exit(1)