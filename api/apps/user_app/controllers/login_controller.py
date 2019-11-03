import uuid, time, json, redis, facebook
from marshmallow import ValidationError
from flask import current_app


class LoginController:
    @classmethod
    def validate_fields(cls, email, password):
        error_message = {'non_field_errors': ['Incorrect email or password']}

        user = current_app.models.User.get_user_by_email(email=email)

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
    def login_with_social(cls, user_id, token):
        user_data = cls._authorize_with_fb(user_id, token)
        
        user = current_app.models.User.get_user_by_email(email=user_data['email'])

        if not user:
            user = current_app.models.User.create_user(name=user_data['first_name'], 
                                                        surname = user_data['last_name'],
                                                        email=user_data['email'],
                                                        avatar=user_data['picture']['data']['url'], 
                                                        is_active=True)
        elif not user.is_active:
            user.activate_user()
        
        return cls._create_session(user=user)

    @staticmethod
    def _authorize_with_fb(user_id, token):
        try:
            graph = facebook.GraphAPI(access_token=token)
            user_data = graph.get_object(id=user_id, fields='first_name, last_name, email, picture')
            return user_data
        except facebook.GraphAPIError as e:
            raise ValidationError(e.message)

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
