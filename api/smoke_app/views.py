from helper_classes.base_view import BaseView 
import smoke_app.app as app


class SmokeView(BaseView):
    def dispatch_request(self):
        data = [
            app.smoke_app.controllers.SmokeController.get_message(),
        ]
        return self._get_response(data)
