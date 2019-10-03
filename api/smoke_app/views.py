from flask import jsonify
from flask.views import View
from .controller import register_controllers


class SmokeView(View):
    def dispatch_request(self):
        smoke_app_controllers = register_controllers()

        return jsonify(smoke_app_controllers.smoke().get_message(),
                       smoke_app_controllers.smoke().get_question())
