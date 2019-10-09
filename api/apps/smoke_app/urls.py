from . import views

urls = {
    '/v1/smoke': views.SmokeView.as_view('smoke')
}
