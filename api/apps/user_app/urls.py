from . import views


urls = {
    '/v1/register': views.UserRegistrationView.as_view('register'),
    '/v1/login': views.LoginView.as_view('login'),
    '/v1/social_login': views.SocialLoginView.as_view('social_login'),
}
