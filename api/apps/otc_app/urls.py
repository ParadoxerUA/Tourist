from . import views

urls = {
    '/v1/reg_confirmation/<string:uuid>': views.OTCView.as_view('otc')
}
