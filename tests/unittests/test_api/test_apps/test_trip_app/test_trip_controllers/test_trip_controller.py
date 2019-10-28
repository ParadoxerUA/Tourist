import unittest, redis, json
from unittest.mock import patch
from tests.unittests.basic_test import BasicTest
import sys

if not "./api" in sys.path:
    sys.path.append("./api")
    
from apps.trip_app.controllers.trip_controller import TripController
from apps.trip_app.models.trip_model import Trip
from apps.trip_app.models.point_model import Point
from apps.user_app.models.user_model import User


class TestTripController(BasicTest):

    @classmethod
    def setUpClass(cls):
        super(TestTripController, cls).setUpClass()
        cls.trip_controller = TripController()

    @patch.object(User, 'get_user_by_id', side_effect=lambda x: x)
    def test_get_session_user(self, get_user_by_id):

        session_id = 1
        user_id = 1
        with redis.Redis() as redis_client:
            redis_client.set(session_id, json.dumps({'user_id': user_id}))

        result = self.trip_controller._get_session_user(session_id)
        self.assertEqual(result, user_id)
        self.assertTrue(get_user_by_id.called)

    @patch.object(Trip, 'create_trip')
    @patch.object(Point, 'create_point')
    @patch.object(TripController, '_get_session_user')
    def test_create_trip(self, _get_session_user, create_point, create_trip):
        data = {"points": [{},{}]}
        trip = create_trip.return_value
        trip.trip_id = 1

        result = self.trip_controller.create_trip(data, 1)
        self.assertTrue(_get_session_user.called)
        self.assertTrue(create_trip.called)
        self.assertTrue(create_point.called)
        self.assertEqual(result, 1)
