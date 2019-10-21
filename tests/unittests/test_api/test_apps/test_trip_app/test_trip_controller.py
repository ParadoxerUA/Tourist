from unittest import TestCase
from api.apps.trip_app.models import Trip
from datetime import date
from app import create_app
from config import DebugConfig
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


class AddTripTestCase(TestCase):
    def setUp(self):
        import sys
        sys.path.append("./api")
        from api.app import create_app
        from api.config import DebugConfig
        app = create_app(DebugConfig)
        self.test_client = app.test_client()

    def test_create_trip(self):
        trip = Trip.create_trip(self.data)
        TestCase.assertEqual(1, trip)



