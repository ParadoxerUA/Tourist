from . import views

urls = {
    '/v1/create_trip': views.CreateTripView.as_view('create_trip'),
}
