from . import views


urls = {
    '/v1/trip/<int:trip_id>': views.TripView.as_view('get_trip'),
    '/v1/trip': views.TripView.as_view('post_trip'),
    '/v1/list': views.TripsListView.as_view('trips_list'),
    '/v1/update/<int:trip_id>': views.TripsListView.as_view('update_trip'),
    '/v1/manage_trip/<string:trip_uuid>': views.TripManageView.as_view('join_trip'),
    '/v1/manage_trip/<int:trip_id>': views.TripManageView.as_view('manage_trip'),
    '/v1/trips/<int:trip_id>/roles': views.RoleView.as_view('role_view'),
    '/v1/trips/<int:trip_id>/roles/<string:role_name>': views.RoleView.as_view('delete_role'),
    '/v1/trips/<int:trip_id>/roles/<int:role_id>/<int:user_id>': views.RoleView.as_view('assign_role')
}

methods = {
    '/v1/trips/<int:trip_id>': ['GET'],
    '/v1/trips': ['POST'],
    '/v1/trips/<int:trip_id>/roles': ['GET', 'POST'],
    '/v1/trips/<int:trip_id>/roles/<string:role_name>': ['DELETE'],
    '/v1/trips/<int:trip_id>/roles/<int:role_id>': ['PUT']
}
