from . import views


urls = {
    '/v1/user': views.UserView.as_view('user'),
    '/v1/user/trips': views.UserTripsView.as_view('get_user_trips'),
    '/v1/user/roles': views.UserRolesView.as_view('get_user_roles'),
    '/v1/user/avatar': views.UserAvatarView.as_view('user_avatar'),
    '/v1/user/change_password': views.ChangePasswordView.as_view('change_password'),
    '/v1/login': views.LoginView.as_view('login'),
    '/v1/logout': views.LogoutView.as_view('logout'),
}