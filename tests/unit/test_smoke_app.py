import unittest
from flask import Flask
from api.smoke_app.app import smoke_app


class BasicTestCase(unittest.TestCase):
    """Basic test cases for the smoke_app blueprint"""

    def setUp(self):
        """Instructions that will be executed before every single test"""

        self.app = Flask(__name__)
        self.app.register_blueprint(smoke_app)
        self.test_client = self.app.test_client()

    def tearDown(self):
        """Instructions that will be executed after every single test"""

        pass

    def test_home_status_code(self):
        """Home page status code test"""

        response = self.test_client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    def test_smoke_status_code(self):
        """Smoke page status code test"""

        response = self.test_client.get('/smoke', content_type='html/text')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
