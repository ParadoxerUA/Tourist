import unittest


class UserRegistrationTestCase(unittest.TestCase):
    """Test cases for User Model"""

    def setUp(self) -> None:
        import sys

        sys.path.append('./api')

        from api.config import DebugConfig
        from api.app import create_app
        self.app = create_app(DebugConfig)
        self.test_client = self.app.test_client()
        self.User = self.app.models.User

    def tearDown(self):
        """Instructions that will be executed after every single test"""
        self.app.db.session.query(self.User).delete()
        self.app.db.session.commit()


    def test_registration(self):
        data = {"name": "test", "email": "test", "password": "password"}
        response = self.test_client.post('/api/user/v1/register', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get["status"], 409)

