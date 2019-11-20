import unittest
from unittest.mock import Mock, MagicMock, patch
from tests.unittests.basic_test import BasicTest
from apps.user_app.controllers.user_controller import UserController
from apps.trip_app.controllers.trip_controller import TripController 
import redis


class TestOtcController(BasicTest):
    def test_handle_uuid(self):
        from apps.otc_app.otc import otc_exceptions


        redis_client = redis.Redis()
        redis_client.set('uuid1', 'user_registration')
        redis_client.set('uuid2', 'trip_link')
        redis_client.set('uuid', 'some_type')

        with patch.object(UserController, 'activate_user', return_value='user_registration'):
            self.assertEqual(
                self.app.blueprints['otc'].controllers.OtcController.handle_uuid('uuid1'),
                'user_registration'
            )

        with patch.object(TripController, 'user_to_trip', return_value='trip_link'):
            self.assertEqual(
                self.app.blueprints['otc'].controllers.OtcController.handle_uuid('uuid2'),
                'trip_link'
            )
            
        with self.assertRaises(otc_exceptions.OtcTypeError):
            self.app.blueprints['otc'].controllers.OtcController.handle_uuid('uuid')
