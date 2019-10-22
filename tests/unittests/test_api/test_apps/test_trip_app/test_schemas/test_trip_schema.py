import unittest
from marshmallow import ValidationError
from datetime import date

class TestTripSchema(unittest.TestCase):
    def setUp(self):
        import sys
        sys.path.append("./api")
        from app import create_app
        from config import DebugConfig
        from apps.trip_app.schemas.trip_schema import TripSchema
        app = create_app(DebugConfig)
        self.test_client = app.test_client()
        self.trip_shema = TripSchema()
        self.data = {
            'name': 'Name',
            'description': '',
            'start_date': '2019-11-11',
            'end_date': '2019-11-11',
            'status': 'True'
        }

    def test_incorrect_short_name(self):
        self.data['name'] = 'N'
        with self.assertRaises(ValidationError):
            self.trip_shema.load(self.data)

    def test_incorrect_long_name(self):
        self.data['name'] = 'Long name'*20
        with self.assertRaises(ValidationError):
            self.trip_shema.load(self.data)

    def test_incorrect_long_description(self):
        self.data['description'] = 'Long description'*20
        with self.assertRaises(ValidationError):
            self.trip_shema.load(self.data)

    def test_incorrect_start_date(self):
        self.data['start_date'] = '2019 11 11'
        with self.assertRaises(ValidationError):
            self.trip_shema.load(self.data)

    def test_incorrect_end_date(self):
        self.data['end_date'] = '2019 11 11'
        with self.assertRaises(ValidationError):
            self.trip_shema.load(self.data)

    def test_incorrect_date_range(self):
        self.data['start_date'] = '2019-11-12'
        self.data['end_date'] = '2019-11-11'
        with self.assertRaises(ValidationError):
            self.trip_shema.load(self.data)

    def test_incorrect_status(self):
        self.data['status'] = "None"
        with self.assertRaises(ValidationError):
            self.trip_shema.load(self.data)

    def test_correct_data(self):
        expected_result = {
            'name': 'Name',
            'description': '',
            'start_date': date(2019, 11, 11),
            'end_date': date(2019, 11, 11),
            'status': True
        }
        self.assertEqual(self.trip_shema.load(self.data), expected_result)
