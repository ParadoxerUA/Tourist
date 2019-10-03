from flask import Flask
import importlib

from config import APPS

app = Flask(__name__)


def create_app(app, applications_list):
    for application in applications_list:
        curr_module = importlib.import_module(application + '.app')
        application_bp = getattr(curr_module, application)
        app.register_blueprint(application_bp)

    return app


if __name__ == '__main__':
    app = create_app(app, APPS)
    app.run()
