from helper_classes.base_view import BaseView
from flask import current_app, request, g
from .schemas.trip_schema import TripSchema
from marshmallow import ValidationError
from helper_classes.auth_decorator import login_required


class TripView(BaseView):
    @login_required
    def post(self, trip_id):
        try:
            trip_data = TripSchema().load(request.json)
            data = current_app.blueprints['trip'].controllers.TripController.create_trip(trip_data, g.user_id)
            return self._get_response(data, status_code=201)
        except (ValidationError, Exception) as err:
            data = [str(err)]
            return self._get_response(data, status_code=400)

    @login_required
    def patch(self, trip_id):
        new_uuid = current_app.blueprints['trip'].controllers.TripController.refresh_trip_uuid(trip_id, g.user_id )
        if new_uuid:
            return self._get_response(new_uuid, status_code=200)
        else:
            return self._get_response('You have no rights', status_code=400)

    @login_required
    def get(self, trip_id):
        trip_data = current_app.blueprints['trip'].controllers.TripController.get_trip_data(trip_id, g.user_id)
        if trip_data:
            return self._get_response(trip_data, status_code=200)
        else:
            return self._get_response('You have no rights', status_code=400)


class TripUsersView(BaseView):
    @login_required
    def post(self, trip_uuid):
        response = current_app.blueprints['trip'].controllers.TripController.user_to_trip(trip_uuid, g.user_id)
        if response:
            return self._get_response(response, status_code=200)
        else:
            return self._get_response('Couldnt asign user to trip', status_code=400)
