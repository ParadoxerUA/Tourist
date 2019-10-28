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
        self.assertEqual(result, "user is registered")

    def test_not_activated_user(self):

        user = self.User.create_user()
        self.User.get_user_by_email.return_value = user
        user.is_active = False
        user.is_uuid_valid = MagicMock(return_value=True)
        result = UserController.register_user("name", "email", "password", "surname")
        self.assertEqual(result, "uuid is valid")

    def test_registration_with_expired_uuid(self):
        user = self.User.create_user()
        self.User.get_user_by_email.return_value = user
        user.is_active = False
        user.is_uuid_valid = MagicMock(return_value=False)
        result = UserController.register_user("name", "email", "password", "surname")
        self.assertEqual(result, "user uuid updated")
        self.assertTrue(user.delete_user.called)

        