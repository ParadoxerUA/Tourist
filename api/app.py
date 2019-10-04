from flask import Flask
import importlib
from config import APPS
from db_config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


def create_app(main_app, app_list, db_config):
    setup_db(main_app, db_config)
    setup_blueprints(main_app, app_list)


def setup_db(main_app, config):
    main_app.config.from_object(config)
    db = SQLAlchemy(main_app)


def setup_blueprints(main_app, app_list):
    for app in app_list:
        curr_module = importlib.import_module(app + '.app')
        app_bp = getattr(curr_module, app)
        app_bp.setup_urls()
        app_bp.setup_controllers()
        main_app.register_blueprint(app_bp)


if __name__ == '__main__':
    create_app(app, APPS, Config)
    app.run()
