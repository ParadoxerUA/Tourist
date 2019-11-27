from . import views


urls = {
    '/v1/user': views.UserView.as_view('user'),
    '/v1/login': views.LoginView.as_view('login'),
    '/v1/login/social': views.SocialLoginView.as_view('social_login'),
    '/v1/logout': views.LogoutView.as_view('logout'),
}

methods = {
    '/v1/user': ['POST', 'GET', 'PATCH', 'PUT'],
}