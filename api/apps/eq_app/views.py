from helper_classes.base_view import BaseView
from flask import current_app, request
from .schemas.eq_schema import EqSchema
from marshmallow import ValidationError


class EqView(BaseView):
    def get(self, eq_id):
        """Return response on get request"""

        try:
            data = current_app.blueprints['eq'].controllers.EqController.get_eq_data(eq_id)
        except ValidationError as err:
            return self._get_response(data=err.messages, status_code=400)

        return self._get_response(data, status_code=200)

    def patch(self, eq_id):
        """Return response on patch request"""

        try:
            new_eq_data = EqSchema().load(request.json)
            new_data = current_app.blueprints['eq'].controllers.EqController.update_eq(eq_id, new_eq_data)
        except ValidationError as err:
            return self._get_response(new_data=err.messages, status_code=400)

        return self._get_response(f"Data successfully updated", status_code=200)

    def delete(self, eq_id):
        """"Return response on delete request"""

        try:
            data = current_app.blueprints['eq'].controllers.EqController.delete_eq(eq_id)
        except ValidationError as err:
            return self._get_response(data=err.messages, status_code=400)

        return self._get_response(f"{data} was successfully deleted", status_code=200)

    def post(self):
        """Return response on post request"""

        try:
            eq_data = EqSchema().load(request.json)
            data = current_app.blueprints['eq'].controllers.EqController.create_eq(eq_data)
        except ValidationError as err:
            return self._get_response(data=err.messages, status_code=400)

        return self._get_response(f"{data} was successfully added", status_code=201)
