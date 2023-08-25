#!/usr/bin/env python

from app.test import Test

import sys
import flask
import json
from sqlalchemy import create_engine
from sqlalchemy import text


app = flask.Flask('storganizer-api')
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

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

  with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

  test = Test()
  return asJson(test.getValues())


# main loop
if __name__ == "__main__":
  try:
    app.run(host="0.0.0.0", debug=True)
  except Exception as e:
    pprint(e)
    sys.exit(1)