from . import views

urls = {
    '/v1/trip': views.CreateTripView.as_view('trip'),
}
