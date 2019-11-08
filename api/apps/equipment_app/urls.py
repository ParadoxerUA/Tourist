from . import views

urls = {
    '/v1/equipment/<int:equipment_id>': views.EquipmentView.as_view('get_equipment'),
    '/v1/equipment/<int:equipment_id>': views.EquipmentView.as_view('update_equipment'),
    '/v1/equipment/<int:equipment_id>': views.EquipmentView.as_view('delete_equipment'),
    '/v1/equipment': views.EquipmentView.as_view('add_equipment'),
}

methods = {
    '/v1/equipment/<int:equipment_id>': ['GET'],
    '/v1/equipment/<int:equipment_id>': ['PATCH'],
    '/v1/equipment/<int:equipment_id>': ['DELETE'],
    '/v1/equipment': ['POST'],
}