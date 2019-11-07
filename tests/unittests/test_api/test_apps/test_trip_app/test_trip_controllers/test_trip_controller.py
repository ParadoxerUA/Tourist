import unittest, redis, json
from unittest.mock import patch, Mock, MagicMock
from tests.unittests.basic_test import BasicTest
import sys

if not "./api" in sys.path:
    sys.path.append("./api")
    
from apps.trip_app.controllers.trip_controller import TripController
from apps.trip_app.models.trip_model import Trip
from apps.trip_app.models.point_model import Point
from apps.user_app.models.user_model import User


class TestTripController(BasicTest):

    def setUp(self):
        self.app.models.Trip = Mock()
        self.Trip = self.app.models.Trip
        self.PointController = MagicMock()
        TripController._get_session_user = MagicMock()

    def test_create_trip(self):
        data = {"points": [{},{}]}
        trip = self.Trip.create_trip()
        trip.trip_id = 1
        self.Trip.create_trip.return_value = trip
        result = TripController.create_trip(data, 1)
        self.assertEqual(result, 1)


    # def test_refresh_trip_uuid_by_admin(self):
    #     new_uuid = TripController.refresh_trip_uuid(1, 1)
    #     self.assertEqual(new_uuid, 1)

    # @patch.object(Trip, 'get_trip_by_id')
    # @patch.object(TripController, '_get_session_user', side_effect=lambda x: x)
    # def test_refresh_trip_uuid_by_user(self, _get_session_user, get_trip_by_id):
    #     trip = get_trip_by_id.return_value
    #     trip.trip_uuid = 1
    #     trip.admin = 1
    #     user_id = 2
    #     new_uuid = self.trip_controller.refresh_trip_uuid(1, user_id)
    #     # self.assertTrue(get_trip_by_id.called)
    #     self.assertTrue(_get_session_user.called)
    #     self.assertEqual(new_uuid, None)

