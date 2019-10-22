from . import views

urls = {
    '/v1/add_trip': views.AddTripView.as_view('add_trip'),
}
