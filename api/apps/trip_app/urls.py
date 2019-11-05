from . import views

urls = {
    # '/v1/trip': views.TripView.as_view('trip'),
    '/v1/trip/<int:trip_id>': views.TripView.as_view('trip'),
    '/v1/trips': views.TripsView.as_view('trips')
}
