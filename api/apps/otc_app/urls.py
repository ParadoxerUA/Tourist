from . import views

urls = {
    '/v1/otc': views.OTCView.as_view('otc')
}
