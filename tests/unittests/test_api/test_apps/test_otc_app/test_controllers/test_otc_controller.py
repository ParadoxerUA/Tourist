import unittest
from unittest.mock import Mock, MagicMock
from tests.unittests.basic_test import BasicTest


class TestOTCController(BasicTest):
    def test_handle_uuid(self):
        from apps.otc_app.controllers import OTCController
        from apps.otc_app.otc import otc_exceptions

        OTCController._activate_user = MagicMock(return_value=True)
        self.assertEqual(
            OTCController.handle_uuid('uuid', 'user_registration'),
            True
        )
        with self.assertRaises(otc_exceptions.OTCTypeError):
            OTCController.handle_uuid('uuid', 'some_type')

    def test__activate_user(self):
        from apps.otc_app.controllers import OTCController
        from apps.otc_app.otc import otc_exceptions
        from app import create_app
        from config import DebugConfig

        self.app.models.User = Mock()
        user = self.app.models.User.create_user()
        self.app.models.User.get_user_by_uuid = MagicMock(return_value=user)
        user.activate_user = MagicMock(return_value=None)

        user.is_active = True
        self.assertEqual(OTCController._activate_user('uuid'), 'user already activated')

        user.is_active = False
        user.is_uuid_valid = MagicMock(return_value=True)
        self.assertEqual(OTCController._activate_user('uuid'), 'user activated')

        with self.assertRaises(otc_exceptions.OTCOutdatedError):
            user.is_uuid_valid = MagicMock(return_value=False)
            user.is_active = False
            OTCController._activate_user('uuid')
