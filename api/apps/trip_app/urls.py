from . import views


urls = {
    '/v1/trips/<int:trip_id>': views.SingleTripView.as_view('trip'),
    '/v1/trips': views.TripsView.as_view('trips'),
}
