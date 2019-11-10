import unittest
import json
from unittest.mock import patch
from tests.unittests.basic_test import BasicTest
import sys

if not "./api" in sys.path:
    sys.path.append("./api")
    
from apps.trip_app.controllers.trip_controller import TripController


class TestCreateTripView(BasicTest):
    
    @classmethod
    def setUpClass(cls):
        super(TestCreateTripView, cls).setUpClass()
        cls.data = {
            "name": "name",
            "description": "desc",
            "start_date": "2011-10-05T14:48:00.000Z",
            "end_date": "2011-10-05T14:48:00.000Z"
            }

    # @patch.object(TripController, 'create_trip')
    # def test_create_trip_success(self, create_trip):
    #     create_trip.return_value = self.data
    #     response = self.test_client.post('api/trip/v1/create_trip', 
    #                                     data=json.dumps(self.data), 
    #                                     content_type='application/json',
    #                                     headers={'Authorization': 'some hash'})
                                        
    #     expected_result = json.loads(response.data)['data']
    #     self.assertEqual(expected_result, [self.data])
    #     self.assertEqual(response.status_code, 201)

    # def test_create_trip_error(self):
    #     response = self.test_client.post('api/trip/v1/create_trip', 
    #                                     data=json.dumps({}), 
    #                                     content_type='application/json',
    #                                     headers={'Authorization': 'some hash'})
    #     self.assertEqual(response.status_code, 400)
