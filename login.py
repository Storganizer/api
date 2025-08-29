#!/usr/bin/env python

from flask import Flask, redirect, url_for, session
from functools import wraps

from flask_restful import Resource, marshal_with


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


class User(Resource):

    def get(self):
      return {
        'logged_in': 'user' in session,
      }
