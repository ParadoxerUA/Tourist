from . import views


urls = {
    '/v1/user': views.UserView.as_view('user'),
    '/v1/user/trips': views.UserTripsView.as_view('user_trips'),
    '/v1/login': views.LoginView.as_view('login'),
    '/v1/logout': views.LogoutView.as_view('logout'),
}