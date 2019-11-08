import uuid, time, json, redis, facebook
from marshmallow import ValidationError
from flask import current_app
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession
from google.auth.exceptions import GoogleAuthError


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
    def login_with_social(cls, data):
        user_data = cls._authorize_user(token=data['auth_token'], provider=data['provider'])
        
        user = current_app.models.User.get_user_by_email(email=user_data['email'])

        if not user:
            user = current_app.models.User.create_user(**user_data, is_active=True)
        elif not user.is_active:
            user.activate_user()
        
        return cls._create_session(user=user)
    
    @classmethod
    def _authorize_user(cls, token, provider):
        if provider == 'FACEBOOK':
            return cls._authorize_with_fb(token)
        if provider == 'GOOGLE':
            return cls._authorize_with_google(token)


    @staticmethod
    def _authorize_with_fb(token):
        try:
            graph = facebook.GraphAPI(access_token=token)
            raw_data = graph.get_object(id="me", fields='first_name, last_name, email, picture')
        except facebook.GraphAPIError as e:
            raise ValidationError(e.message)

        user_data = {
            'name': raw_data['first_name'],
            'surname': raw_data['last_name'],
            'email': raw_data['email'],
            'avatar': raw_data['picture']['data']['url']
        }
        return user_data

    @staticmethod
    def _authorize_with_google(token):
        credentials = Credentials(token)
        authed_session = AuthorizedSession(credentials)
        try:
            response = authed_session.get('https://www.googleapis.com/oauth2/v1/userinfo?alt=json')
        except GoogleAuthError:
            ValidationError('Invalid auth token')

        raw_data = json.loads(response.text)
        user_data = {
            'name': raw_data['given_name'],
            'surname': raw_data['family_name'],
            'email': raw_data['email'],
            'avatar': raw_data['picture']
        }
        return user_data

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
