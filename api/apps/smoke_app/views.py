from helper_classes.base_view import BaseView
from flask import current_app
from helper_classes.email_builder.build_email import build_email
import requests, json


class SmokeView(BaseView):
    def get(self):
        data = [
            current_app.blueprints['smoke'].controllers.SmokeController.get_message(),
        ]

        # simple test for build_email()
        # email_data = json.dumps(build_email('wither04@gmail.com', 'email_confirmation', username='Kiril', uuid='69/24/7'))
        # requests.post('http://127.0.0.1:5001/send_email', json=email_data)
        return self._get_response(data)
