from . import views

urls = {
    '/v1/trip/<int:trip_id>': views.TripView.as_view('get_trip'),
    '/v1/trip': views.TripView.as_view('post_trip'),
    '/v1/trips_list': views.TripsListView.as_view('trips_list'),
}

methods = {
    '/v1/trip/<int:trip_id>': ['GET'],
    '/v1/trip': ['POST'],
}
