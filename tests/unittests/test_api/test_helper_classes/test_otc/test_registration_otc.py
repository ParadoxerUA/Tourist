import unittest


class RegistrationOTCTest(unittest.TestCase):
    def setUp(self):
        import sys
        import os

    def test_otc_type_value(self):
        from api.helper_classes import otc

        otc_instance = otc.registration_otc.RegistrationOTC()
        self.assertEqual(otc_instance._otc_type, 'user_registration')

    def test_setup_otc(self):
        import redis
        from api.helper_classes import otc

        otc_instance = otc.registration_otc.RegistrationOTC()
        otc_instance.setup_otc()
        code = otc_instance.get_otc()

        with redis.Redis() as r:
            otc_type = r.get(code).decode('utf8')

        self.assertEqual(otc_instance._otc_type, otc_type)


if __name__ == '__main__':
    import sys
    import os

    path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../../../../..'
        )
    )
    sys.path.append(path)
    unittest.main()
