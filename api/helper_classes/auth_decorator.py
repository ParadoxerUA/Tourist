from functools import wraps
from flask import request, g
from marshmallow import ValidationError
import redis

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = request.headers.get('Authorization')
        with redis.Redis() as redis_client:
            user = redis_client.get(token) # return bytes
        if not user:
            raise ValidationError('Missing Authorization token')
        g.session_id = token
        return f(*args, **kwargs)
    return wrap