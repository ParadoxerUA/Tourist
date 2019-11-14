import unittest, redis, json
from unittest.mock import patch, Mock, MagicMock
from tests.unittests.basic_test import BasicTest
import sys

if not "./api" in sys.path:
    sys.path.append("./api")
    
from apps.trip_app.controllers.trip_controller import TripController
from apps.trip_app.controllers.point_controller import PointController
from apps.trip_app.models.trip_model import Trip
from apps.trip_app.models.point_model import Point
from apps.user_app.models.user_model import User


class TestTripController(BasicTest):

    def setUp(self):
        self.app.models.Trip = Mock()
        self.Trip = self.app.models.Trip
        PointController.create_point = MagicMock()
        TripController._get_session_user = MagicMock(side_effect=lambda x: x)

    def test_create_trip(self):
        data = {"points": [{},{}]}
        trip = self.Trip.create_trip()
        trip.trip_id = 1
        self.Trip.create_trip.return_value = trip
        result = TripController.create_trip(data, 1)
        self.assertEqual(result, 1)


    def test_refresh_trip_uuid_by_admin(self):
        admin_id = trip_id = 1
        trip = self.Trip.create_trip()
        self.Trip.get_trip_by_id.return_value = trip
        trip.admin = admin_id
        trip.trip_uuid = 1
        new_uuid = TripController.refresh_trip_uuid(trip_id, admin_id)
        self.assertEqual(new_uuid, 1)

    def test_refresh_trip_uuid_by_user(self):
        user_id = trip_id = 1
        trip = self.Trip.create_trip()
        self.Trip.get_trip_by_id.return_value = trip
        trip.trip_uuid = 1
        new_uuid = TripController.refresh_trip_uuid(trip_id, user_id)
        self.assertEqual(new_uuid, None)

    def test_get_trip_data_success(self):
        trip_id = user_id = 1
        fields_uuid = ['trip_uuid', 'field-1', 'field-2'] #<trip-uuid> - private field, should be deleted from trip_data if user != admin
        fields = ['field-1', 'field-2'] # for aditional recheck
        trip = self.Trip.create_trip()
        self.Trip.get_trip_by_id.return_value = trip
        trip.get_fields = lambda args: {arg:1 for arg in args}
        trip.users = [1,]
        trip_data_1 = TripController.get_trip_data(trip_id, user_id, fields_uuid)
        trip_data_2 = TripController.get_trip_data(trip_id, user_id, fields)
        self.assertEqual(trip_data_1, trip_data_2)
        self.assertEqual(True, bool(trip_data_2))
        self.assertEqual(bool(trip_data_1), True)

    def test_user_to_trip_success(self):
        trip_uuid = user_id = 1
        response = TripController.user_to_trip(trip_uuid, user_id)
        self.assertEqual(response, 'User assigned to trip')

    def test_user_to_trip_fail(self):
        trip_uuid = user_id = 1
        trip = self.Trip.create_trip()
        self.Trip.get_trip_by_uuid.return_value = trip
        trip.join_user = BaseException()
        response = TripController.user_to_trip(trip_uuid, user_id)
        self.assertEqual(response, None)
