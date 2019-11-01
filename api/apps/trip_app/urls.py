from . import views

urls = {
    '/v1/trip': views.TripView.as_view('trip'),
}
