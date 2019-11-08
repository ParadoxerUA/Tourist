from functools import wraps
from flask import request, g
from marshmallow import ValidationError
import redis, json

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = request.headers.get('Authorization')
        g.user_id = None
        with redis.Redis() as redis_client:
            user = redis_client.get(token) # return bytes
        if not user:
            raise ValidationError('Missing Authorization token')
        g.user_id = json.loads(user)['user_id']
        return f(*args, **kwargs)
    return wrap