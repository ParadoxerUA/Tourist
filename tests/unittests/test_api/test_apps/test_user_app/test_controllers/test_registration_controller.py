import unittest
from unittest.mock import Mock, MagicMock
from tests.unittests.basic_test import BasicTest
from apps.user_app.controllers.user_controller import UserController

class TestUserRegistrationController(BasicTest):
    def setUp(self):
        self.app.models.User = Mock()
        self.User = self.app.models.User
        UserController.setup_registration_otc = MagicMock()

    def test_new_user_register(self):
        self.User.get_user_by_email.return_value = None
        result = UserController.register_user("name", "email", "password", "surname")
        self.assertEqual(result, "user created")
        
    def test_activated_user(self):
        user = self.User.create_user()
        self.User.get_user_by_email.return_value = user 
        user.is_active = True
        result = UserController.register_user("name", "email", "password", "surname")
        self.assertEqual(result, ("User is already registered", 400))

    def test_not_activated_user(self):
        user = self.User.create_user()
        self.User.get_user_by_email.return_value = user
        user.is_active = False
        user.is_uuid_valid = MagicMock(return_value=True)
        result = UserController.register_user("name", "email", "password", "surname")
        self.assertEqual(result, ("uuid is valid", 402))

    def test_registration_with_expired_uuid(self):
        user = self.User.create_user()
        self.User.get_user_by_email.return_value = user
        user.is_active = False
        user.is_uuid_valid = MagicMock(return_value=False)
        result = UserController.register_user("name", "email", "password", "surname")
        self.assertEqual(result, "user uuid updated")
        self.assertTrue(user.delete_user.called)

    def test_activate_user(self):
        self.app.models.User = Mock()
        user = self.app.models.User.create_user()
        self.app.models.User.get_user_by_uuid = MagicMock(return_value=user)
        user.activate_user = MagicMock(return_value=None)
        user.is_active = True
        self.assertEqual(UserController.activate_user('uuid'), ('user already activated', 409))
        user.is_active = False
        user.is_uuid_valid = MagicMock(return_value=True)
        self.assertEqual(UserController.activate_user('uuid'), ('user activated', 200))
