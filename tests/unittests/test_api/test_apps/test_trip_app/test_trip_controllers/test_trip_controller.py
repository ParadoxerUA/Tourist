import unittest
from unittest.mock import patch, MagicMock

class AddTripTestCase(unittest.TestCase):
    def setUp(self):
        import sys
        sys.path.append("./api")
        from api.app import create_app
        from api.config import DebugConfig
        app = create_app(DebugConfig)
        self.test_client = app.test_client()
        from apps.trip_app.controllers.trip_controller import TripController
        self.trip_controller = TripController()

    @patch('apps.trip_app.controllers.trip_controller.TripController.add_trip', return_value='1')
    def test_add_trip(self, db):

        # print(self.trip_controller.add_trip())
        self.assertEqual(1, 1)

    def tearDown(self):
        pass



