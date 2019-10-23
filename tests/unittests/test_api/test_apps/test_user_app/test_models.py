import unittest


class UserModelTestCase(unittest.TestCase):
    """Test cases for User Model"""

    def setUp(self) -> None:

        import sys
        sys.path.append('./api')

        from api.config import DebugConfig
        from api.app import create_app
        app = create_app(DebugConfig)
        self.test_client = app.test_client()

    def tearDown(self):
        """Instructions that will be executed after every single test"""
        from api.database import db
        from api.apps.user_app.models import User
        db.session.query(User).delete()
        db.session.commit()

    def test_create_user(self):
        from api.apps.user_app.models import User
        user = User.create_user(name='name', email='example@gmail.com', password='password')
        self.assertEqual(user.name, 'name')
        self.assertEqual(user.surname, None)
        self.assertEqual(user.email, 'example@gmail.com')
        self.assertTrue(User.check_password('password'))
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.uuid, None)

    def test_get_user(self):
        from api.apps.user_app.models import User
        user = User.create_user(name='Vasya', email='email', password='password')
        self.assertEqual(user.user_id, User.get_user(email='email').user_id)


    def test_activate_user(self):
        from api.apps.user_app.models import User
        user = User.create_user(name='Vasya', email='email', password='password')
        user.activate_user()
        self.assertTrue(user.is_active)

    def test_change_capacity(self):
        from api.apps.user_app.models import User
        user = User.create_user(name='Vasya', email='email', password='password')
        user.change_capacity(8)
        self.assertEqual(user.capacity, 8)


