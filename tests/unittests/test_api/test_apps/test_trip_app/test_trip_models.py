import unittest
from datetime import date


class TripModelTestCase(unittest.TestCase):
    def setUp(self):
        import sys
        sys.path.append("./api")
        from app import create_app
        from config import DebugConfig
        app = create_app(DebugConfig)
        self.test_client = app.test_client()

    def test_create_trip(self):
        from api.apps.trip_app.models import Trip
        expected_result = {
            'name': 'Name',
            'description': '',
            'start_date': date(2019, 11, 11),
            'end_date': date(2019, 11, 11),
            'status': True,
            'id_admin': 1
        }
        trip = Trip.create_trip(expected_result)
        self.assertEqual(trip.name, 'Name')
        self.assertEqual(trip.description, '')
        self.assertEqual(trip.start_date, date(2019, 11, 11))
        self.assertEqual(trip.end_date, date(2019, 11, 11))
        self.assertEqual(trip.status, True)
        self.assertEqual(trip.id_admin, 1)

    def tearDown(self):
        from database import db
        from apps.trip_app.models import Trip
        db.session.query(Trip).delete()
        db.session.commit()
