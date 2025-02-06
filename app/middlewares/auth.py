import datetime
from flask import request, jsonify
import jwt
from functools import wraps

def configure_auth_middleware(app):
    # whitelist of routes that do not require authentication
    AUTH_EXEMPT_ROUTES = {
        'healthcheck': { 'path': '/v1/healthcheck'},
        'register': {'path': '/v1/register'},
        'login': {'path': '/v1/login'}
    }

    @app.before_request
    def jwt_authentication():
        # whitelist check
        if any(
            request.path == route['path']
            for route in AUTH_EXEMPT_ROUTES.values()
        ):
            return

        # JWT token check
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({"error": "Authorization token required"}), 401

        try:
            secret_key = app.config['SECRET_KEY']
            algorithm = app.config['JWT_ALGORITHM']
            # print('secret_key:', secret_key)
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            # print('payload:', payload)
            # expired token check
            exp = payload.get('exp')
            if exp is None:
                return jsonify({"error": "Invalid token"}), 401
            if exp:
                current_timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
                print('current_timestamp:', current_timestamp) 
                if exp < current_timestamp:
                    return jsonify({"error": "Token expired"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401