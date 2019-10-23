import unittest


class UserRegistrationTestCase(unittest.TestCase):
    """Test cases for User Model"""

    def setUp(self) -> None:
        import sys

        sys.path.append('./api')

        from api.config import DebugConfig
        from api.app import create_app
        app = create_app(DebugConfig)
        self.test_client = app.test_client()

    def tearDown(self):
        """Instructions that will be executed after every single test"""
        from api.database import db
        from api.apps.user_app.models import User
        db.session.query(User).delete()
        db.session.commit()


    def test_registration(self):
        data = {"name": "test", "email": "test", "password": "password"}
        response = self.test_client.post('/api/user/v1/register', content_type='application/x-www-form-urlencoded', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], 201)

