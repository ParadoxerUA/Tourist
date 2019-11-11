import json
import redis
import sys
from unittest.mock import patch, Mock
from marshmallow import ValidationError
from tests.unittests.basic_test import BasicTest

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
