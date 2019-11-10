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

    @patch.object(Equipment, 'get_equipment_by_id')
    def test_get_equipment_data(self, get_equipment_by_id):
        equipment_data = {
            'equipment_id': 1,
            'name': 'Apple',
            'weight': 1,
            'quantity': 3,
            'trip_id': 1
        }

        equipment_mock = Mock()
        equipment_mock.equipment_id = equipment_data['equipment_id']
        equipment_mock.name = equipment_data['name']
        equipment_mock.weight = equipment_data['weight']
        equipment_mock.quantity = equipment_data['quantity']
        equipment_mock.trip_id = equipment_data['trip_id']

        get_equipment_by_id.return_value = equipment_mock
        result = self.Equipment.get_equipment_data(equipment_id=1)

        self.assertEqual(result, equipment_mock)

    def test_update_equipment(self):
        pass

    def test_delete_equipment(self):
        pass

    def test_create_equipment(self):
        pass
