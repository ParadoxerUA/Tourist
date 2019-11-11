import json
import redis
import sys
from unittest.mock import patch, Mock
from marshmallow import ValidationError
from tests.unittests.basic_test import BasicTest
from unittest.mock import Mock, MagicMock

if not "./api" in sys.path:
    sys.path.append("./api")

from apps.user_app.controllers.login_controller import LoginController
from apps.user_app.models import User


class TestLoginController(BasicTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.login_controller = LoginController()
        cls.user_data = {
            'email': 'some_email@yahoo.com',
            'password': 'some_password'
        }
        cls._authorize_user_patcher = patch.object(LoginController, '_authorize_user')
        cls._create_session_patcher = patch.object(LoginController, '_create_session', side_effect=lambda user: user)
        cls.user_model_patcher = patch.object(cls.app.models, 'User')
        cls.user = Mock()
        cls.social_data = {'auth_token': '', 'provider': ''}

    @patch.object(User, 'get_user_by_email', return_value=None)
    def test_incorrect_email(self, get_user_by_email):

        with self.assertRaises(ValidationError):
            self.login_controller.login(data=self.user_data)

    @patch.object(User, 'get_user_by_email')
    def test_incorrect_password(self, get_user_by_email):
        user_mock = Mock(name='Test User object')
        user_mock.check_password.return_value = False

        get_user_by_email.return_value = user_mock

        with self.assertRaises(ValidationError):
            self.login_controller.login(data=self.user_data)

    @patch.object(User, 'get_user_by_email')
    def test_login(self, get_user_by_email):
        user_mock = Mock(name='Test User object')
        user_mock.check_password.return_value = True
        user_mock.is_active = True
        user_mock.user_id = 1

        get_user_by_email.return_value = user_mock

        session_id = self.login_controller.login(data=self.user_data)
        with redis.Redis() as redis_client:
            result = redis_client.get(session_id)
        self.assertIsNotNone(result)
        result = json.loads(result)
        self.assertEqual(result['user_id'], user_mock.user_id)
        self.assertEqual((result['expired_at'] - result['started_at']), 24 * 60 * 60)


    def test_login_with_social_active_user(self):
        self.start_patch()

        self.user.is_active = True
        self.app.models.User.get_user_by_email.return_value = self.user

        result = self.login_controller.login_with_social(self.social_data)

        self.assertEqual(self.app.models.User.get_user_by_email.called, True)
        self.assertEqual(self.app.models.User.create_user.called, False)
        self.assertEqual(self.app.models.User.activate_user.called, False)
        self.assertEqual(result, self.user)
        self.assertEqual(result.is_active, True)
        
        self.stop_patch()

    def test_login_with_social_not_active_user(self):
        self.start_patch()

        self.user.is_active = False
        self.app.models.User.get_user_by_email.return_value = self.user

        def activate_user():
            self.user.is_active = True

        self.user.activate_user.side_effect = activate_user
        result = self.login_controller.login_with_social(self.social_data)

        self.assertEqual(self.app.models.User.get_user_by_email.called, True)
        self.assertEqual(self.app.models.User.create_user.called, False)
        self.assertEqual(self.user.activate_user.called, True)
        self.assertEqual(result, self.user)
        self.assertEqual(result.is_active, True)

        self.stop_patch()

    def test_login_with_social_new_user(self):
        self.start_patch()

        self.app.models.User.get_user_by_email.return_value = None
        self.app.models.User.create_user.return_value = self.user
        self.user.is_active = True

        result = self.login_controller.login_with_social(self.social_data)

        self.assertEqual(self.app.models.User.get_user_by_email.called, True)
        self.assertEqual(self.app.models.User.create_user.called, True)
        self.assertEqual(self.user.activate_user.called, False)
        self.assertEqual(result, self.user)
        self.assertEqual(result.is_active, True)

        self.stop_patch()

    @classmethod
    def start_patch(cls):
        cls.user_model_patcher.start()
        cls._authorize_user_patcher.start()
        cls._create_session_patcher.start()

    @classmethod
    def stop_patch(cls):
        cls._authorize_user_patcher.stop()
        cls._create_session_patcher.stop()
        cls.user_model_patcher.stop()