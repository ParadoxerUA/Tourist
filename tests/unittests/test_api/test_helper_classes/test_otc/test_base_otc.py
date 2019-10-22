import unittest


class BaseOTCTest(unittest.TestCase):
    def test_otc_type_value(self):
        from api.helper_classes import otc

        otc_instance = otc.base_otc.BaseOTC('test_type')
        self.assertEqual(otc_instance._otc_type, 'test_type')

    def test_code_value(self):
        from api.helper_classes import otc

        otc_instance = otc.base_otc.BaseOTC('test_type')
        self.assertEqual(otc_instance._code, None)

    def test_insert_to_redis(self):
        import redis
        from api.helper_classes import otc

        otc_instance = otc.base_otc.BaseOTC('test_type')
        otc_instance._code = 'test_code'

        otc_instance._insert_to_redis()
        with redis.Redis() as r:
            otc_type = r.get('test_code').decode('utf8')

        self.assertEqual(otc_type, 'test_type')


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
