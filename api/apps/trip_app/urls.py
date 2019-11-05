from . import views

urls = {
    '/v1/trip/<int:trip_id>': views.TripView.as_view('trip'),
    '/v1/trip/join/<string:trip_uuid>': views.TripUsersView.as_view('trip-join'),
}
