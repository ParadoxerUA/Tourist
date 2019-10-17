from flask import Flask
from apps import APPS


def _setup_blueprints(main_app, app_list):
    for app in app_list:
        app.setup_urls()
        app.setup_controllers()
        main_app.register_blueprint(app, url_prefix=f'/api/{app.name}')


def create_app(config):
    main_app = Flask(__name__)
    main_app.config.from_object(config)
    _setup_blueprints(main_app, APPS)
    return main_app


if __name__ == '__main__':
    from config import DebugConfig
    app = create_app(DebugConfig)
    app.run()

