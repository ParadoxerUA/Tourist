from . import views


urls = {
    '/v1/user': views.UserView.as_view('user'),
    '/v1/user/trips': views.UserTripsView.as_view('get_user_trips'),
    '/v1/auth': views.AuthView.as_view('authorization'),
}