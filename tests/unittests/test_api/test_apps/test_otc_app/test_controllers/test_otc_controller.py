import unittest
from unittest.mock import Mock, MagicMock, patch
from tests.unittests.basic_test import BasicTest
import redis


class TestOtcController(BasicTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.UserController = cls.app.blueprints['user'].controllers.UserController
        cls.TripController = cls.app.blueprints['trip'].controllers.TripController
        cls.OtcController = cls.app.blueprints['otc'].controllers.OtcController

    def test_handle_uuid(self):
        from apps.otc_app.otc import otc_exceptions
        from flask import g

        g.user_id = Mock()
        redis_client = redis.Redis()
        redis_client.set('uuid1', 'user_registration')
        redis_client.set('uuid2', 'trip_link')
        redis_client.set('uuid', 'some_type')

        with patch.object(self.UserController, 'activate_user', return_value='user_registration'):
            self.assertEqual(
                self.OtcController.handle_uuid('uuid1'),
                'user_registration'
            )

        with patch.object(self.TripController, 'user_to_trip', return_value='trip_link'):
            self.assertEqual(
                self.OtcController.handle_uuid('uuid2'),
                'trip_link'
            )
            
        with self.assertRaises(otc_exceptions.OtcTypeError):
            self.app.blueprints['otc'].controllers.OtcController.handle_uuid('uuid')

        redis_client.delete('uuid')
        redis_client.delete('uuid1')
        redis_client.delete('uuid2')
