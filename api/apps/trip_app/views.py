from helper_classes.base_view import BaseView
from flask import current_app, request, g
from .schemas.trip_schema import TripSchema
from marshmallow import ValidationError
from helper_classes.auth_decorator import login_required


class TripView(BaseView):
    @login_required
    def post(self):
        try:
            trip_data = TripSchema().load(request.json)
            data = current_app.blueprints['trip'].controllers.TripController.create_trip(trip_data, g.session_id)
            return self._get_response(data, status_code=201)
        except (ValidationError, Exception) as err:
            data = [str(err)]
            return self._get_response(data, status_code=400)

    @login_required
    def patch(self):
        trip_id = request.json['trip_id']
        new_uuid = current_app.blueprints['trip'].controllers.TripController.refresh_trip(trip_id, g.session_id )
        if new_uuid:
            return self._get_response(new_uuid, status_code=200)
        else:
            return self._get_response('You have no rights', status_code=400)

    @login_required
    def get(self):
        trip_id = request.json['trip_id']
        uuid = current_app.blueprints['trip'].controllers.TripController.get_trip_uuid(trip_id, g.session_id )
        if uuid:
            return self._get_response(uuid, status_code=200)
        else:
            return self._get_response('You have no rights', status_code=400)
