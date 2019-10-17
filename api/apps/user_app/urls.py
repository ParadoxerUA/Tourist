from . import views

urls = {
    '/v1/test': views.UserTestView.as_view('test')
}
