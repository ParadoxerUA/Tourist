import unittest


class BasicTestCase(unittest.TestCase):
    """Basic test cases for the smoke_app blueprint"""

    def setUp(self):
        """Instructions that will be executed before every single test"""
        import sys
        sys.path.append("./api")
        from api.app import create_app
        from api.config import DebugConfig
        app = create_app(DebugConfig)
        self.test_client = app.test_client()

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
