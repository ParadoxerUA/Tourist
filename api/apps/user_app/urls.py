from . import views


urls = {
    '/v1/user': views.UserView.as_view('user'),
    '/v1/user/trips': views.UserTripsView.as_view('get_user_trips'),
    # tofix by Kirill
    '/v1/user/change_password': views.ChangePasswordView.as_view('change_password'),
    '/v1/auth': views.AuthView.as_view('authorization'),
}