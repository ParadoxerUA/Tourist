from helper_classes.base_view import BaseView 
from flask import current_app


class SmokeView(BaseView):
    def get(self):
        data = [
            current_app.blueprints['smoke_app'].controllers.SmokeController.get_message(),
        ]
        return self._get_response(data)
