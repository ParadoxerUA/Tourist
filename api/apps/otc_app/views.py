from helper_classes.base_view import BaseView
from flask import current_app


class OTCView(BaseView):
    def get(self, uuid):
        data = [
            current_app.blueprints['otc'].controllers.OTCController.get_otc_type(uuid),
        ]
        return self._get_response(data)

    def post(self):
        pass
