from helper_classes.base_view import BaseView
from flask import current_app


class TripView(BaseView):
    def get(self):
        data = [
            current_app.blueprints['trip'].controllers.TripController.get_message(),
        ]
        return self._get_response(data)
