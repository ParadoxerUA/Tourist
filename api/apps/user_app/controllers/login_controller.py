import uuid
import time
import json
import redis
from marshmallow import ValidationError
from apps.user_app.models import User


class LoginController:
    @classmethod
    def validate_fields(cls, email, password):
        error_message = {'non_field_errors': ['Incorrect email or password']}
        user = User.get_user_by_email(email=email)

        if not user or not user.check_password(password):
            raise ValidationError(error_message)

        if not user.is_active:
            raise ValidationError({'non_field_errors': ['Your account is not active']})

        return user

    @classmethod
    def login(cls, data):
        user = cls.validate_fields(**data)
        return cls._create_session(user=user)

    @classmethod
    def _create_session(cls, user):
        session_id = str(uuid.uuid1())
        login_time = 24 * 60 * 60
        started_at = time.time()
        expired_at = started_at + login_time
        session_data = {
            'user_id': user.user_id,
            'started_at': started_at,
            'expired_at': expired_at,
        }
        with redis.Redis() as redis_client:
            redis_client.set(session_id, json.dumps(session_data))

        return session_id
