from helper_classes.base_view import BaseView
from flask import current_app


class OTCView(BaseView):
    def get(self):
        data = [
            current_app.blueprints['otc'].controllers.OTCController.get_message(),
        ]
        return self._get_response(data)

    def post(self):
        pass
