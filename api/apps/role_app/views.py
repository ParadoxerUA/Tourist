from helper_classes.base_view import BaseView
from flask import current_app


class RoleView(BaseView):
    def get(self):
        data = [
            current_app.blueprints['role'].controllers.RoleController.get_message(),
        ]

