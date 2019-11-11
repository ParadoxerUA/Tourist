import json
import redis
import sys
from unittest.mock import patch, Mock
from marshmallow import ValidationError
from tests.unittests.basic_test import BasicTest

if not "./api" in sys.path:
    sys.path.append("./api")

from apps.user_app.controllers.user_profile_controller import UserProfileController
from apps.user_app.models import User


class TestUserProfileController(BasicTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_profile_controller = UserProfileController()

    @patch.object(User, 'get_user_by_id')
    def test_user_profile(self, get_user_by_id):
        user_data = {
            'name': 'Tania',
            'surname': 'Ivanova',
            'email': 'correct_email@yahoo.com',
            'password': 'correct_password'
        }
        user_mock = Mock()
        user_mock.avatar = None
        user_mock.name = user_data['name']
        user_mock.surname = user_data['surname']
        user_mock.email = user_data['email']
        user_mock.password = user_data['password']

        get_user_by_id.return_value = user_mock

        result = self.user_profile_controller.get_user_profile(user_id=1)
        self.assertEqual(result['avatar'], 'http://localhost:5000/static/images/user_avatar.png')
        self.assertEqual(result['name'], user_mock.name)
        self.assertEqual(result['surname'], user_mock.surname)
        self.assertEqual(result['email'], user_mock.email)
        self.assertEqual(result['capacity'], user_mock.capacity)
