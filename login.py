#!/usr/bin/env python

from flask import Flask, redirect, url_for, session, current_app
from functools import wraps

from flask_restful import Resource, marshal_with


def oidc_required(f):
    """
    Decorator that enforces OIDC authentication when OIDC_AUTH is enabled.
    When OIDC_AUTH=false, this decorator does nothing (pass-through).
    When OIDC_AUTH=true, it checks for valid session and returns 401 if not authenticated.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If OIDC_AUTH is disabled, allow access without authentication
        if not current_app.config.get('OIDC_AUTH', False):
            return f(*args, **kwargs)

        # If OIDC_AUTH is enabled, require valid session
        if 'user' not in session:
            return {
                'error': True,
                'message': 'Authentication required. Please log in.'
            }, 401  # Unauthorized

        # Ensure personId is set in session (should be set during /auth callback)
        if 'personId' not in session:
            return {
                'error': True,
                'message': 'User profile not found. Please log out and log in again.'
            }, 401  # Unauthorized

        return f(*args, **kwargs)
    return decorated_function


def getCurrentPersonId():
    """
    Returns the current user's personId from session.
    Returns None if OIDC_AUTH is disabled or user is not logged in.
    """
    if not current_app.config.get('OIDC_AUTH', False):
        return None
    return session.get('personId', None)


def isOidcEnabled():
    """
    Returns True if OIDC authentication is enabled.
    """
    return current_app.config.get('OIDC_AUTH', False)


class User(Resource):

    def get(self):
        user_data = {
            'logged_in': 'user' in session,
            'oidc_enabled': isOidcEnabled(),
        }
        if 'user' in session:
            user_data['user'] = session['user']
            user_data['personId'] = getCurrentPersonId()
        return user_data
