import unittest
import json
from unittest.mock import patch


class TestCreateTripView(unittest.TestCase):

    def setUp(self):
        import sys

        sys.path.append("./api")
        from api.app import create_app
        from api.config import DebugConfig
        app = create_app(DebugConfig)
        self.test_client = app.test_client()
        self.data = {
            "name": "name",
            "description": "desc",
            "start_date": "2011-10-05T14:48:00.000Z",
            "end_date": "2011-10-05T14:48:00.000Z"
            }

    @patch('apps.trip_app.controllers.TripController.create_trip')
    def test_create_trip_success(self, create_trip):
        create_trip.return_value = self.data
        response = self.test_client.post('api/trip/v1/create_trip', 
                                        data=json.dumps(self.data), 
                                        content_type='application/json',
                                        headers={'Authorization': 'some hash'})
                                        
        expected_result = json.loads(response.data)['data']
        self.assertEqual(expected_result, [self.data])
        self.assertEqual(response.status_code, 201)

    def test_create_trip_error(self):
        response = self.test_client.post('api/trip/v1/create_trip', 
                                        data=json.dumps({}), 
                                        content_type='application/json',
                                        headers={'Authorization': 'some hash'})
        self.assertEqual(response.status_code, 400)
