from unittest.mock import patch, Mock, MagicMock
from tests.unittests.basic_test import BasicTest
import sys

if "./api" not in sys.path:
    sys.path.append("./api")

from apps.equipment_app.controllers.equipment_controller import EquipmentController
from apps.equipment_app.models import Equipment
# from apps.user_app.models.user_model import User


class TestEquipmentController(BasicTest):
    """Tests for equipment_app controller"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from flask import g
        g.user_id = Mock()

    def setUp(self):
        self.Equipment = EquipmentController()
        self.equipment_data = {
            'equipment_id': 1,
            'name': 'Apple',
            'weight': 1,
            'quantity': 3,
            'trip_id': 1
        }

    @patch.object(Equipment, 'get_equipment_by_id')
    def test_get_equipment_data(self, get_equipment_by_id):
        user = Mock()
        user.trips = []
        EquipmentController._get_user = Mock(return_value=user)
        equipment_mock = Mock(**self.equipment_data)

        user.trips.append(equipment_mock.trip)

        get_equipment_by_id.return_value = equipment_mock
        result = self.Equipment.get_equipment_data(equipment_id=1)

        self.assertEqual(result, (equipment_mock, 201))

    @patch.object(Equipment, 'update_equipment')
    def test_update_equipment(self, update_equipment):
        new_data = {
            'name': 'Orange',
            'weight': 2,
            'quantity': 4
        }
        EquipmentController._get_eq = Mock()
        EquipmentController._user_has_privileges = Mock(return_value=True)
        update_equipment.return_value = None
        equipment_id = 1
        result = self.Equipment.update_equipment(equipment_id, new_data)

        self.assertEqual(result, (None, 201))

    # @patch.object(Equipment, 'delete_equipment')
    # def test_delete_equipment(self, delete_equipment):
    #     EquipmentController._get_eq = Mock()
    #     EquipmentController._user_has_privileges = Mock(return_value=True)
    #     delete_equipment.return_value = None
    #     result = self.Equipment.delete_equipment(equipment_id=1)

    #     self.assertEqual(result, (None, 201))

    # @patch.object(Equipment, 'create_equipment')
    # def test_create_equipment(self, create_equipment):
    #     equipment_mock_1 = Mock()
    #     equipment_mock_1.equipment_id = self.equipment_data['equipment_id']
    #     equipment_mock_1.name = self.equipment_data['name']
    #     equipment_mock_1.weight = self.equipment_data['weight']
    #     equipment_mock_1.quantity = self.equipment_data['quantity']
    #     equipment_mock_1.trip_id = self.equipment_data['trip_id']

    #     equipment_mock_2 = Mock()
    #     equipment_mock_2.equipment_id = self.equipment_data['equipment_id']

    #     create_equipment.return_value = equipment_mock_1
    #     result = self.Equipment.create_equipment(self.equipment_data)

    #     self.assertEqual(result, equipment_mock_1)
    #     self.assertNotEqual(result, equipment_mock_2)
