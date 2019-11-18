from helper_classes.base_view import BaseView
from flask import current_app


class OtcView(BaseView):
    def patch(self, uuid):
        data = [
            current_app.blueprints['otc'].controllers\
            .OtcController.handle_uuid(uuid),
        ]
        return self._get_response(data)
