from . import views


urls = {
    '/v1/trip/<int:trip_id>': views.SingleTripView.as_view('trip'),
    '/v1/trip': views.SingleTripView.as_view('create_trip'),
    '/v1/trips': views.TripsView.as_view('trips'),
}

methods = {
    '/v1/trip': ['POST'],
}