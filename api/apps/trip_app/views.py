from helper_classes.base_view import BaseView
from flask import current_app, request
from .schemas.trip_schema import TripSchema
from marshmallow import ValidationError


class AddTripView(BaseView):
    def post(self):
        try:
            result = TripSchema().load(request.json)
            data = [
                current_app.blueprints['trip'].controllers.TripController.add_trip(result),
            ]
            return self._get_response(data)
        except ValidationError as err:
            data = [err.messages, err.valid_data]
            return self._get_response(data, status_code=400)
