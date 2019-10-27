import unittest
from marshmallow import ValidationError


class TestTripSchema(unittest.TestCase):
    def setUp(self):
        import sys
        sys.path.append("./api")
        from app import create_app
        from config import DebugConfig
        from apps.trip_app.schemas.trip_schema import TripSchema
        app = create_app(DebugConfig)
        self.test_client = app.test_client()
        self.trip_schema = TripSchema()

    def test_validate_incorrect_date_range(self):
        data = {
            'start_date': '2019-11-12T00:00:00.000Z',
            'end_date': '2019-11-11T00:00:00.000Z',
        }
        with self.assertRaises(ValidationError):
            self.trip_schema._validate_date(data)

    def test_validate_correct_date_range(self):
        data = {
            'start_date': '2019-11-11T00:00:00.000Z',
            'end_date': '2019-11-11T00:00:00.000Z',
        }
        self.assertEqual(self.trip_schema._validate_date(data), None)
