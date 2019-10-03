from flask import Flask
import importlib
from config import APPS


app = Flask(__name__)


def create_app(main_app, app_list):
    setup_blueprints(main_app, app_list)


def setup_blueprints(main_app, app_list):
    for app in app_list:
        curr_module = importlib.import_module(app + '.app')
        app_bp = getattr(curr_module, app)
        app_bp.setup_urls()
        app_bp.setup_controllers()
        main_app.register_blueprint(app_bp)


if __name__ == '__main__':
    create_app(app, APPS)
    app.run()
