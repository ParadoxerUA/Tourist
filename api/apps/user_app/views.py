from helper_classes.base_view import BaseView
from flask import current_app


class UserTestView(BaseView):
    def get(self):
        data = [
            current_app.blueprints['user'].controllers.UserTestController.get_message(),
        ]
        return self._get_response(data)
