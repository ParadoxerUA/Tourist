from . import views

urls = {
    '/smoke': views.SmokeView.as_view('smoke')
}
