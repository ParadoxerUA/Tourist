from . import views

urls = {
    '/v1/trip/<int:trip_id>': views.TripView.as_view('get_trip'),
    '/v1/trip': views.TripView.as_view('post_trip'),
    '/v1/trips_list': views.TripsListView.as_view('trips_list'),
    '/v1/update/<int:trip_id>': views.TripsListView.as_view('update_trip'),
    '/v1/manage_trip/<string:trip_uuid>': views.TripManageView.as_view('join_trip'),
    '/v1/manage_trip/<int:trip_id>': views.TripManageView.as_view('manage_trip'),
}

methods = {
    '/v1/trip/<int:trip_id>': ['GET'],
    '/v1/trip': ['POST'],
    # i think we dont need it, but not quite sure
    # '/v1/manage_trip': ['PATCH'],
    # '/v1/manage_trip/<string:trip_uuid>': ['POST']
}
