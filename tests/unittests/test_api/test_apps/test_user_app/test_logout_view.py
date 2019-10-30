import json
import redis
import uuid

from tests.unittests.basic_test import BasicTest


class TestLogoutView(BasicTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_logout(self):
        session_id = str(uuid.uuid1())
        session_data = {
            'user_id': '25',
        }
        with redis.Redis() as redis_client:
            redis_client.set(session_id, json.dumps(session_data))
        response = self.test_client.post('/api/user/v1/logout', headers={'Authorization': session_id})
        self.assertEqual(response.status_code, 200)

    def test_negative_logout(self):
        response = self.test_client.post('/api/user/v1/logout')
        self.assertEqual(response.status_code, 403)

