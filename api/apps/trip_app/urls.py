from . import views

urls = {
    '/v1/trip/<int:trip_id>': views.TripView.as_view('get_trip'),
    '/v1/trip': views.TripView.as_view('post_trip'),
}

methods = {
    '/v1/trip/<int:trip_id>': ['GET'],
    '/v1/trip': ['POST'],
}
