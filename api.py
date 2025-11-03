#!/usr/bin/env python

"""
Example of Flask RESTFul integration.
requires: `pip install flask-restful`
"""
import sys
import os

from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask_wtf.csrf import CSRFProtect
from flask_restful import Api
from flask_cors import CORS
import uuid
from flask_restful import Resource, abort, reqparse

from login import User
from controller.locations import Locations, Location
from controller.locationTypes import LocationTypes, LocationType
from controller.boxes import Boxes, Box
from controller.items import Items, Item
from controller.persons import Persons, Person
from controller.backup import Backup, Restore
from controller.config import DefaultImages


app = Flask(__name__)
app.secret_key = 'app-secret-choose-freely'
# Session configuration for cross-origin requests
# For production with HTTPS, use SESSION_COOKIE_SAMESITE='None' and SESSION_COOKIE_SECURE=True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_HTTPONLY'] = True

print(os.getenv('KEYCLOAK_CLIENT_SECRET', 'client-secret'))

oauth = OAuth(app)
oauth.register(
    name='keycloak',
    client_id=os.getenv('KEYCLOAK_CLIENT_ID', 'storganizer-dev'),
    client_secret=os.getenv('KEYCLOAK_CLIENT_SECRET', 'client-secret'),
    server_metadata_url=os.getenv('KEYCLOAK_SERVER_METADATA_URL', 'https://cloak.gs.net-sec.ch/realms/storganizer/.well-known/openid-configuration'),
    client_kwargs={
        'scope': 'openid profile email'
    }
)

cors = CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "http://10.1.1.21:3000"],
        "supports_credentials": True,
        "allow_headers": ["Content-Type", "Authorization"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    }
})
api = Api(app)

app.config['SWAGGER'] = {
    'title': 'Storganizer RESTful',
    'uiversion': 3
}

api.add_resource(Locations, '/locations')
api.add_resource(Location, '/location/<id>')
api.add_resource(LocationTypes, '/locationTypes')
api.add_resource(LocationType, '/locationType/<id>')
api.add_resource(Boxes, '/boxes')
api.add_resource(Box, '/box/<id>')
api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<id>')
api.add_resource(Persons, '/persons')
api.add_resource(Person, '/person/<id>')
api.add_resource(Backup, '/backup')
api.add_resource(Restore, '/restore')
api.add_resource(DefaultImages, '/config/default-images')

api.add_resource(User, '/user')


# oidc
@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    nonce = uuid.uuid4().hex
    session['nonce'] = nonce
    return oauth.keycloak.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/auth')
def auth():
    token = oauth.keycloak.authorize_access_token()
    nonce = session.pop('nonce', None)
    user = oauth.keycloak.parse_id_token(token, nonce=nonce)
    session['user'] = user
    return redirect("http://127.0.0.1:3000")

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    return f"Hallo {session['user']['preferred_username']}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

sys.exit(0)
