from helper_classes.base_view import BaseView
from flask import current_app, request
from .schemas.trip_schema import TripSchema
from marshmallow import ValidationError


class CreateTripView(BaseView):
    def post(self):
        try:
            if 'Authorization' not in request.headers:
                raise Exception({'header': 'Missing Authorization key'})
            session_id = request.headers.get('Authorization')
            trip_data = TripSchema().load(request.json)
            data = [
                current_app.blueprints['trip'].controllers.TripController.create_trip(trip_data, session_id),
            ]
            return self._get_response(data)
        except (ValidationError, Exception) as err:
            data = [str(err)]
            return self._get_response(data, status_code=400)
