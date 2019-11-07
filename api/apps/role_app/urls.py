from . import views

urls = {
    '/v1/role/<int:trip_id>': views.RoleView.as_view('get_roles'),
    '/v1/role': views.RoleView.as_view('add_role'),
    '/v1/role/<int:trip_id>/<string:role_name>': views.RoleView.as_view('delete_role'),
}

methods = {
    '/v1/role/<int:trip_id>': ['GET'],
    '/v1/role': ['POST'],
    '/v1/role/<int:trip_id>/<string:role_name>': ['DELETE']
}
