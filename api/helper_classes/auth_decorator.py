from functools import wraps
from flask import request, g, make_response, jsonify, current_app
from marshmallow import ValidationError
from werkzeug.exceptions import Unauthorized
from datetime import datetime
import redis, json


def custom_response(message, status_code):
        response = {
            'data': message,
            'date': datetime.now().__str__(),
        }
        return make_response(jsonify(response), status_code)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return custom_response('Missing Authorization token', 401)
        with create_redis_tmp() as redis_client:
            user = redis_client.get(token) # return bytes
        if not user:
            return custom_response('Invalid Authorization token', 401)
        g.user_id = json.loads(user)['user_id']
        return f(*args, **kwargs)
    return wrap

def otc_authorization(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            g.user_id = None
            return f(*args, **kwargs)
        with create_redis_tmp() as redis_client:
            user = redis_client.get(token) # return bytes
        if not user:
            return custom_response('Invalid Authorization token', 401)
        g.user_id = json.loads(user)['user_id']
        return f(*args, **kwargs)
    return wrap

def create_redis_tmp():
    broker_url = current_app.config['CELERY_BROKER_URL']
    slashes_index = broker_url.index('//')
    semicolon_index = broker_url.index(':', slashes_index)
    last_slash_index = broker_url.index('/', semicolon_index)

    host = broker_url[slashes_index + 2:semicolon_index]
    port = broker_url[semicolon_index + 1:last_slash_index]
    db = broker_url[last_slash_index + 1:]
    return redis.Redis(host=host, port=port, db=db)
