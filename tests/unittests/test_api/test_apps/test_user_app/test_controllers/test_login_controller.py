import json
import redis
from marshmallow import ValidationError
from tests.unittests.basic_test import BasicTest


class TestLoginController(BasicTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from apps.user_app.controllers.login_controller import LoginController
        from apps.user_app.models import User
        cls.user_model = User
        cls.login_controller = LoginController()

    def tearDown(self):
        from api.database import db
        db.session.query(self.user_model).delete()
        db.session.commit()

    def test_incorrect_email(self):
        user_data = {
            'email': 'incorrect_email@yahoo.com',
            'password': 'correct_password'
        }
        with self.assertRaises(ValidationError):
            self.login_controller.login(data=user_data)

    def test_incorrect_password(self):
        self.user_model.create_user(name='Tania', email='correct_email@yahoo.com', password='correct_password')
        user_data = {
            'email': 'correct_email@yahoo.com',
            'password': 'incorrect_password'
        }
        with self.assertRaises(ValidationError):
            self.login_controller.login(data=user_data)

    def test_login(self):
        user = self.user_model.create_user(name='Tania', email='correct_email@yahoo.com', password='correct_password')
        user.activate_user()
        user_data = {
            'email': 'correct_email@yahoo.com',
            'password': 'correct_password'
        }
        session_id = self.login_controller.login(data=user_data)
        with redis.Redis() as redis_client:
            result = redis_client.get(session_id)
        self.assertIsNotNone(result)
        result = json.loads(result)
        self.assertEqual(result['user_id'], user.user_id)
        self.assertEqual((result['expired_at'] - result['started_at']), 24 * 60 * 60)
