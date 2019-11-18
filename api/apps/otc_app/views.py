from helper_classes.base_view import BaseView
from flask import current_app


class OTCView(BaseView):
    def patch(self, uuid):
        data = [
            current_app.blueprints['otc'].controllers\
            .OTCController.handle_uuid(uuid, 'user_registration'),
        ]
        return self._get_response(data)
