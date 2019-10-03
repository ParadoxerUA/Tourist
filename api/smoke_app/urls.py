from .views import SmokeView


def add_urls(app):
    app.add_url_rule('/smoke', view_func=SmokeView.as_view('smoke_app'))
