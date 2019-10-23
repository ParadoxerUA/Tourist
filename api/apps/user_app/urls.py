from . import views

urls = {
    '/v1/register': views.UserRegistrationView.as_view('register'),

}
