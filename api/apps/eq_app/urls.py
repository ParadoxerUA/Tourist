from . import views

urls = {
    '/v1/eq/<int:eq_id>': views.EqView.as_view('get_eq'),
    '/v1/eq/<int:eq_id>': views.EqView.as_view('update_eq'),
    '/v1/eq/<int:eq_id>': views.EqView.as_view('delete_eq'),
    '/v1/eq': views.EqView.as_view('add_eq'),
}

methods = {
    '/v1/eq/<int:eq_id>': ['GET'],
    '/v1/eq/<int:eq_id>': ['PATCH'],
    '/v1/eq/<int:eq_id>': ['DELETE'],
    '/v1/eq': ['POST'],
}