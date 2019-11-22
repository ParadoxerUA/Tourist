from . import views


urls = {
    '/v1/trips/<int:trip_id>': views.SingleTripView.as_view('trip'),
    '/v1/trips': views.TripsView.as_view('trips'),
    '/v1/trips/<int:trip_id>/roles': views.RoleView.as_view('role_view'),
    '/v1/trips/<int:trip_id>/roles/<string:role_name>': views.RoleView.as_view('delete_role'),
    '/v1/trips/<int:trip_id>/roles/<int:role_id>/<int:user_id>': views.RoleView.as_view('assign_role'),
    '/v1/trips/<int:trip_id>/equipment/<int:equipment_id>': views.EquipmentView.as_view('equipment_view'),
    '/v1/trips/<int:trip_id>/equipment': views.EquipmentView.as_view('add_equipment'),
}

methods = {
    '/v1/trips/<int:trip_id>': ['GET'],
    '/v1/trips/<int:trip_id>/roles': ['GET', 'POST'],
    '/v1/trips/<int:trip_id>/roles/<string:role_name>': ['DELETE'],
    '/v1/trips/<int:trip_id>/roles/<int:role_id>': ['PUT'],
    '/v1/trips/<int:trip_id>/equipment/<int:equipment_id>': ['GET', 'PATCH', 'DELETE'],
    '/v1/equipment': ['POST'],
}
