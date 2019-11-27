from . import views


urls = {
    '/v1/user': views.UserView.as_view('user'),
    '/v1/user/change_password': views.ChangePasswordView.as_view('change_password'),
    '/v1/auth': views.AuthView.as_view('authorization'),
}