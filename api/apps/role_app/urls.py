from . import views

urls = {
    '/v1/role': views.RoleView.as_view('role')
}
