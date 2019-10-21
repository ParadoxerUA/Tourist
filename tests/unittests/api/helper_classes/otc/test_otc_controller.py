import unittest
import sys

class OTCControllerTest(unittest.TestCase):
    def setUp(self):
        import sys
        import os

    def test_create_OTC_instance(self):
        from api.helper_classes import otc

        otc_instance = otc.OTCController.create_OTC_instance(
            'user_registration'
        )

        self.assertTrue(
            isinstance(
                otc_instance,
                otc.registration_otc.RegistrationOTC
            )
        )

        with self.assertRaises(otc.OTCUnavailableError):
            otc.OTCController.get_otc_type('some_code')

    def test_get_otc_type(self):
        from api.helper_classes import otc

        otc_instance = otc.OTCController.create_OTC_instance(
            'user_registration'
        )
        otc_instance.setup_otc()
        code = otc_instance.get_otc()
        otc_type = otc.OTCController.get_otc_type(code)

        self.assertEqual(otc_type, 'user_registration')
        with self.assertRaises(otc.OTCTypeError):
            otc.OTCController.create_OTC_instance('some_type')


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
