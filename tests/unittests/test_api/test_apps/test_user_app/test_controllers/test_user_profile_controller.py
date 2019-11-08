import json
import redis
from marshmallow import ValidationError
from tests.unittests.basic_test import BasicTest


class TestUserProfileController(BasicTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from apps.user_app.controllers.user_profile_controller import UserProfileController
        from apps.user_app.models import User
        cls.user_model = User
        cls.user_profile_controller = UserProfileController()

    def tearDown(self):
        from api.database import db
        db.session.query(self.user_model).delete()
        db.session.commit()

    def test_user_profile(self):
        user_data = {
            'name': 'Tania',
            'surname': 'Ivanova',
            'email': 'correct_email@yahoo.com',
            'password': 'correct_password'
        }
        user = self.user_model.create_user(name=user_data['name'], surname=user_data['surname'],
                                           email=user_data['email'], password=user_data['password'])
        result = self.user_profile_controller.get_user_profile(user_id=user.user_id)
        self.assertEqual(result['avatar'], user.avatar if user.avatar else 'http://localhost:5000/static/images/user_avatar.png')
        self.assertEqual(result['name'], user.name)
        self.assertEqual(result['surname'], user.surname)
        self.assertEqual(result['email'], user.email)
        self.assertEqual(result['capacity'], user.capacity)
