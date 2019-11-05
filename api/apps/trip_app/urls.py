from . import views

urls = {
    '/v1/trip/<int:trip_id>': views.TripView.as_view('trip'),
}
