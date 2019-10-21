from helper_classes.base_view import BaseView
from flask import current_app, request
from .schemas.trip_schema import TripSchema
from marshmallow.exceptions import ValidationError


class TripView(BaseView):
    def get(self):
        data = [
            current_app.blueprints['trip'].controllers.TripController.get_message(),
        ]
        return self._get_response(data)

    def post(self):
        schema = TripSchema()
        try:
            result = schema.load(request.json)
            data = [
                current_app.blueprints['trip'].controllers.TripController.add_trip(result),
            ]
            return self._get_response(data)
        except ValidationError as err:
            data = [err.messages, err.valid_data]
            return self._get_response(data, status_code=400)
