from unittest.mock import patch, Mock
from tests.unittests.basic_test import BasicTest
import sys

if "./api" not in sys.path:
    sys.path.append("./api")

from apps.equipment_app.controllers.equipment_controller import EquipmentController
from apps.equipment_app.models import Equipment


class TestEquipmentController(BasicTest):
    """Tests for equipment_app controller"""

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
        equipment_mock = Mock()
        equipment_mock.equipment_id = self.equipment_data['equipment_id']
        equipment_mock.name = self.equipment_data['name']
        equipment_mock.weight = self.equipment_data['weight']
        equipment_mock.quantity = self.equipment_data['quantity']
        equipment_mock.trip_id = self.equipment_data['trip_id']

        get_equipment_by_id.return_value = equipment_mock
        result = self.Equipment.get_equipment_data(equipment_id=1)

        self.assertEqual(result, equipment_mock)

    @patch.object(Equipment, 'update_equipment')
    def test_update_equipment(self, update_equipment):
        new_data = {
            'name': 'Orange',
            'weight': 2,
            'quantity': 4
        }
        update_equipment.return_value = None
        equipment_id = 1
        result = self.Equipment.update_equipment(equipment_id, new_data)

        self.assertEqual(result, None)

    def test_delete_equipment(self):
        pass

    @patch.object(Equipment, 'create_equipment')
    def test_create_equipment(self, create_equipment):
        equipment_mock_1 = Mock()
        equipment_mock_1.equipment_id = self.equipment_data['equipment_id']
        equipment_mock_1.name = self.equipment_data['name']
        equipment_mock_1.weight = self.equipment_data['weight']
        equipment_mock_1.quantity = self.equipment_data['quantity']
        equipment_mock_1.trip_id = self.equipment_data['trip_id']

        equipment_mock_2 = Mock()
        equipment_mock_2.equipment_id = self.equipment_data['equipment_id']

        create_equipment.return_value = equipment_mock_1
        result = self.Equipment.create_equipment(self.equipment_data)

        self.assertEqual(result, equipment_mock_1)
        self.assertNotEqual(result, equipment_mock_2)
